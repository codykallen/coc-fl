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
      income using mtr_taxcalc.py.
"""

# Whether to look forward or to use naive equations
eqstyle = 'naive'
assert eqstyle in ['naive', 'forward']

# Current law
pol_clbase = Policy()
parm_clbase = Parameter()
calc_clbase = Calculator(parm_clbase, pol_clbase)

# Extension of individual income tax parameters
pol_extII = Policy('policy_extendII.csv')
parm_extII = Parameter()
calc_extII = Calculator(parm_extII, pol_extII)

# Extension of all current TCJA tax parameters (current policy baseline)
pol_cpbase = Policy('policy_currentPolicy.csv')
parm_cpbase = Parameter()
calc_cpbase = Calculator(parm_cpbase, pol_cpbase)

# Biden tax plan
pol_biden = Policy('policy_biden.csv')
parm_biden = Parameter()
calc_biden = Calculator(parm_biden, pol_biden)


# Calculate results for year year
for year in range(2021, 2030):
    if eqstyle == 'naive':
        calc_clbase.calc_all_basic(year)
        calc_extII.calc_all_basic(year)
        calc_cpbase.calc_all_basic(year)
        calc_biden.calc_all_basic(year)
    else:
        calc_clbase.calc_all_forward(year)
        calc_extII.calc_all_forward(year)
        calc_cpbase.calc_all_forward(year)
        calc_biden.calc_all_forward(year)

# Create objects to store results
ob_clbase = OutputBuilder(calc_clbase, 'clbase')
ob_extII = OutputBuilder(calc_extII, 'extII')
ob_cpbase = OutputBuilder(calc_cpbase, 'cpbase')
ob_biden = OutputBuilder(calc_biden, 'biden')


# Store raw output for 2021
ob_clbase.store_raw(2021)
ob_extII.store_raw(2021)
ob_cpbase.store_raw(2021)
ob_biden.store_raw(2021)

# Tabulate main results by year
main_mtr_clbase = pd.DataFrame({'Category': catlist})
main_mtr_extII = pd.DataFrame({'Category': catlist})
main_mtr_cpbase = pd.DataFrame({'Category': catlist})
main_mtr_biden = pd.DataFrame({'Category': catlist})
main_mettr_clbase = pd.DataFrame({'Category': catlist})
main_mettr_extII = pd.DataFrame({'Category': catlist})
main_mettr_cpbase = pd.DataFrame({'Category': catlist})
main_mettr_biden = pd.DataFrame({'Category': catlist})
main_coc_clbase = pd.DataFrame({'Category': catlist})
main_coc_extII = pd.DataFrame({'Category': catlist})
main_coc_cpbase = pd.DataFrame({'Category': catlist})
main_coc_biden = pd.DataFrame({'Category': catlist})
main_ucoc_clbase = pd.DataFrame({'Category': catlist})
main_ucoc_extII = pd.DataFrame({'Category': catlist})
main_ucoc_cpbase = pd.DataFrame({'Category': catlist})
main_ucoc_biden = pd.DataFrame({'Category': catlist})
main_eatrd_clbase = pd.DataFrame({'Category': catlist})
main_eatrd_extII = pd.DataFrame({'Category': catlist})
main_eatrd_cpbase = pd.DataFrame({'Category': catlist})
main_eatrd_biden = pd.DataFrame({'Category': catlist})
main_eatrf_clbase = pd.DataFrame({'Category': catlist})
main_eatrf_extII = pd.DataFrame({'Category': catlist})
main_eatrf_cpbase = pd.DataFrame({'Category': catlist})
main_eatrf_biden = pd.DataFrame({'Category': catlist})

for year in range(2021, 2030):
    # Run tabulations
    res1_clbase = ob_clbase.tabulate_main(year)
    res1_extII = ob_extII.tabulate_main(year)
    res1_cpbase = ob_cpbase.tabulate_main(year)
    res1_biden = ob_biden.tabulate_main(year)
    # Store MTR results
    main_mtr_clbase[str(year)] = res1_clbase['METR']
    main_mtr_extII[str(year)] = res1_extII['METR']
    main_mtr_cpbase[str(year)] = res1_cpbase['METR']
    main_mtr_biden[str(year)] = res1_biden['METR']
    # Store MTR results
    main_mettr_clbase[str(year)] = res1_clbase['METTR']
    main_mettr_extII[str(year)] = res1_extII['METTR']
    main_mettr_cpbase[str(year)] = res1_cpbase['METTR']
    main_mettr_biden[str(year)] = res1_biden['METTR']
    # Store CoC results
    main_coc_clbase[str(year)] = res1_clbase['CoC']
    main_coc_extII[str(year)] = res1_extII['CoC']
    main_coc_cpbase[str(year)] = res1_cpbase['CoC']
    main_coc_biden[str(year)] = res1_biden['CoC']
    # Store user CoC results
    main_ucoc_clbase[str(year)] = res1_clbase['UCoC']
    main_ucoc_extII[str(year)] = res1_extII['UCoC']
    main_ucoc_cpbase[str(year)] = res1_cpbase['UCoC']
    main_ucoc_biden[str(year)] = res1_biden['UCoC']
    # Store EATR results
    main_eatrd_clbase[str(year)] = res1_clbase['EATRd']
    main_eatrd_extII[str(year)] = res1_extII['EATRd']
    main_eatrd_cpbase[str(year)] = res1_cpbase['EATRd']
    main_eatrd_biden[str(year)] = res1_biden['EATRd']
    main_eatrf_clbase[str(year)] = res1_clbase['EATRf']
    main_eatrf_extII[str(year)] = res1_extII['EATRf']
    main_eatrf_cpbase[str(year)] = res1_cpbase['EATRf']
    main_eatrf_biden[str(year)] = res1_biden['EATRf']
    # Print coefficient of variation for CoC
    if year in [2021, 2025, 2029]:
        print('Base StD: ', ob_clbase.cocVariation(year))
        print('ExtII StD: ', ob_extII.cocVariation(year))
        print('ExtAll StD: ', ob_cpbase.cocVariation(year))
        print('Biden StD: ', ob_biden.cocVariation(year))

# Save results to tables for combining later
main_coc_clbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_coc_' + 'clbase' + '.csv', index=False)
main_coc_extII.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_coc_' + 'extII' + '.csv', index=False)
main_coc_cpbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_coc_' + 'cpbase' + '.csv', index=False)
main_coc_biden.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_coc_' + 'biden' + '.csv', index=False)
main_mtr_clbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_mtr_' + 'clbase' + '.csv', index=False)
main_mtr_extII.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_mtr_' + 'extII' + '.csv', index=False)
main_mtr_cpbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_mtr_' + 'cpbase' + '.csv', index=False)
main_mtr_biden.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_mtr_' + 'biden' + '.csv', index=False)
main_mettr_clbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_mettr_' + 'clbase' + '.csv', index=False)
main_mettr_extII.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_mettr_' + 'extII' + '.csv', index=False)
main_mettr_cpbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_mettr_' + 'cpbase' + '.csv', index=False)
main_mettr_biden.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_mettr_' + 'biden' + '.csv', index=False)
main_ucoc_clbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_ucoc_' + 'clbase' + '.csv', index=False)
main_ucoc_extII.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_ucoc_' + 'extII' + '.csv', index=False)
main_ucoc_cpbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_ucoc_' + 'cpbase' + '.csv', index=False)
main_ucoc_biden.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_ucoc_' + 'biden' + '.csv', index=False)
main_eatrd_clbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_eatrd_' + 'clbase' + '.csv', index=False)
main_eatrd_extII.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_eatrd_' + 'extII' + '.csv', index=False)
main_eatrd_cpbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_eatrd_' + 'cpbase' + '.csv', index=False)
main_eatrd_biden.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_eatrd_' + 'biden' + '.csv', index=False)
main_eatrf_clbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_eatrf_' + 'clbase' + '.csv', index=False)
main_eatrf_extII.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_eatrf_' + 'extII' + '.csv', index=False)
main_eatrf_cpbase.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_eatrf_' + 'cpbase' + '.csv', index=False)
main_eatrf_biden.to_csv(OUTPUTPATH + 'main/' + eqstyle + '_eatrf_' + 'biden' + '.csv', index=False)















