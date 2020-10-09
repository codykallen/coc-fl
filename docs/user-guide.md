# User Guide

## Specifying policy parameters
 - To specify business tax parameters, create a CSV file as in `policy_baseline.csv`
 - The directly controlled business tax parameters are: `taxrt_ccorp`, `intded_c`, `intded_nc1`, `gilti_ex`, `fdii_ex`, `ccr_sheet`, `stepup``. Set these to the desired values.
 - The other tax parameters are weighted average marginal tax (or subsidy) rates on different types of income (or state/local taxes), computed using `mtr-taxcalc.py`. Either set these to desired values, or estimate them using `mtr-taxcalc`. For the latter, see below for instructions.
 - Descriptions of each policy parameter are in `docs\policy_variables.md`.
 - In the Python code, create a `Policy()` object using the policy name. For example:
```pol = Policy('policy_POLICYNAME'.csv')```

## Specifying economic parameters
 - The basic parameters are specified in `Parameter.set_chosen_parms()`. They fall into three categories:
   - Basic economic parameters: risk-free rate, inflation rate, debt/equity premiums, required rates of return, financial income rate.
   - Dictionaries: information relevant for calculating the return to saving (`shares`), and state/local tax rates on income and property (`sltaxes`).
   - Equation styles: whether to include state/local taxes in calculations (`include_slt`), and whether to make equations forward-looking.
 - To set your own values for these, create a Python dictionary with the parameter names as keys and their new values.
 - Either pass this dictionary to the `Parameter` class when creating it, or when calling `Parameter.update_params()`. For example, the following two methods are equivalent.
```
paramdict = {'include_slt': False}
param1 = Parameter(paramdict)
param2 = Parameter()
param2.update_parms(pdict)
```

## Calculating marginal tax rates on individual income
 - To calculate weighted average MTRs on individual income, create a JSON file or a reform dictionary for Tax-Calculator.
 - Use code as in `mtr-taxcalc.py`. 
 - Create a Calculator with the reform, compute the relevant MTRs for each year, and save the results to the relevant policy file.
 - Note that this requires the IRS public use file, cleaned/augmented using `taxdata`.

## Setting up and running calculations
 - Create a `Parameter` object and a `Policy` object. Pass these as arguments to create a Calculator class. 
 - For any desired year, calculate all results using the `Calculator.calc_all()` function.
 - For example:
```
parm = Parameter()
pol = Policy()
calc = Calculator(parm, pol)
calc.calc_all(2021)
calc.calc_all(2025)
calc.calc_all(2029)
```

## Tabulating and saving results
 - Create an `OutputBuilder` object by passing the relevant Calculator object and a key (string) to describe it.
 - To store raw results by firm type, asset type and year, using the `ObjectBuilder.store_raw()` function.
 - To store results tabulated by industry, use the `ObjectBuilder.tabulate_industry()` function.
 - To store results tabulated by asset type, use the `ObjectBuilder.tabulate_asset()` function.
 - All three of these functions store their results as CSV files in the `output\raw\` folder.
 - To produce multiyear tables with select aggregate results as in Fitzgerald, Hassett, Kallen & Mulligan (2020), use the `OutputBuilder.tabulate_main_multiyear()` function, which saves in the `output\main\` folder.
 - To compute the standard deviation of the cost of capital, use the `ObjectBuilder.cocVariation()` function.
 - For example:
```
ob = ObjectBuilder(calc, 'test')
ob.store_raw(2021)
ob.tabulate_industry(2021)
ob.tabulate_asset(2021)
ob.tabulate_main_multiyear([2021, 2025, 2029])
print('CoC std dev: ', ob.cocVariation(2021))
```

