import copy
import pandas as pd
from config import INPUTPATH


class Parameter():
    """
    Parameter class.

    Reads in environment parameters and stores them.
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, altparms=None):
        self.set_chosen_parms()
        if altparms is not None:
            self.update_parms(altparms)
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
        # Income rate including supernormal returns
        self.p = 0.2
        # Set shares for distribution of of investment income
        self.shares = {'txshr_d_c': 0.523, # taxable share of corporate debt
                       'txshr_d_nc': 0.763, # taxable share of pass-through debt
                       'txshr_e': 0.572, # taxable share of corporate equity
                       'divshr': 0.44, # dividend payout share
                       'wt_scg': 0.034, # share of capital gains realized short-term
                       'wt_lcg': 0.496, # share of capital gains realized long-term
                       'h_lcg': 10.0, # holding period for long-term gains
                       'h_xcg': 30.0} # holding period for gains held until death
        # Set state-level tax rates
        self.sltaxes = {'int': 0.0413, 'ndiv': 0.0421, 'qdiv': 0.0479,
                        'scg': 0.0457, 'lcg': 0.0467,
                        'soleprop': 0.0389, 'partner': 0.0497,
                        'property': 0.0125, 'corp': 0.05}
        # Bool for whether to include state and local taxes
        self.include_slt = True
        # Bool for whether equations are forward-looking
        self.forwardLooking = False
    
    def update_parms(self, pdict):
        """
        Function to update certain parameters.
        """
        # Check that pdict is acceptable.
        assert type(pdict) is dict
        for parm in pdict:
            assert parm in ['rf', 'pi', 'premD', 'premE', 'rd', 're', 'p',
                            'shares', 'sltaxes',
                            'include_slt', 'forwardLooking']
        # Check values and update baseic economic parameters
        if 'rf' in pdict:
            assert pdict['rf'] > 0
            self.rf = pdict['rf']
        if 'pi' in pdict:
            assert pdict['pi'] > -self.rf
            self.pi = pdict['pi']
        if 'premD' in pdict:
            assert pdict['premD'] > 0
            self.premD = pdict['premD']
            self.rd = self.rf + self.premD
        if 'premE' in pdict:
            assert pdict['premE'] > 0
            self.premE = pdict['premE']
        if 'rd' in pdict:
            assert pdict['rd'] > 0
            self.rd = pdict['rd']
        if 're' in pdict:
            assert pdict['re'] > 0
            self.re = pdict['re']
        if 'p' in pdict:
            assert pdict['p'] > 0
            self.p = pdict['p']
        # Update assumptions for equation style
        if 'include_slt' in pdict:
            assert type(pdict['include_slt']) is bool
            self.include_slt = pdict['include_slt']
        if 'forwardLooking' in pdict:
            assert type(pdict['forwardLooking']) is bool
            self.forwardLooking = pdict['forwardLooking']
        # Update dictionaries
        if 'shares' in pdict:
            assert type(pdict['shares']) is dict
            for elem in pdict['shares']:
                self.shares[elem] = pdict['shares'][elem]
        if 'sltaxes' in pdict:
            assert type(pdict['sltaxes']) is dict
            for elem in pdict['sltaxes']:
                self.sltaxes[elem] = pdict['sltaxes'][elem]
        # Check that new parameters in dictionaries are acceptable
        assert self.shares['txshr_d_c'] >= 0 and self.shares['txshr_d_c'] <= 1
        assert self.shares['txshr_d_nc'] >= 0 and self.shares['txshr_d_nc'] <= 1
        assert self.shares['txshr_e'] >= 0 and self.shares['txshr_e'] <= 1
        assert self.shares['divshr'] >= 0 and self.shares['divshr'] <= 1
        assert self.shares['wt_scg'] >= 0 and self.shares['wt_scg'] <= 1
        assert self.shares['wt_lcg'] >= 0 and self.shares['wt_lcg'] <= 1
        assert self.shares['wt_scg'] + self.shares['wt_lcg'] <= 1
        assert self.shares['h_lcg'] >= 0
        assert self.shares['h_xcg'] >= 0
        for inctype in self.sltaxes:
            assert self.sltaxes[inctype] >= 0 and self.sltaxes[inctype] <= 1
        
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


