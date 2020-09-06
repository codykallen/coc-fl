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

"""
Note: Before running the following, make sure to execute the code in
      data.py. Also, compute the average EMTRs on each type of pass-through
      income using iiEMTR.py.
"""
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
    calc_base.calc_all_basic(year)
    calc_extII.calc_all_basic(year)
    calc_extAll.calc_all_basic(year)
    calc_biden.calc_all_basic(year)

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
for year in range(2021, 2030):
    ob_base.tabulate_main(year)
    ob_extII.tabulate_main(year)
    ob_extAll.tabulate_main(year)
    ob_biden.tabulate_main(year)















