# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 11:23:17 2020

@author: cody_
"""

import os
os.chdir('C:/Users/cody_/Documents/GitHub/coc-fl')
from parameter import Parameter
from policy import Policy
from calculator import Calculator
from outputBuilder import OutputBuilder

"""
Note: Before running the following, make sure to execute the code in
      data.py. Also, compute the average EMTRs on each type of pass-through
      income using mtr_taxcalc.py.
"""

parmdict = {'forwardLooking': True}

# Current law
pol_clbase = Policy()
parm_clbase = Parameter(parmdict)
calc_clbase = Calculator(parm_clbase, pol_clbase)

# Extension of individual income tax parameters
pol_extII = Policy('policy_extendII.csv')
parm_extII = Parameter(parmdict)
calc_extII = Calculator(parm_extII, pol_extII)

# Extension of all current TCJA tax parameters (current policy baseline)
pol_cpbase = Policy('policy_currentPolicy.csv')
parm_cpbase = Parameter(parmdict)
calc_cpbase = Calculator(parm_cpbase, pol_cpbase)

# Biden tax plan
pol_biden = Policy('policy_biden.csv')
parm_biden = Parameter(parmdict)
calc_biden = Calculator(parm_biden, pol_biden)


# Calculate results for year year
yearlist = [*range(2021, 2023)]
for year in yearlist:
    calc_clbase.calc_all(year)
    calc_extII.calc_all(year)
    calc_cpbase.calc_all(year)
    calc_biden.calc_all(year)


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


# Store tabulations by industry and by asset type
ob_clbase.tabulate_industry(2021)
ob_extII.tabulate_industry(2021)
ob_cpbase.tabulate_industry(2021)
ob_biden.tabulate_industry(2021)
ob_clbase.tabulate_asset(2021)
ob_extII.tabulate_asset(2021)
ob_cpbase.tabulate_asset(2021)
ob_biden.tabulate_asset(2021)


# Tabulate main results for every year 2021-2029
ob_clbase.tabulate_main_multiyear(yearlist)
ob_extII.tabulate_main_multiyear(yearlist)
ob_cpbase.tabulate_main_multiyear(yearlist)
ob_biden.tabulate_main_multiyear(yearlist)


# Print standard deviation of cost of capital for select years
for year in [2021, 2025, 2029]:
    print('Base StD: ', ob_clbase.cocVariation(year))
    print('ExtII StD: ', ob_extII.cocVariation(year))
    print('ExtAll StD: ', ob_cpbase.cocVariation(year))
    print('Biden StD: ', ob_biden.cocVariation(year))

















