# File map

## Python files for cost of capital calculations (not for direct use)
 - `calculator.py`: Runs all calculations.
 - `config.py`: Contains relevant metadata.
 - `functions.py`: Contains functions used for calculations done in `calculator.py`.
 - `outputBuilder.py`: Tabulates and stores results.
 - `parameter.py`: Sets up parameters and assumptions.
 - `policy.py`: Sets up policy parameters.

## Python files for direct use
 - `data.py`: Converts raw BEA and IRS data into stocks and investment by asset type, industry and firm type.
 - `main_work.py`: Main file for calculations in Fitzgerald, Hassett, Kallen and Mulligan (2020).
 - `mtr-taxcalc.py`: Computes marginal tax rates and subsidy rates on different income types using local version of Tax-Calculator, and saves these in the relevant `policy_` CSV files.
 - `other-taxcalc.py`: Other computations using local version of Tax-Calculator.

## Policy files
 - `policy_baseline.csv`: Main CSV file with policy parameters for each year.
 - `policy_currentPolicy.csv`: CSV file with current policy parameters extended forward.
 - `policy_biden.csv`: CSV file with policy parameters from the Biden proposals.
 - `policy_extendII`: CSV file with policy parameters for just extending the TCJA's individual income tax provisions.
 - `CCR_rules.xlsx`: Excel file with alternative versions of capital cost recovery rules by asset type.
 - `JSONs\biden.json`: JSON reform file of Biden tax provisions for local version of Tax-Calculator.
 - `JSONs\extendII.json`: JSON reform file for extending the TCJA's II tax provisions, for local version of Tax-Calculator.

## Other folders and files
 - `data_files\`: Raw data files used for the model.
 - `tcLocal\`: Local version of Tax-Calculator, modified for more MTR variables and to allow new Biden provisions.
 - `Appendix-CoC.pdf`: Methodological appendix from Fitzgerald, Hassett, Kallen and Mulligan (2020).
