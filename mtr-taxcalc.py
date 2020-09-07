# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 07:36:10 2020

@author: cody_
"""

import os
os.chdir('C:/Users/cody_/Documents/GitHub/coc-fl')
import numpy as np
import pandas as pd
import taxcalc
from taxcalc import *

puf_path = 'puf.csv'

def make_calculator(refdict=None, year=2020):
    """
    Creates a calculator advanced to the given year and calculates tax results
    Note: Passing an empty dictionary to refdict produces a 
          current law calculator (TCJA law)
    """
    assert year in range(2014, 2030)
    pol = Policy()
    rec = Records(puf_path)
    if refdict is not None:
        assert type(refdict) is dict
        pol.implement_reform(refdict)
    calc1 = Calculator(policy=pol, records=rec, verbose=False)
    calc1.advance_to_year(year)
    calc1.calc_all()
    return calc1

def calcTauNC(calc):
    """
    Calculates the effective marginal tax rate on each type of pass-through business
    income.
    """
    inc1 = np.abs(calc.array('e00900'))
    inc2 = np.abs(calc.array('e26270'))
    inc3 = np.abs(calc.array('e02000') - calc.array('e26270'))
    wgt = calc.array('s006')
    mtr1 = calc.mtr('e00900p', calc_all_already_called=True)[2]
    mtr2 = calc.mtr('e26270', calc_all_already_called=True)[2]
    mtr3 = calc.mtr('e02000', calc_all_already_called=True)[2]
    wmtr1 = sum(mtr1 * inc1 * wgt) / sum(inc1 * wgt)
    wmtr2 = sum((mtr2 * inc2 + mtr3 * inc3) * wgt) / sum((inc2 + inc3) * wgt)
    return (wmtr1, wmtr2)


# Create baseline
calc_base = make_calculator(None, 2019)

# Version with extension of II tax policies
param_extII = Calculator.read_json_param_objects('JSONs/extendII.json', None)
calc_extII = make_calculator(param_extII['policy'], 2019)

# Version with Biden plan
#param_biden = Calculator.read_json_param_objects('JSONs/biden.json', None)
#calc_biden = make_calculator(param_biden['policy'], 2019)

# Compute relevant MTRs for each year
mtr_sp_base = np.zeros(10)
mtr_ps_base = np.zeros(10)
mtr_sp_extII = np.zeros(10)
mtr_ps_extII = np.zeros(10)
#mtr_sp_biden = np.zeros(10)
#mtr_ps_biden = np.zeros(10)

for i in range(10):
    # Advance each Calculator
    calc_base.increment_year()
    calc_base.calc_all()
    calc_extII.increment_year()
    calc_extII.calc_all()
    #calc_biden.increment_year()
    #calc_biden.calc_all()
    # Compute and save MTRs
    mtrs1 = calcTauNC(calc_base)
    mtr_sp_base[i] = mtrs1[0]
    mtr_ps_base[i] = mtrs1[1]
    mtrs2 = calcTauNC(calc_extII)
    mtr_sp_extII[i] = mtrs2[0]
    mtr_ps_extII[i] = mtrs2[1]
#    (mtr_sp_biden(i), mtr_ps_biden(i)) = calcTauNC(calc_biden)

# Update policy CSVs with MTRs
pols_base = pd.read_csv('policy_baseline.csv')
pols_extII = pd.read_csv('policy_extendII.csv')
pols_extAll = pd.read_csv('policy_extendAll.csv')
#pols_biden = pd.read_csv('policy_biden.csv')

pols_base['taxrt_scorp'] = mtr_ps_base
pols_base['taxrt_soleprop'] = mtr_sp_base
pols_base['taxrt_partner'] = mtr_ps_base
pols_base.to_csv('policy_baseline.csv', index=False)

pols_extII['taxrt_scorp'] = mtr_ps_extII
pols_extII['taxrt_soleprop'] = mtr_sp_extII
pols_extII['taxrt_partner'] = mtr_ps_extII
pols_extII.to_csv('policy_extendII.csv', index=False)

pols_extAll['taxrt_scorp'] = mtr_ps_extII
pols_extAll['taxrt_soleprop'] = mtr_sp_extII
pols_extAll['taxrt_partner'] = mtr_ps_extII
pols_extAll.to_csv('policy_extendAll.csv', index=False)

#pols_biden['taxrt_scorp'] = mtr_ps_biden
#pols_biden['taxrt_soleprop'] = mtr_sp_biden
#pols_biden['taxrt_partner'] = mtr_ps_biden
#pols_biden.to_csv('policy_biden.csv')


