# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 07:36:10 2020

@author: cody_
"""

import os
os.chdir('C:/Users/cody_/Documents/GitHub/coc-fl')
import numpy as np
import pandas as pd
import tclocal
from tclocal import *

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
    wgt = calc.array('s006')
    # Sole proprietorships
    inc1 = np.abs(calc.array('e00900'))
    mtr1 = calc.mtr('e00900p', calc_all_already_called=True)[2]
    wmtr1 = sum(mtr1 * inc1 * wgt) / sum(inc1 * wgt)
    # Partnerships
    inc2 = np.abs(calc.array('k1bx14p') + calc.array('k1bx14s'))
    mtr2 = calc.mtr('k1bx14p', calc_all_already_called=True)[2]
    wmtr2 = sum(mtr2 * inc2 * wgt) / sum(inc2 * wgt)
    # S corporations, active and passive
    inc3 = np.abs(calc.array('e26270'))
    inc4 = np.abs(calc.array('e02000') - calc.array('e26270'))
    mtr3 = calc.mtr('e26270', calc_all_already_called=True)[2]
    mtr4 = calc.mtr('e02000', calc_all_already_called=True)[2]
    wmtr3 = sum((mtr3 * inc3 + mtr4 * inc4) * wgt) / sum((inc3 + inc4) * wgt)
    return (wmtr1, wmtr2, wmtr3)


# Create baseline
calc_base = make_calculator(None, 2019)

# Version with extension of II tax policies
param_extII = Calculator.read_json_param_objects('JSONs/extendII.json', None)
calc_extII = make_calculator(param_extII['policy'], 2019)

# Version with Biden plan
param_biden = Calculator.read_json_param_objects('JSONs/biden.json', None)
calc_biden = make_calculator(param_biden['policy'], 2019)

# Compute relevant MTRs for each year
mtr_sp_base = np.zeros(10)
mtr_pa_base = np.zeros(10)
mtr_sc_base = np.zeros(10)
mtr_sp_extII = np.zeros(10)
mtr_pa_extII = np.zeros(10)
mtr_sc_extII = np.zeros(10)
mtr_sp_biden = np.zeros(10)
mtr_pa_biden = np.zeros(10)
mtr_sc_biden = np.zeros(10)

for i in range(10):
    # Advance each Calculator
    calc_base.increment_year()
    calc_base.calc_all()
    calc_extII.increment_year()
    calc_extII.calc_all()
    calc_biden.increment_year()
    calc_biden.calc_all()
    # Compute and save MTRs
    mtrs1 = calcTauNC(calc_base)
    mtr_sp_base[i] = mtrs1[0]
    mtr_pa_base[i] = mtrs1[1]
    mtr_sc_base[i] = mtrs1[2]
    mtrs2 = calcTauNC(calc_extII)
    mtr_sp_extII[i] = mtrs2[0]
    mtr_pa_extII[i] = mtrs2[1]
    mtr_sc_extII[i] = mtrs2[2]
    mtrs3 = calcTauNC(calc_biden)
    mtr_sp_biden[i] = mtrs3[0]
    mtr_pa_biden[i] = mtrs3[1]
    mtr_sc_biden[i] = mtrs3[2]

# Update policy CSVs with MTRs
pols_base = pd.read_csv('policy_baseline.csv')
pols_extII = pd.read_csv('policy_extendII.csv')
pols_extAll = pd.read_csv('policy_extendAll.csv')
pols_biden = pd.read_csv('policy_biden.csv')

pols_base['taxrt_scorp'] = mtr_sc_base
pols_base['taxrt_soleprop'] = mtr_sp_base
pols_base['taxrt_partner'] = mtr_pa_base
pols_base.to_csv('policy_baseline.csv', index=False)

pols_extII['taxrt_scorp'] = mtr_sc_extII
pols_extII['taxrt_soleprop'] = mtr_sp_extII
pols_extII['taxrt_partner'] = mtr_pa_extII
pols_extII.to_csv('policy_extendII.csv', index=False)

pols_extAll['taxrt_scorp'] = mtr_sc_extII
pols_extAll['taxrt_soleprop'] = mtr_sp_extII
pols_extAll['taxrt_partner'] = mtr_pa_extII
pols_extAll.to_csv('policy_extendAll.csv', index=False)

pols_biden['taxrt_scorp'] = mtr_sc_biden
pols_biden['taxrt_soleprop'] = mtr_sp_biden
pols_biden['taxrt_partner'] = mtr_pa_biden
pols_biden.to_csv('policy_biden.csv', index=False)


