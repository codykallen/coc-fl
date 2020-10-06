# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 13:28:09 2020

@author: cody_
"""

import os
os.chdir('C:/Users/cody_/Documents/GitHub/coc-fl')
import numpy as np
import pandas as pd
from config import OUTPUTPATH
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

def DonutFacts(calc):
    """
    Want to compute the following for the given Calculator:
        - The share of people (head + spouse) with W2 income affected by the donut hole. 
        - The share of W2 income affected by the donut hole. 
        - The share of sole proprietorship and S corporation income affected by the donut hole. 
    """
    wgt = calc.array('s006')
    # W2 income
    gross_was_p = calc.array('e00200p') + calc.array('pencon_p')
    gross_was_s = calc.array('e00200s') + calc.array('pencon_s')
    # Self-employment income
    sey_p = calc.array('e00900p') + calc.array('e02100p') + calc.array('k1bx14p')
    sey_s = calc.array('e00900s') + calc.array('e02100s') + calc.array('k1bx14s')
    # Amount of income subject to donut hole
    sey_frac = 1.0 - 0.5 * calc.policy_param('FICA_ss_trt')
    was_plus_sey_p = gross_was_p + np.maximum(0., sey_p * sey_frac)
    was_plus_sey_s = gross_was_s + np.maximum(0., sey_s * sey_frac)
    donuthit_p = np.maximum(0., was_plus_sey_p - calc.policy_param('SS_Earnings_thd'))
    donuthit_s = np.maximum(0., was_plus_sey_s - calc.policy_param('SS_Earnings_thd'))
    w2_p_over = np.minimum(donuthit_p, gross_was_p)
    w2_s_over = np.minimum(donuthit_s, gross_was_s)
    sey_p_over = np.maximum(np.minimum(donuthit_p, sey_p), 0.)
    sey_s_over = np.maximum(np.minimum(donuthit_s, sey_s), 0.)
    # Indicators
    scorp = calc.array('e26270') - calc.array('k1bx14p') - calc.array('k1bx14s')
    employee_p = np.where(gross_was_p > 0, 1, 0)
    employee_s = np.where(gross_was_s > 0, 1, 0)
    entrepreneur_p = np.where(sey_p + scorp != 0.0, 1, 0)
    entrepreneur_s = np.where(sey_s != 0.0, 1, 0)
    affected_p = np.where(donuthit_p > 0, 1, 0)
    affected_s = np.where(donuthit_s > 0, 1, 0)
    # Share of employees affected
    stat1 = sum((employee_p * affected_p + employee_s * affected_s) * wgt) / sum((employee_p + employee_s) * wgt)
    # Share of W2 income affected
    stat2 = sum((employee_p * affected_p * w2_p_over + employee_s * affected_s * w2_s_over) * wgt) / sum((employee_p * gross_was_p + employee_s * gross_was_s) * wgt)
    # Share of entrepreneurs affected
    stat3 = sum((entrepreneur_p * affected_p + entrepreneur_s * affected_s) * wgt) / sum((entrepreneur_p + entrepreneur_s) * wgt)
    # Share of entrepreneur income affected
    stat4 = sum((entrepreneur_p * affected_p * sey_p_over + entrepreneur_s * affected_s * sey_s_over) * wgt) / sum((entrepreneur_p * (sey_p + scorp) + entrepreneur_s * sey_s) * wgt)
    return (stat1, stat2, stat3, stat4)

def interestingComparison(calc1, calc2):
    """
    Want to compute the following results for calc2 relative to calc1:
        - The number of filers with pass-through business income facing tax hikes.
        - The share of pass-through business income held by filers facing tax hikes.
    """
    wgt = calc1.array('s006')
    tax1 = calc1.array('combined')
    tax2 = calc2.array('combined')
    # Entrepreneurial income
    sp_income = calc1.array('e00900p') + calc1.array('e00900s')
    pa_income = calc1.array('k1bx14p') + calc1.array('k1bx14s')
    sc_income = calc1.array('e26270') - pa_income
    fa_income = calc1.array('e02100p') + calc1.array('e02100s')
    pt_income = sp_income + pa_income + sc_income + fa_income
    exp_income = calc1.array('expanded_income')
    # Indicators
    has_ptinc = np.where(pt_income != 0.0, 1, 0)
    tax_hike = np.where(tax2 > tax1, 1, 0)
    # Compute relevant statistics
    stat1 = sum(tax_hike * wgt) / sum(wgt)
    stat2 = sum(tax_hike * exp_income * wgt) / sum(exp_income * wgt)
    stat3 = sum(has_ptinc * tax_hike * wgt) / sum(has_ptinc * wgt)
    stat4 = sum(pt_income * tax_hike * wgt) / sum(pt_income * wgt)
    return (stat1, stat2, stat3, stat4)



# Create baseline
calc_base = make_calculator(None, 2020)

# Version with extension of II tax policies
param_extII = Calculator.read_json_param_objects('JSONs/extendII.json', None)
calc_extII = make_calculator(param_extII['policy'], 2020)

# Version with Biden plan
param_biden = Calculator.read_json_param_objects('JSONs/biden.json', None)
calc_biden = make_calculator(param_biden['policy'], 2020)


emp_af = np.zeros(10)
wsi_af = np.zeros(10)
ent_af = np.zeros(10)
pti_af = np.zeros(10)
all_hike1 = np.zeros(10)
all_hike2 = np.zeros(10)
pt_hike1 = np.zeros(10)
pt_hike2 = np.zeros(10)

for i in range(10):
    calc_extII.increment_year()
    calc_extII.calc_all()
    calc_biden.increment_year()
    calc_biden.calc_all()
    (emp_af[i], wsi_af[i], ent_af[i], pti_af[i]) = DonutFacts(calc_biden)
    (all_hike1[i], all_hike2[i], pt_hike1[i], pt_hike2[i]) = interestingComparison(calc_extII, calc_biden)
    
df1 = pd.DataFrame({'Year': range(2021, 2031),
                    'Employees': emp_af, 'W2 income': wsi_af,
                    'Self-employed': ent_af, 'Self-employment income': pti_af,
                    'All % of filers': all_hike1, 'All % of income': all_hike2,
                    'PT % of filers': pt_hike1, 'PT % of income': pt_hike2})
df1.to_csv(OUTPUTPATH + 'main/other-taxcalc.csv', index=False)



