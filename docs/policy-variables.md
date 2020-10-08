# Policy Variable Descriptions

This document describes the policy variables available to use. These fall into three categories:

    1) Main business tax variables contained in the `policy_*.csv` files.
    2) Capital cost recovery rules in `CCR_rules.xlsx`.
    3) Individual income tax variables in the JSON files.

## Main business tax variables

 - `taxrt_ccorp`: 
    - Description: Corporate tax rate
    - Acceptable values: min 0, max 1
 - `taxrt_scorp`: 
    - Description: Weighted average MTR on S corporation income. Calculted using `mtr-taxcalc.py`.
    - Acceptable values: min 0, max 1
 - `taxrt_soleprop`: 
    - Description: Weighted average MTR on sole proprietorship income. Calculted using `mtr-taxcalc.py`.
    - Acceptable values: min 0, max 1
 - `taxrt_partner`: 
    - Description: Weighted average MTR on partnership income. Calculted using `mtr-taxcalc.py`.
    - Acceptable values: min 0, max 1
 - `intded_c`: 
    - Description: Deductible share of corporate interest deductions.
    - Acceptable values: min 0, max 1
 - `intded_nc`: 
    - Description: Deductible share of noncorporate business interest deductions.
    - Acceptable values: min 0, max 1
 - `gilti_ex`: 
    - Description: Share of GILTI income excluded from taxable income.
    - Acceptable values: min 0, max 1
 - `fdii_ex`: 
    - Description: Share of FDII income excluded from taxable income.
    - Acceptable values: min 0, max 1
 - `ccr_sheet`: 
    - Description: Sheet name in `CCR_rules.xlsx` with relevant capital cost recovery rules.
    - Acceptable values: Must be valid sheet name in `CCR_rules.xlsx`.
 - `taxrt_int`: 
    - Description: Weighted average MTR on interest income. Calculted using `mtr-taxcalc.py`.
    - Acceptable values: min 0, max 1
 - `taxrt_div`: 
    - Description: Weighted average MTR on dividend income. Calculted using `mtr-taxcalc.py`.
    - Acceptable values: min 0, max 1
 - `taxrt_scg`: 
    - Description: Weighted average MTR on short-term capital gains. Calculted using `mtr-taxcalc.py`.
    - Acceptable values: min 0, max 1
 - `taxrt_lcg`: 
    - Description: Weighted average MTR on long-term capital gains. Calculted using `mtr-taxcalc.py`.
    - Acceptable values: min 0, max 1
 - `stepup`: 
    - Description: Indicator for whether unrealized capital gains at death eligible for step-up basis.
    - Acceptable values: 0 or 1. 0 indicates unrealized capital gains at death are subject to capital gains taxes.
 - `sub_slti`: 
    - Description: Weighted average marginal subsidy on state and local taxes paid. Calculted using `mtr-taxcalc.py`.
    - Acceptable values: min 0, max 1

## Capital cost recovery rules

All measures are by asset type, using the given BEA asset codes.

 - `method`: 
    - Description: Method for capital cost recovery (declining balance, straight-line, expensing, economic).
    - Acceptable values: DB, SL, EXP, ECON
 - `life`: 
    - Description: Tax life for depreciation deductions.
    - Acceptable values: min 0, max 50
 - `acclrt`: 
    - Description: Acceleration rate for declining balance depreciation method (not relevant for other methods).
    - Acceptable values: min 1
 - `bonus`: 
    - Description: Bonus depreciation rate.
    - Acceptable values: min 0, max 1
 - `itc_base`:
    - Description: Reduction in depreciable basis by investment tax credit.
    - Acceptable values: min 0, max 1
 - `itcrt`: 
    - Description: Investment tax credit rate.
    - Acceptable values: min 0
 - `itc_life`: 
    - Description: Length of period over which to claim the R&D tax credit (0 for immediate credit).
    - Acceptable values: min 0

## Individual income tax variables

In general, all policy variables and descriptions are available in `tcLocal\policy_current_law.json` and in the [Tax-Calculator documentation](https://pslmodels.github.io/Tax-Calculator/).

 - `RetirementSaving_crt`: 
    - Description: Credit for contributions to retirement savings accounts.
 - `PT_qbid_ps`: 
    - Description: QBID phases out above this threshold of taxable income.
 - `PT_qbid_prt`: 
    - Description: QBID phases out at this rate on taxable income in excess of PT_qbid_pthd.
