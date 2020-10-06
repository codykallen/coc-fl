# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 07:36:10 2020

@author: cody_
"""

import os
os.chdir('C:/Users/cody_/Documents/GitHub/coc-fl')
import numpy as np
import pandas as pd
from tclocal import Policy, Records, Calculator

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

def calcTauInv(calc):
    """
    Calculates the effective marginal tax rate on each type of investment
    income.
    """
    wgt = calc.array('s006')
    # Interest income
    inc1 = np.abs(calc.array('e00300'))
    mtr1 = calc.mtr('e00300', calc_all_already_called=True)[2]
    wmtr_int = sum(mtr1 * inc1 * wgt) / sum(inc1 * wgt)
    # Dividend income
    inc2 = np.abs(calc.array('e00650'))
    inc3 = np.abs(calc.array('e00600') - inc2)
    mtr2 = calc.mtr('e00650', calc_all_already_called=True)[2]
    mtr3 = calc.mtr('e00600', calc_all_already_called=True)[2]
    wmtr_div = sum((mtr2 * inc2 + mtr3 * inc3) * wgt) / sum((inc2 + inc3) * wgt)
    # Short-term capital gains
    inc4 = np.maximum(calc.array('p22250'), 0.)
    mtr4 = calc.mtr('p22250', calc_all_already_called=True)[2]
    wmtr_scg = sum(mtr4 * inc4 * wgt) / sum(inc4 * wgt)
    # Long-term capital gains
    inc5 = np.maximum(calc.array('p23250'), 0.)
    mtr5 = calc.mtr('p23250', calc_all_already_called=True)[2]
    wmtr_lcg = sum(mtr5 * inc5 * wgt) / sum(inc5 * wgt)
    return (wmtr_int, wmtr_div, wmtr_scg, wmtr_lcg)

def calcSubSLTax(calc):
    """
    Calculates the marginal federal tax subsidies from the deductibility of
    state and local income and property taxes.
    """
    wgt = calc.array('s006')
    taxi = calc.array('e18400')
    taxp = calc.array('e18500')
    mtri = calc.mtr('e18400', calc_all_already_called=True)[2]
    mtrp = calc.mtr('e18500', calc_all_already_called=True)[2]
    wsubi = -sum(mtri * taxi * wgt) / sum(taxi * wgt)
    wsubp = -sum(mtrp * taxp * wgt) / sum(taxp * wgt)
    return (wsubi, wsubp)


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
mtr_int_base = np.zeros(10)
mtr_div_base = np.zeros(10)
mtr_scg_base = np.zeros(10)
mtr_lcg_base = np.zeros(10)
sub_slti_base = np.zeros(10)

mtr_sp_extII = np.zeros(10)
mtr_pa_extII = np.zeros(10)
mtr_sc_extII = np.zeros(10)
mtr_int_extII = np.zeros(10)
mtr_div_extII = np.zeros(10)
mtr_scg_extII = np.zeros(10)
mtr_lcg_extII = np.zeros(10)
sub_slti_extII = np.zeros(10)

mtr_sp_biden = np.zeros(10)
mtr_pa_biden = np.zeros(10)
mtr_sc_biden = np.zeros(10)
mtr_int_biden = np.zeros(10)
mtr_div_biden = np.zeros(10)
mtr_scg_biden = np.zeros(10)
mtr_lcg_biden = np.zeros(10)
sub_slti_biden = np.zeros(10)

for i in range(10):
    # Advance each Calculator
    calc_base.increment_year()
    calc_base.calc_all()
    calc_extII.increment_year()
    calc_extII.calc_all()
    calc_biden.increment_year()
    calc_biden.calc_all()
    # Compute and save MTRs on pass-through business income
    mtrb1 = calcTauNC(calc_base)
    mtr_sp_base[i] = mtrb1[0]
    mtr_pa_base[i] = mtrb1[1]
    mtr_sc_base[i] = mtrb1[2]
    mtrb2 = calcTauNC(calc_extII)
    mtr_sp_extII[i] = mtrb2[0]
    mtr_pa_extII[i] = mtrb2[1]
    mtr_sc_extII[i] = mtrb2[2]
    mtrb3 = calcTauNC(calc_biden)
    mtr_sp_biden[i] = mtrb3[0]
    mtr_pa_biden[i] = mtrb3[1]
    mtr_sc_biden[i] = mtrb3[2]
    # Compute and save MTRs on investment income
    mtri1 = calcTauInv(calc_base)
    mtr_int_base[i] = mtri1[0]
    mtr_div_base[i] = mtri1[1]
    mtr_scg_base[i] = mtri1[2]
    mtr_lcg_base[i] = mtri1[3]
    mtri2 = calcTauInv(calc_extII)
    mtr_int_extII[i] = mtri2[0]
    mtr_div_extII[i] = mtri2[1]
    mtr_scg_extII[i] = mtri2[2]
    mtr_lcg_extII[i] = mtri2[3]
    mtri3 = calcTauInv(calc_biden)
    mtr_int_biden[i] = mtri3[0]
    mtr_div_biden[i] = mtri3[1]
    mtr_scg_biden[i] = mtri3[2]
    mtr_lcg_biden[i] = mtri3[3]
    # Compute and save marginal subsidies on state and local taxes
    sub1 = calcSubSLTax(calc_base)
    sub_slti_base[i] = sub1[0]
    sub2 = calcSubSLTax(calc_extII)
    sub_slti_extII[i] = sub2[0]
    sub3 = calcSubSLTax(calc_biden)
    sub_slti_biden[i] = sub3[0]
    

# Update policy CSVs with MTRs
pols_clbase = pd.read_csv('policy_baseline.csv')
pols_extII = pd.read_csv('policy_extendII.csv')
pols_cpbase = pd.read_csv('policy_currentPolicy.csv')
pols_biden = pd.read_csv('policy_biden.csv')

pols_clbase['taxrt_scorp'] = mtr_sc_base
pols_clbase['taxrt_soleprop'] = mtr_sp_base
pols_clbase['taxrt_partner'] = mtr_pa_base
pols_clbase['taxrt_int'] = mtr_int_base
pols_clbase['taxrt_div'] = mtr_div_base
pols_clbase['taxrt_scg'] = mtr_scg_base
pols_clbase['taxrt_lcg'] = mtr_lcg_base
pols_clbase['sub_slti'] = sub_slti_base
pols_clbase.to_csv('policy_baseline.csv', index=False)

pols_extII['taxrt_scorp'] = mtr_sc_extII
pols_extII['taxrt_soleprop'] = mtr_sp_extII
pols_extII['taxrt_partner'] = mtr_pa_extII
pols_extII['taxrt_int'] = mtr_int_extII
pols_extII['taxrt_div'] = mtr_div_extII
pols_extII['taxrt_scg'] = mtr_scg_extII
pols_extII['taxrt_lcg'] = mtr_lcg_extII
pols_extII['sub_slti'] = sub_slti_extII
pols_extII.to_csv('policy_extendII.csv', index=False)

pols_cpbase['taxrt_scorp'] = mtr_sc_extII
pols_cpbase['taxrt_soleprop'] = mtr_sp_extII
pols_cpbase['taxrt_partner'] = mtr_pa_extII
pols_cpbase['taxrt_int'] = mtr_int_extII
pols_cpbase['taxrt_div'] = mtr_div_extII
pols_cpbase['taxrt_scg'] = mtr_scg_extII
pols_cpbase['taxrt_lcg'] = mtr_lcg_extII
pols_cpbase['sub_slti'] = sub_slti_extII
pols_cpbase.to_csv('policy_currentPolicy.csv', index=False)

pols_biden['taxrt_scorp'] = mtr_sc_biden
pols_biden['taxrt_soleprop'] = mtr_sp_biden
pols_biden['taxrt_partner'] = mtr_pa_biden
pols_biden['taxrt_int'] = mtr_int_biden
pols_biden['taxrt_div'] = mtr_div_biden
pols_biden['taxrt_scg'] = mtr_scg_biden
pols_biden['taxrt_lcg'] = mtr_lcg_biden
pols_biden['sub_slti'] = sub_slti_biden
pols_biden.to_csv('policy_biden.csv', index=False)


