import copy
import numpy as np
import pandas as pd
from config import *


class Parameter():
    """
    Parameter class.

    Reads in environment parameters and stores them.
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        self.set_chosen_parms()
        self.read_depr()
        self.read_debt()
        self.read_sec179()
        self.read_foreign()
    
    def set_chosen_parms(self):
        """
        Set certain parameters we can choose (may update to differ over time)
        """
        # Nominal risk-free rate
        self.rf = 0.025
        # Expected inflation rate
        self.pi = 0.02
        # Bond premium
        self.premD = 0.023
        # Equity premium
        self.premE = 0.05
        # Required return on debt
        self.rd = self.rf + self.premD
        # Required return on equity
        self.re = self.rf + self.premE
        # Set shares for distribution of of investment income
        self.shares = {'txshr_d_c': 0.523, # taxable share of corporate debt
                       'txshr_d_nc': 0.763, # taxable share of pass-through debt
                       'txshr_e': 0.572, # taxable share of corporate equity
                       'divshr': 0.44, # dividend payout share
                       'wt_scg': 0.034, # share of capital gains realized short-term
                       'wt_lcg': 0.496, # share of capital gains realized long-term
                       'h_lcg': 10.0, # holding period for long-term gains
                       'h_xcg': 30.0} # holding period for gains held until death
        assert self.shares['wt_scg'] + self.shares['wt_lcg'] <= 1.0
        
    def read_depr(self):
        """
        Read in economic depreciation rates by asset type.
        Source: Cost-of-Capital-Calculator
        """
        depr1 = pd.read_csv(INPUTPATH + 'economic_depreciation_rates.csv')
        depr1.drop(['Asset'], axis=1, inplace=True)
        # Drop unwanted categories
        depr1.drop([28, 36, 56, 89, 90, 97, 98], axis=0, inplace=True)
        depr1.rename({'Code': 'asset', 'Economic Depreciation Rate': 'delta'}, axis=1, inplace=True)
        depr1.set_index('asset', inplace=True)
        self.deltas = copy.deepcopy(depr1)
        
    def read_debt(self):
        """
        Read in debt financing share by industry and firm type
        Source: CBO internal
        """
        debtfile = pd.read_csv(INPUTPATH + 'debt_financing.csv')
        debtfile.set_index('indcode', inplace=True)
        self.Deltas = copy.deepcopy(debtfile)
        
    def read_sec179(self):
        """
        Read in section 179 eligibility rates (effective) by asset type
        """
        s179file = pd.read_csv(INPUTPATH + 'sec179use.csv')
        s179file.set_index('asset', inplace=True)
        self.s179 = copy.deepcopy(s179file)
    
    def read_foreign(self):
        """
        Read in foreign tax rates and asset information.
        """
        ffile = pd.read_csv(INPUTPATH + 'international-by-industry.csv')
        ffile.set_index('indcode', inplace=True)
        self.foreign = copy.deepcopy(ffile)


