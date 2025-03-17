# Market Clearing Optimization

## Overview
This project implements a market-clearing optimization model for an electricity market. The model considers buyers (demanders) and sellers (generators) connected through a transmission network and determines optimal allocations that minimize total cost while respecting network constraints.

## Dependencies
The script requires the following Python libraries:
- `pandas` for data handling
- `numpy` for numerical computations
- `scipy` for mathematical optimizations

Install the required packages using:
```bash
pip install pandas numpy scipy
```

## Input Data
The script reads three CSV files:
1. **buyers.csv**: Contains buyer information with columns:
   - `node`: The node at which the buyer is located
   - `id`: Unique identifier for the buyer
   - `marginal cost`: Cost per unit of electricity purchased
   - `quantity`: Maximum quantity that can be purchased

2. **sellers.csv**: Contains seller information with columns:
   - `node`: The node at which the seller is located
   - `id`: Unique identifier for the seller
   - `marginal cost`: Cost per unit of electricity sold
   - `quantity`: Maximum quantity that can be sold

3. **network.csv**: Defines the transmission network with columns:
   - `from node`: Starting node of a transmission line
   - `to node`: Ending node of a transmission line
   - `reactance`: Electrical reactance of the line
   - `capacity`: Maximum transmission capacity of the line

## Methodology
The script performs the following steps:
1. **Load and parse input data** using Pandas.
2. **Compute network properties**:
   - Construct the **incidence matrix** representing the network.
   - Compute the **susceptance matrix (Bd)** from reactance values.
   - Derive the **reduced admittance matrix (B)** for power flow calculations.
3. **Formulate the optimization problem**:
   - Define decision variables (quantities bought/sold).
   - Apply **power flow constraints** using the admittance matrix.
   - Apply **supply-demand balance constraints**.
   - Use **linear programming** (`scipy.optimize.linprog`) to minimize cost.
4. **Output the market clearing results**:
   - Display the cleared buyers and sellers with their allocations.
   - Report the **total social welfare (negative of minimized cost)**.

## Execution
Run the script with:
```bash
python market_clearing.py
```
Make sure that `buyers.csv`, `sellers.csv`, and `network.csv` are in the same directory.

## Output
If successful, the script prints:
- Cleared buyers and the amount they buy
- Cleared sellers and the amount they sell
- Unmatched sellers
- Total minimized cost (social welfare)

If optimization fails, an error message is displayed.

## Applications
This model can be used for:
- Simulating electricity market dynamics
- Evaluating grid congestion management strategies
- Assessing economic efficiency in power trading

## License
This project is open-source and provided under the MIT License.

## Contact
For queries or contributions, feel free to reach out.

