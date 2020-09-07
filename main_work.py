# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 11:23:17 2020

@author: cody_
"""

import os
os.chdir('C:/Users/cody_/Documents/GitHub/coc-fl')
import numpy as np
import pandas as pd
from parameter import Parameter
from policy import Policy
from calculator import Calculator
from outputBuilder import OutputBuilder
from config import *

"""
Note: Before running the following, make sure to execute the code in
      data.py. Also, compute the average EMTRs on each type of pass-through
      income using iiEMTR.py.
"""

# Whether to look forward or to use naive equations
eqstyle = 'forward'
assert eqstyle in ['naive', 'forward']

# Current law baseline
pol_base = Policy()
parm_base = Parameter()
calc_base = Calculator(parm_base, pol_base)

# Extension of individual income tax parameters
pol_extII = Policy('policy_extendII.csv')
parm_extII = Parameter()
calc_extII = Calculator(parm_extII, pol_extII)

# Extension of all TCJA tax parameters
pol_extAll = Policy('policy_extendAll.csv')
parm_extAll = Parameter()
calc_extAll = Calculator(parm_extAll, pol_extAll)

# Biden tax plan
pol_biden = Policy('policy_biden.csv')
parm_biden = Parameter()
calc_biden = Calculator(parm_biden, pol_biden)


# Calculate results for year year
for year in range(2021, 2030):
    if eqstyle == 'naive':
        calc_base.calc_all_basic(year)
        calc_extII.calc_all_basic(year)
        calc_extAll.calc_all_basic(year)
        calc_biden.calc_all_basic(year)
    else:
        calc_base.calc_all_forward(year)
        calc_extII.calc_all_forward(year)
        calc_extAll.calc_all_forward(year)
        calc_biden.calc_all_forward(year)

# Create objects to store results
ob_base = OutputBuilder(calc_base, 'base')
ob_extII = OutputBuilder(calc_extII, 'extII')
ob_extAll = OutputBuilder(calc_extAll, 'extAll')
ob_biden = OutputBuilder(calc_biden, 'biden')


# Store raw output for 2021
ob_base.store_raw(2021)
ob_extII.store_raw(2021)
ob_extAll.store_raw(2021)
ob_biden.store_raw(2021)

# Tabulate main results by year
main_mtr_base = pd.DataFrame({'Category': catlist})
main_mtr_extII = pd.DataFrame({'Category': catlist})
main_mtr_extAll = pd.DataFrame({'Category': catlist})
main_mtr_biden = pd.DataFrame({'Category': catlist})
main_coc_base = pd.DataFrame({'Category': catlist})
main_coc_extII = pd.DataFrame({'Category': catlist})
main_coc_extAll = pd.DataFrame({'Category': catlist})
main_coc_biden = pd.DataFrame({'Category': catlist})
main_ucoc_base = pd.DataFrame({'Category': catlist})
main_ucoc_extII = pd.DataFrame({'Category': catlist})
main_ucoc_extAll = pd.DataFrame({'Category': catlist})
main_ucoc_biden = pd.DataFrame({'Category': catlist})


for year in range(2021, 2030):
    # Run tabulations
    res1_base = ob_base.tabulate_main(year)
    res1_extII = ob_extII.tabulate_main(year)
    res1_extAll = ob_extAll.tabulate_main(year)
    res1_biden = ob_biden.tabulate_main(year)
    # Store MTR results
    main_mtr_base[str(year)] = res1_base['METR']
    main_mtr_extII[str(year)] = res1_extII['METR']
    main_mtr_extAll[str(year)] = res1_extAll['METR']
    main_mtr_biden[str(year)] = res1_biden['METR']
    # Store CoC results
    main_coc_base[str(year)] = res1_base['CoC']
    main_coc_extII[str(year)] = res1_extII['CoC']
    main_coc_extAll[str(year)] = res1_extAll['CoC']
    main_coc_biden[str(year)] = res1_biden['CoC']
    # Store user CoC results
    main_ucoc_base[str(year)] = res1_base['UCoC']
    main_ucoc_extII[str(year)] = res1_extII['UCoC']
    main_ucoc_extAll[str(year)] = res1_extAll['UCoC']
    main_ucoc_biden[str(year)] = res1_biden['UCoC']

# Save results to tables for combining later
main_coc_base.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_coc_' + 'base' + '.csv', index=False)
main_coc_extII.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_coc_' + 'extII' + '.csv', index=False)
main_coc_extAll.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_coc_' + 'extAll' + '.csv', index=False)
main_coc_biden.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_coc_' + 'biden' + '.csv', index=False)
main_mtr_base.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_mtr_' + 'base' + '.csv', index=False)
main_mtr_extII.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_mtr_' + 'extII' + '.csv', index=False)
main_mtr_extAll.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_mtr_' + 'extAll' + '.csv', index=False)
main_mtr_biden.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_mtr_' + 'biden' + '.csv', index=False)
main_ucoc_base.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_ucoc_' + 'base' + '.csv', index=False)
main_ucoc_extII.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_ucoc_' + 'extII' + '.csv', index=False)
main_ucoc_extAll.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_ucoc_' + 'extAll' + '.csv', index=False)
main_ucoc_biden.to_csv(OUTPUTPATH + 'compiled_' + eqstyle + '_ucoc_' + 'biden' + '.csv', index=False)

















