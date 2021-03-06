import copy
import numpy as np
import pandas as pd
from config import (INPUTPATH, OUTPUTPATH, ast_codes, ind_codes,
                    catlist, ntype, nind)

class OutputBuilder():
    """
    OutputBuilder class.

    Saves results and tabulates (to be done).
    """

    def __init__(self, calc, key, weighting='stock'):
        """
            parm: Parameter class object
            pol: Policy class object
        """
        # Store Calculator object
        assert calc.calc_all_called
        self.calc = copy.deepcopy(calc)
        # Read in asset data
        if weighting is not None:
            assert weighting in ['stock', 'investment']
            self.weighting = weighting
        else:
            self.weighting = 'stock'
        self.read_assets()
        assert type(key) is str
        self.key = key
        
    def read_assets(self):
        """
        Read in asset data by asset type, industry and firm type.
        """
        if self.weighting == 'stock':
            fpath = OUTPUTPATH + 'capital/stock_'
        else:
            fpath = OUTPUTPATH + 'capital/inv_'
        self.stock_ccorp = pd.read_csv(fpath + 'ccorp.csv',
                                       index_col='asset').fillna(value = 0)
        self.stock_scorp = pd.read_csv(fpath + 'scorp.csv',
                                       index_col='asset').fillna(value = 0)
        self.stock_soleprop = pd.read_csv(fpath + 'soleprop.csv',
                                          index_col='asset').fillna(value = 0)
        self.stock_partner = pd.read_csv(fpath + 'partner.csv',
                                         index_col='asset').fillna(value = 0)
    
    def store_raw(self, year):
        """
        Store output from Calculator for the given year.
        """
        assert str(year) in list(self.calc.results_coc)
        # Convert result arrays to DataFrames
        df_corp1 = pd.DataFrame(self.calc.results_coc[str(year)]['corp'],
                                index=ast_codes, columns=ind_codes)
        df_scorp1 = pd.DataFrame(self.calc.results_coc[str(year)]['scorp'],
                                 index=ast_codes, columns=ind_codes)
        df_soleprop1 = pd.DataFrame(self.calc.results_coc[str(year)]['soleprop'],
                                    index=ast_codes, columns=ind_codes)
        df_partner1 = pd.DataFrame(self.calc.results_coc[str(year)]['partner'],
                                   index=ast_codes, columns=ind_codes)
        df_corp2 = pd.DataFrame(self.calc.results_metr[str(year)]['corp'],
                                index=ast_codes, columns=ind_codes)
        df_scorp2 = pd.DataFrame(self.calc.results_metr[str(year)]['scorp'],
                                 index=ast_codes, columns=ind_codes)
        df_soleprop2 = pd.DataFrame(self.calc.results_metr[str(year)]['soleprop'],
                                    index=ast_codes, columns=ind_codes)
        df_partner2 = pd.DataFrame(self.calc.results_metr[str(year)]['partner'],
                                   index=ast_codes, columns=ind_codes)
        # Save results to CSV files
        fileend = self.key + '_' + str(year) + '.csv'
        df_corp1.to_csv(OUTPUTPATH + 'raw/coc_corp_' + fileend)
        df_scorp1.to_csv(OUTPUTPATH + 'raw/coc_scorp_' + fileend)
        df_soleprop1.to_csv(OUTPUTPATH + 'raw/coc_soleprop_' + fileend)
        df_partner1.to_csv(OUTPUTPATH + 'raw/coc_partner_' + fileend)
        df_corp2.to_csv(OUTPUTPATH + 'raw/metr_corp_' + fileend)
        df_scorp2.to_csv(OUTPUTPATH + 'raw/metr_scorp_' + fileend)
        df_soleprop2.to_csv(OUTPUTPATH + 'raw/metr_soleprop_' + fileend)
        df_partner2.to_csv(OUTPUTPATH + 'raw/metr_partner_' + fileend)
    
    def tabulate_industry(self, year):
        """
        Compute weighted averags of various measures by industry
        for the given year.
        """
        assert str(year) in list(self.calc.results_coc)
        # Extract asset weights
        stock_ccorp_arr = self.stock_ccorp.to_numpy()
        stock_scorp_arr = self.stock_scorp.to_numpy()
        stock_soleprop_arr = self.stock_soleprop.to_numpy()
        stock_partner_arr = self.stock_partner.to_numpy()
        # Extract results by firm type
        coc_ccorp = self.calc.results_coc[str(year)]['corp']
        coc_scorp = self.calc.results_coc[str(year)]['scorp']
        coc_soleprop = self.calc.results_coc[str(year)]['soleprop']
        coc_partner = self.calc.results_coc[str(year)]['partner']
        mtr_ccorp = self.calc.results_metr[str(year)]['corp']
        mtr_scorp = self.calc.results_metr[str(year)]['scorp']
        mtr_soleprop = self.calc.results_metr[str(year)]['soleprop']
        mtr_partner = self.calc.results_metr[str(year)]['partner']
        mettr_ccorp = self.calc.results_mettr[str(year)]['corp']
        mettr_scorp = self.calc.results_mettr[str(year)]['scorp']
        mettr_soleprop = self.calc.results_mettr[str(year)]['soleprop']
        mettr_partner = self.calc.results_mettr[str(year)]['partner']
        ucoc_ccorp = self.calc.results_ucoc[str(year)]['corp']
        ucoc_scorp = self.calc.results_ucoc[str(year)]['scorp']
        ucoc_soleprop = self.calc.results_ucoc[str(year)]['soleprop']
        ucoc_partner = self.calc.results_ucoc[str(year)]['partner']
        # Extract international results
        eatr_d = self.calc.results_international[str(year)]['domestic']
        eatr_f = self.calc.results_international[str(year)]['foreign']
        # Compute and store averages by industry
        coclist = ((coc_ccorp * stock_ccorp_arr
                    + coc_scorp * stock_scorp_arr
                    + coc_soleprop * stock_soleprop_arr
                    + coc_partner * stock_partner_arr).sum(0)
                   / (stock_ccorp_arr + stock_scorp_arr
                      + stock_soleprop_arr + stock_partner_arr).sum(0))
        mtrlist = ((mtr_ccorp * stock_ccorp_arr
                    + mtr_scorp * stock_scorp_arr
                    + mtr_soleprop * stock_soleprop_arr
                    + mtr_partner * stock_partner_arr).sum(0)
                   / (stock_ccorp_arr + stock_scorp_arr
                      + stock_soleprop_arr + stock_partner_arr).sum(0))
        mettrlist = ((mettr_ccorp * stock_ccorp_arr
                      + mettr_scorp * stock_scorp_arr
                      + mettr_soleprop * stock_soleprop_arr
                      + mettr_partner * stock_partner_arr).sum(0)
                     / (stock_ccorp_arr + stock_scorp_arr
                        + stock_soleprop_arr + stock_partner_arr).sum(0))
        ucoclist = ((ucoc_ccorp * stock_ccorp_arr
                     + ucoc_scorp * stock_scorp_arr
                     + ucoc_soleprop * stock_soleprop_arr
                     + ucoc_partner * stock_partner_arr).sum(0)
                    / (stock_ccorp_arr + stock_scorp_arr
                       + stock_soleprop_arr + stock_partner_arr).sum(0))
        eatrdlist = (eatr_d * stock_ccorp_arr).sum(0)/ stock_ccorp_arr.sum(0)
        eatrflist = (eatr_f * stock_ccorp_arr).sum(0)/ stock_ccorp_arr.sum(0)
        # Combine into dataframe and save
        indnames = pd.read_csv(INPUTPATH + 'industries.csv')
        data1 = pd.DataFrame({'Industry code': ind_codes,
                              'Industry': indnames['industry name'],
                              'Cost of capital': coclist,
                              'User cost of capital': ucoclist,
                              'METR': mtrlist, 'METTR': mettrlist,
                              'Domestic EATR': eatrdlist,
                              'Foreign EATR': eatrflist})
        data1.to_csv(OUTPUTPATH + 'raw/' + 'byIndustry_' + self.key + '_'
                     + str(year) + '.csv', index=False)
    
    def tabulate_asset(self, year):
        """
        Compute weighted averages of various measures by asset type
        for the given year.
        """
        assert str(year) in list(self.calc.results_coc)
        # Extract asset weights
        stock_ccorp_arr = self.stock_ccorp.to_numpy()
        stock_scorp_arr = self.stock_scorp.to_numpy()
        stock_soleprop_arr = self.stock_soleprop.to_numpy()
        stock_partner_arr = self.stock_partner.to_numpy()
        # Extract results by firm type
        coc_ccorp = self.calc.results_coc[str(year)]['corp']
        coc_scorp = self.calc.results_coc[str(year)]['scorp']
        coc_soleprop = self.calc.results_coc[str(year)]['soleprop']
        coc_partner = self.calc.results_coc[str(year)]['partner']
        mtr_ccorp = self.calc.results_metr[str(year)]['corp']
        mtr_scorp = self.calc.results_metr[str(year)]['scorp']
        mtr_soleprop = self.calc.results_metr[str(year)]['soleprop']
        mtr_partner = self.calc.results_metr[str(year)]['partner']
        mettr_ccorp = self.calc.results_mettr[str(year)]['corp']
        mettr_scorp = self.calc.results_mettr[str(year)]['scorp']
        mettr_soleprop = self.calc.results_mettr[str(year)]['soleprop']
        mettr_partner = self.calc.results_mettr[str(year)]['partner']
        ucoc_ccorp = self.calc.results_ucoc[str(year)]['corp']
        ucoc_scorp = self.calc.results_ucoc[str(year)]['scorp']
        ucoc_soleprop = self.calc.results_ucoc[str(year)]['soleprop']
        ucoc_partner = self.calc.results_ucoc[str(year)]['partner']
        # Extract international results
        eatr_d = self.calc.results_international[str(year)]['domestic']
        eatr_f = self.calc.results_international[str(year)]['foreign']
        # Compute and store averages by asset type
        coclist = ((coc_ccorp * stock_ccorp_arr
                    + coc_scorp * stock_scorp_arr
                    + coc_soleprop * stock_soleprop_arr
                    + coc_partner * stock_partner_arr).sum(1)
                   / (stock_ccorp_arr + stock_scorp_arr
                      + stock_soleprop_arr + stock_partner_arr).sum(1))
        mtrlist = ((mtr_ccorp * stock_ccorp_arr
                    + mtr_scorp * stock_scorp_arr
                    + mtr_soleprop * stock_soleprop_arr
                    + mtr_partner * stock_partner_arr).sum(1)
                   / (stock_ccorp_arr + stock_scorp_arr
                      + stock_soleprop_arr + stock_partner_arr).sum(1))
        mettrlist = ((mettr_ccorp * stock_ccorp_arr
                      + mettr_scorp * stock_scorp_arr
                      + mettr_soleprop * stock_soleprop_arr
                      + mettr_partner * stock_partner_arr).sum(1)
                     / (stock_ccorp_arr + stock_scorp_arr
                        + stock_soleprop_arr + stock_partner_arr).sum(1))
        ucoclist = ((ucoc_ccorp * stock_ccorp_arr
                     + ucoc_scorp * stock_scorp_arr
                     + ucoc_soleprop * stock_soleprop_arr
                     + ucoc_partner * stock_partner_arr).sum(1)
                    / (stock_ccorp_arr + stock_scorp_arr
                       + stock_soleprop_arr + stock_partner_arr).sum(1))
        eatrdlist = (eatr_d * stock_ccorp_arr).sum(1)/ stock_ccorp_arr.sum(1)
        eatrflist = (eatr_f * stock_ccorp_arr).sum(1)/ stock_ccorp_arr.sum(1)
        # Combine into dataframe and save
        astnames = pd.read_csv(INPUTPATH + 'assettypes.csv')
        data1 = pd.DataFrame({'Asset code': ast_codes,
                              'Asset': astnames['asset name'],
                              'Cost of capital': coclist,
                              'User cost of capital': ucoclist,
                              'METR': mtrlist, 'METTR': mettrlist,
                              'Domestic EATR': eatrdlist,
                              'Foreign EATR': eatrflist})
        data1.to_csv(OUTPUTPATH + 'raw/' + 'byAssetType_' + self.key + '_'
                     + str(year) + '.csv', index=False)
    
    def tabulate_main(self, year):
        """
        Compute weighted averages of various measures for:
            All
            C corporations
            S corporations
            Sole proprietorships
            Partnerships
            Equipment
            Structures
            Rental residential
            Intellectual property
        """
        assert str(year) in list(self.calc.results_coc)
        # Extract asset weights
        stock_ccorp_arr = self.stock_ccorp.to_numpy()
        stock_scorp_arr = self.stock_scorp.to_numpy()
        stock_soleprop_arr = self.stock_soleprop.to_numpy()
        stock_partner_arr = self.stock_partner.to_numpy()
        # Extract results by firm type
        coc_ccorp = self.calc.results_coc[str(year)]['corp']
        coc_scorp = self.calc.results_coc[str(year)]['scorp']
        coc_soleprop = self.calc.results_coc[str(year)]['soleprop']
        coc_partner = self.calc.results_coc[str(year)]['partner']
        mtr_ccorp = self.calc.results_metr[str(year)]['corp']
        mtr_scorp = self.calc.results_metr[str(year)]['scorp']
        mtr_soleprop = self.calc.results_metr[str(year)]['soleprop']
        mtr_partner = self.calc.results_metr[str(year)]['partner']
        mettr_ccorp = self.calc.results_mettr[str(year)]['corp']
        mettr_scorp = self.calc.results_mettr[str(year)]['scorp']
        mettr_soleprop = self.calc.results_mettr[str(year)]['soleprop']
        mettr_partner = self.calc.results_mettr[str(year)]['partner']
        ucoc_ccorp = self.calc.results_ucoc[str(year)]['corp']
        ucoc_scorp = self.calc.results_ucoc[str(year)]['scorp']
        ucoc_soleprop = self.calc.results_ucoc[str(year)]['soleprop']
        ucoc_partner = self.calc.results_ucoc[str(year)]['partner']
        # Extract international results
        eatr_d = self.calc.results_international[str(year)]['domestic']
        eatr_f = self.calc.results_international[str(year)]['foreign']
        # Arrays for storing results
        coclist = np.zeros(9)
        mtrlist = np.zeros(9)
        mettrlist = np.zeros(9)
        ucoclist = np.zeros(9)
        eatrdlist = np.zeros(9)
        eatrflist = np.zeros(9)
        # Store average results for cost of capital
        coclist[0] = ((coc_ccorp * stock_ccorp_arr
                       + coc_scorp * stock_scorp_arr
                       + coc_soleprop * stock_soleprop_arr
                       + coc_partner * stock_partner_arr).sum()
                      / (stock_ccorp_arr + stock_scorp_arr
                         + stock_soleprop_arr + stock_partner_arr).sum())
        coclist[1] = ((coc_ccorp * stock_ccorp_arr).sum()
                      / stock_ccorp_arr.sum())
        coclist[2] = ((coc_scorp * stock_scorp_arr).sum()
                      / stock_scorp_arr.sum())
        coclist[3] = ((coc_soleprop * stock_soleprop_arr).sum()
                      / stock_soleprop_arr.sum())
        coclist[4] = ((coc_partner * stock_partner_arr).sum()
                      / stock_partner_arr.sum())
        coclist[5] = ((coc_ccorp[0:37,:] * stock_ccorp_arr[0:37,:]
                       + coc_scorp[0:37,:] * stock_scorp_arr[0:37,:]
                       + coc_soleprop[0:37,:] * stock_soleprop_arr[0:37,:]
                       + coc_partner[0:37,:] * stock_partner_arr[0:37,:]).sum()
                      / (stock_ccorp_arr[0:37,:] + stock_scorp_arr[0:37,:]
                         + stock_soleprop_arr[0:37,:]
                         + stock_partner_arr[0:37,:]).sum())
        coclist[6] = ((coc_ccorp[37:68,:] * stock_ccorp_arr[37:68,:]
                       + coc_scorp[37:68,:] * stock_scorp_arr[37:68,:]
                       + coc_soleprop[37:68,:] * stock_soleprop_arr[37:68,:]
                       + coc_partner[37:68,:] * stock_partner_arr[37:68,:]).sum()
                      / (stock_ccorp_arr[37:68] + stock_scorp_arr[37:68,:]
                         + stock_soleprop_arr[37:68,:]
                         + stock_partner_arr[37:68,:]).sum())
        coclist[7] = ((coc_ccorp[91,:] * stock_ccorp_arr[91,:]
                       + coc_scorp[91,:] * stock_scorp_arr[91,:]
                       + coc_soleprop[91,:] * stock_soleprop_arr[91,:]
                       + coc_partner[91,:] * stock_partner_arr[91,:]).sum()
                      / (stock_ccorp_arr[91,:] + stock_scorp_arr[91,:]
                         + stock_soleprop_arr[91,:]
                         + stock_partner_arr[91,:]).sum())
        coclist[8] = ((coc_ccorp[68:91,:] * stock_ccorp_arr[68:91,:]
                       + coc_scorp[68:91,:] * stock_scorp_arr[68:91,:]
                       + coc_soleprop[68:91,:] * stock_soleprop_arr[68:91,:]
                       + coc_partner[68:91,:] * stock_partner_arr[68:91,:]).sum()
                      / (stock_ccorp_arr[68:91,:] + stock_scorp_arr[68:91,:]
                         + stock_soleprop_arr[68:91,:]
                         + stock_partner_arr[68:91,:]).sum())
        # Store average results for METR
        mtrlist[0] = ((mtr_ccorp * stock_ccorp_arr
                       + mtr_scorp * stock_scorp_arr
                       + mtr_soleprop * stock_soleprop_arr
                       + mtr_partner * stock_partner_arr).sum()
                      / (stock_ccorp_arr + stock_scorp_arr
                         + stock_soleprop_arr + stock_partner_arr).sum())
        mtrlist[1] = ((mtr_ccorp * stock_ccorp_arr).sum()
                      / stock_ccorp_arr.sum())
        mtrlist[2] = ((mtr_scorp * stock_scorp_arr).sum()
                      / stock_scorp_arr.sum())
        mtrlist[3] = ((mtr_soleprop * stock_soleprop_arr).sum()
                      / stock_soleprop_arr.sum())
        mtrlist[4] = ((mtr_partner * stock_partner_arr).sum()
                      / stock_partner_arr.sum())
        mtrlist[5] = ((mtr_ccorp[0:37,:] * stock_ccorp_arr[0:37,:]
                       + mtr_scorp[0:37,:] * stock_scorp_arr[0:37,:]
                       + mtr_soleprop[0:37,:] * stock_soleprop_arr[0:37,:]
                       + mtr_partner[0:37,:] * stock_partner_arr[0:37,:]).sum()
                      / (stock_ccorp_arr[0:37,:] + stock_scorp_arr[0:37,:]
                         + stock_soleprop_arr[0:37,:]
                         + stock_partner_arr[0:37,:]).sum())
        mtrlist[6] = ((mtr_ccorp[37:68,:] * stock_ccorp_arr[37:68,:]
                       + mtr_scorp[37:68,:] * stock_scorp_arr[37:68,:]
                       + mtr_soleprop[37:68,:] * stock_soleprop_arr[37:68,:]
                       + mtr_partner[37:68,:] * stock_partner_arr[37:68,:]).sum()
                      / (stock_ccorp_arr[37:68] + stock_scorp_arr[37:68,:]
                         + stock_soleprop_arr[37:68,:]
                         + stock_partner_arr[37:68,:]).sum())
        mtrlist[7] = ((mtr_ccorp[91,:] * stock_ccorp_arr[91,:]
                       + mtr_scorp[91,:] * stock_scorp_arr[91,:]
                       + mtr_soleprop[91,:] * stock_soleprop_arr[91,:]
                       + mtr_partner[91,:] * stock_partner_arr[91,:]).sum()
                      / (stock_ccorp_arr[91,:] + stock_scorp_arr[91,:]
                         + stock_soleprop_arr[91,:]
                         + stock_partner_arr[91,:]).sum())
        mtrlist[8] = ((mtr_ccorp[68:91,:] * stock_ccorp_arr[68:91,:]
                       + mtr_scorp[68:91,:] * stock_scorp_arr[68:91,:]
                       + mtr_soleprop[68:91,:] * stock_soleprop_arr[68:91,:]
                       + mtr_partner[68:91,:] * stock_partner_arr[68:91,:]).sum()
                      / (stock_ccorp_arr[68:91,:] + stock_scorp_arr[68:91,:]
                         + stock_soleprop_arr[68:91,:]
                         + stock_partner_arr[68:91,:]).sum())
        # Store average results for METTR
        mettrlist[0] = ((mettr_ccorp * stock_ccorp_arr
                         + mettr_scorp * stock_scorp_arr
                         + mettr_soleprop * stock_soleprop_arr
                         + mettr_partner * stock_partner_arr).sum()
                        / (stock_ccorp_arr + stock_scorp_arr
                         + stock_soleprop_arr + stock_partner_arr).sum())
        mettrlist[1] = ((mettr_ccorp * stock_ccorp_arr).sum()
                        / stock_ccorp_arr.sum())
        mettrlist[2] = ((mettr_scorp * stock_scorp_arr).sum()
                        / stock_scorp_arr.sum())
        mettrlist[3] = ((mettr_soleprop * stock_soleprop_arr).sum()
                        / stock_soleprop_arr.sum())
        mettrlist[4] = ((mettr_partner * stock_partner_arr).sum()
                        / stock_partner_arr.sum())
        mettrlist[5] = ((mettr_ccorp[0:37,:] * stock_ccorp_arr[0:37,:]
                         + mettr_scorp[0:37,:] * stock_scorp_arr[0:37,:]
                         + mettr_soleprop[0:37,:] * stock_soleprop_arr[0:37,:]
                         + mettr_partner[0:37,:] * stock_partner_arr[0:37,:]).sum()
                        / (stock_ccorp_arr[0:37,:] + stock_scorp_arr[0:37,:]
                           + stock_soleprop_arr[0:37,:]
                           + stock_partner_arr[0:37,:]).sum())
        mettrlist[6] = ((mettr_ccorp[37:68,:] * stock_ccorp_arr[37:68,:]
                         + mettr_scorp[37:68,:] * stock_scorp_arr[37:68,:]
                         + mettr_soleprop[37:68,:] * stock_soleprop_arr[37:68,:]
                         + mettr_partner[37:68,:] * stock_partner_arr[37:68,:]).sum()
                        / (stock_ccorp_arr[37:68] + stock_scorp_arr[37:68,:]
                           + stock_soleprop_arr[37:68,:]
                           + stock_partner_arr[37:68,:]).sum())
        mettrlist[7] = ((mettr_ccorp[91,:] * stock_ccorp_arr[91,:]
                         + mettr_scorp[91,:] * stock_scorp_arr[91,:]
                         + mettr_soleprop[91,:] * stock_soleprop_arr[91,:]
                         + mettr_partner[91,:] * stock_partner_arr[91,:]).sum()
                        / (stock_ccorp_arr[91,:] + stock_scorp_arr[91,:]
                           + stock_soleprop_arr[91,:]
                           + stock_partner_arr[91,:]).sum())
        mettrlist[8] = ((mettr_ccorp[68:91,:] * stock_ccorp_arr[68:91,:]
                         + mettr_scorp[68:91,:] * stock_scorp_arr[68:91,:]
                         + mettr_soleprop[68:91,:] * stock_soleprop_arr[68:91,:]
                         + mettr_partner[68:91,:] * stock_partner_arr[68:91,:]).sum()
                        / (stock_ccorp_arr[68:91,:] + stock_scorp_arr[68:91,:]
                           + stock_soleprop_arr[68:91,:]
                           + stock_partner_arr[68:91,:]).sum())
        # Store average results for user cost of capital
        ucoclist[0] = ((ucoc_ccorp * stock_ccorp_arr
                        + ucoc_scorp * stock_scorp_arr
                        + ucoc_soleprop * stock_soleprop_arr
                        + ucoc_partner * stock_partner_arr).sum()
                       / (stock_ccorp_arr + stock_scorp_arr
                         + stock_soleprop_arr + stock_partner_arr).sum())
        ucoclist[1] = ((ucoc_ccorp * stock_ccorp_arr).sum()
                       / stock_ccorp_arr.sum())
        ucoclist[2] = ((ucoc_scorp * stock_scorp_arr).sum()
                       / stock_scorp_arr.sum())
        ucoclist[3] = ((ucoc_soleprop * stock_soleprop_arr).sum()
                       / stock_soleprop_arr.sum())
        ucoclist[4] = ((ucoc_partner * stock_partner_arr).sum()
                       / stock_partner_arr.sum())
        ucoclist[5] = ((ucoc_ccorp[0:37,:] * stock_ccorp_arr[0:37,:]
                        + ucoc_scorp[0:37,:] * stock_scorp_arr[0:37,:]
                        + ucoc_soleprop[0:37,:] * stock_soleprop_arr[0:37,:]
                        + ucoc_partner[0:37,:] * stock_partner_arr[0:37,:]).sum()
                       / (stock_ccorp_arr[0:37,:] + stock_scorp_arr[0:37,:]
                          + stock_soleprop_arr[0:37,:]
                          + stock_partner_arr[0:37,:]).sum())
        ucoclist[6] = ((ucoc_ccorp[37:68,:] * stock_ccorp_arr[37:68,:]
                        + ucoc_scorp[37:68,:] * stock_scorp_arr[37:68,:]
                        + ucoc_soleprop[37:68,:] * stock_soleprop_arr[37:68,:]
                        + ucoc_partner[37:68,:] * stock_partner_arr[37:68,:]).sum()
                       / (stock_ccorp_arr[37:68] + stock_scorp_arr[37:68,:]
                          + stock_soleprop_arr[37:68,:]
                          + stock_partner_arr[37:68,:]).sum())
        ucoclist[7] = ((ucoc_ccorp[91,:] * stock_ccorp_arr[91,:]
                        + ucoc_scorp[91,:] * stock_scorp_arr[91,:]
                        + ucoc_soleprop[91,:] * stock_soleprop_arr[91,:]
                        + ucoc_partner[91,:] * stock_partner_arr[91,:]).sum()
                       / (stock_ccorp_arr[91,:] + stock_scorp_arr[91,:]
                          + stock_soleprop_arr[91,:]
                          + stock_partner_arr[91,:]).sum())
        ucoclist[8] = ((ucoc_ccorp[68:91,:] * stock_ccorp_arr[68:91,:]
                        + ucoc_scorp[68:91,:] * stock_scorp_arr[68:91,:]
                        + ucoc_soleprop[68:91,:] * stock_soleprop_arr[68:91,:]
                        + ucoc_partner[68:91,:] * stock_partner_arr[68:91,:]).sum()
                       / (stock_ccorp_arr[68:91,:] + stock_scorp_arr[68:91,:]
                          + stock_soleprop_arr[68:91,:]
                          + stock_partner_arr[68:91,:]).sum())
        # Store average results for EATRs
        eatrdlist[0] = (eatr_d * stock_ccorp_arr).sum() / stock_ccorp_arr.sum()
        eatrflist[0] = (eatr_f * stock_ccorp_arr).sum() / stock_ccorp_arr.sum()
        eatrdlist[5] = ((eatr_d[0:37,:] * stock_ccorp_arr[0:37,:]).sum()
                        / stock_ccorp_arr[0:37,:].sum())
        eatrflist[5] = ((eatr_f[0:37,:] * stock_ccorp_arr[0:37,:]).sum()
                        / stock_ccorp_arr[0:37,:].sum())
        eatrdlist[6] = ((eatr_d[37:68,:] * stock_ccorp_arr[37:68,:]).sum()
                        / stock_ccorp_arr[37:68,:].sum())
        eatrflist[6] = ((eatr_f[37:68,:] * stock_ccorp_arr[37:68,:]).sum()
                        / stock_ccorp_arr[37:68,:].sum())
        eatrdlist[7] = ((eatr_d[91,:] * stock_ccorp_arr[91,:]).sum()
                        / stock_ccorp_arr[91,:].sum())
        eatrflist[7] = ((eatr_f[91,:] * stock_ccorp_arr[91,:]).sum()
                        / stock_ccorp_arr[91,:].sum())
        eatrdlist[8] = ((eatr_d[68:91,:] * stock_ccorp_arr[68:91,:]).sum()
                        / stock_ccorp_arr[68:91,:].sum())
        eatrflist[8] = ((eatr_f[68:91,:] * stock_ccorp_arr[68:91,:]).sum()
                        / stock_ccorp_arr[68:91,:].sum())
        # Save and return results
        df1 = pd.DataFrame({'Category': catlist, 'CoC': coclist,
                            'METR': mtrlist, 'UCoC': ucoclist,
                            'EATRd': eatrdlist, 'EATRf': eatrflist,
                            'METTR': mettrlist})
        return df1
    
    def tabulate_main_multiyear(self, yearlist):
        """
        Run tabulate_main(year) for every year in yearlist, and
        combine results. Export the combined results to CSVs.
        """
        # Create empty DataFrames to store results
        mtr_res = pd.DataFrame({'Category': catlist})
        mettr_res = pd.DataFrame({'Category': catlist})
        coc_res = pd.DataFrame({'Category': catlist})
        ucoc_res = pd.DataFrame({'Category': catlist})
        eatrd_res = pd.DataFrame({'Category': catlist})
        eatrf_res = pd.DataFrame({'Category': catlist})
        # Tabulate for each year and store results
        for year in yearlist:
            res1_all = self.tabulate_main(year)
            mtr_res[str(year)] = res1_all['METR']
            mettr_res[str(year)] = res1_all['METTR']
            coc_res[str(year)] = res1_all['CoC']
            ucoc_res[str(year)] = res1_all['UCoC']
            eatrd_res[str(year)] = res1_all['EATRd']
            eatrf_res[str(year)] = res1_all['EATRf']
        # Save results to tables for combining later
        coc_res.to_csv(OUTPUTPATH + 'main/' + 'coc_' + self.key + '.csv',
                       index=False)
        mtr_res.to_csv(OUTPUTPATH + 'main/' + 'mtr_' + self.key + '.csv',
                       index=False)
        mettr_res.to_csv(OUTPUTPATH + 'main/' + 'mettr_' + self.key + '.csv',
                         index=False)
        ucoc_res.to_csv(OUTPUTPATH + 'main/' + 'ucoc_' + self.key + '.csv',
                        index=False)
        eatrd_res.to_csv(OUTPUTPATH + 'main/' + 'eatrd_' + self.key + '.csv',
                         index=False)
        eatrf_res.to_csv(OUTPUTPATH + 'main/' + 'eatrf_' + self.key + '.csv',
                         index=False)

        return None
    
    def cocVariation(self, year):
        """
        Compute standard deviation of the cost of capital.
        Note: Must first run tabulate_main(year).
        """
        # Get average CoC
        df1 = self.tabulate_main(year)
        df1.set_index('Category', inplace=True)
        coc = df1.loc[catlist[0], 'CoC']
        # Extract asset weights
        stock_ccorp_arr = self.stock_ccorp.to_numpy()
        stock_scorp_arr = self.stock_scorp.to_numpy()
        stock_soleprop_arr = self.stock_soleprop.to_numpy()
        stock_partner_arr = self.stock_partner.to_numpy()
        wgtarray = np.zeros((ntype, nind, 4))
        wgtarray[:,:,0] = stock_ccorp_arr
        wgtarray[:,:,1] = stock_scorp_arr
        wgtarray[:,:,2] = stock_soleprop_arr
        wgtarray[:,:,3] = stock_partner_arr
        # Extract results by firm type
        coc_ccorp = self.calc.results_coc[str(year)]['corp']
        coc_scorp = self.calc.results_coc[str(year)]['scorp']
        coc_soleprop = self.calc.results_coc[str(year)]['soleprop']
        coc_partner = self.calc.results_coc[str(year)]['partner']
        # Build array of squared deviations
        vararray = np.zeros((ntype, nind, 4))
        vararray[:,:,0] = (coc_ccorp - coc)**2
        vararray[:,:,1] = (coc_scorp - coc)**2
        vararray[:,:,2] = (coc_soleprop - coc)**2
        vararray[:,:,3] = (coc_partner - coc)**2
        # Compute variance
        vcoc = (vararray * wgtarray).sum() / wgtarray.sum()
        sdcoc = vcoc**0.5
        return sdcoc
        
        


