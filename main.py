import pandas as pd
import numpy as np
import scipy as sp

buyers = pd.read_csv('buyers.csv') # (node, id, marginal cost, quantity)
sellers = pd.read_csv('sellers.csv') # (node, id, marginal cost, quantity)
network = pd.read_csv('network.csv') # (from node, to node, reactance, capacity)  

def incidence_matrix(network, nodes):
    # Initialize the incidence matrix A (L × N)
    node_index = {node: i for i, node in enumerate(nodes)}
    L, N = len(network), len(nodes)
    A = np.zeros((L, N))

    # Fill the incidence matrix
    for i, (from_node, to_node, _, _) in enumerate(network.itertuples(index=False)):
        A[i, node_index[from_node]] = 1   # Line starts from node → +1
        A[i, node_index[to_node]] = -1    # Line goes to node → -1
    
    return A

Bd = np.diag(1/network.iloc[:,2]) # Diagonal matrix of susceptances
nodes = sorted(set(network.iloc[:, 0]) | set(network.iloc[:, 1]))  # Unique nodes
A = incidence_matrix(network, nodes) # Incidence matrix
reduced_A = A[:,1:]
B = reduced_A.T @ Bd @ reduced_A # Reduced admittance matrix
Fmax = np.array(network.iloc[:,3]) # Maximum flow limits

Psi = np.zeros((len(network), len(nodes)))
Psi[:,1:] = Bd @ reduced_A @ np.linalg.inv(B)

cof = np.concatenate([-buyers.iloc[:,2], sellers.iloc[:,2]])

# Constraints of Decision variables with lower bound set to 0
constraints = [(0, buyers.iloc[i,3]) for i in range(len(buyers))] + [(0, sellers.iloc[i,3]) for i in range(len(sellers))] 

# PD and PG matrices
PG = np.zeros((len(nodes), len(cof)))
PD = np.zeros((len(nodes), len(cof)))
for i in range(len(buyers)):
    PD[buyers.iloc[i,0]-1, i] = 1
for i in range(len(sellers)):
    PG[sellers.iloc[i,0]-1, len(buyers)+i] = 1

# Lagrange Constriants
A_eq = np.array([1]*len(buyers) + [-1]*len(sellers)).reshape(1,-1)
B_eq = np.array([0.0])

A_ub = np.vstack([Psi @ (PG - PD), -Psi @ (PG - PD)])
b_ub = np.hstack([Fmax, Fmax]) 

# Output vector = concataenation of buyers' quantities and sellers' quantities
from scipy.optimize import linprog 
output = result = linprog(cof, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=B_eq, bounds=constraints, method='highs')

if output.success:
    allocations = output.x  # Extract the optimal allocation
    
    print("Market Clearing Results:")
    print("-----------------------------------")
    
    # Buyers' transactions
    print("Cleared Buyers:")
    for i in range(len(buyers)):
        if allocations[i] > 0:  # Buyer is cleared if they receive a nonzero allocation
            print(f"Buyer {buyers.iloc[i,1]} at Node {buyers.iloc[i,0]} buys {allocations[i]:.2f} units")
    
    print("-----------------------------------")
    
    # Sellers' transactions
    print("Cleared Sellers:")
    for i in range(len(sellers)):
        if allocations[len(buyers) + i] > 0:  # Seller is cleared if they sell a nonzero allocation
            print(f"Seller {sellers.iloc[i,1]} at Node {sellers.iloc[i,0]} sells {allocations[len(buyers) + i]:.2f} units")
        else:
            print(f"Seller {sellers.iloc[i,1]} at Node {sellers.iloc[i,0]} is not cleared")
    print("-----------------------------------")
    print(f"Total Social Welfare (Minimized Cost): {-output.fun:.2f}")
else:
    print("Optimization failed. No feasible market clearing solution found.")