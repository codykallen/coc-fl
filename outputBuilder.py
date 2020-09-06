import copy
import numpy as np
import pandas as pd
from policy import Policy
from parameter import Parameter
from config import *
from functions import *
from calculator import Calculator

class OutputBuilder():
    """
    OutputBuilder class.

    Saves results and tabulates (to be done).
    """

    def __init__(self, calc, key):
        """
            parm: Parameter class object
            pol: Policy class object
        """
        # Store Calculator object
        assert calc.calc_all_called
        self.calc = copy.deepcopy(calc)
        # Read in asset data
        self.read_assets()
        assert type(key) is str
        
    def read_assets(self):
        """
        Read in asset data by asset type, industry and firm type.
        """
        self.stock_ccorp = pd.read_csv(OUTPUTPATH + 'stock_ccorp.csv', index_col='asset')
        self.stock_scorp = pd.read_csv(OUTPUTPATH + 'stock_scorp.csv', index_col='asset')
        self.stock_soleprop = pd.read_csv(OUTPUTPATH + 'stock_soleprop.csv', index_col='asset')
        self.stock_partner = pd.read_csv(OUTPUTPATH + 'stock_partner.csv', index_col='asset')
    
    def store_raw(self, year):
        """
        Store output from Calculator for the given year.
        """
        assert str(year) in list(self.calc.results_coc)
        # Convert result arrays to DataFrames
        df_corp1 = pd.DataFrame(self.calc.results_coc[str(year)]['corp'], index=ast_codes, columns=ind_codes)
        df_scorp1 = pd.DataFrame(self.calc.results_coc[str(year)]['scorp'], index=ast_codes, columns=ind_codes)
        df_soleprop1 = pd.DataFrame(self.calc.results_coc[str(year)]['soleprop'], index=ast_codes, columns=ind_codes)
        df_partner1 = pd.DataFrame(self.calc.results_coc[str(year)]['partner'], index=ast_codes, columns=ind_codes)
        df_corp2 = pd.DataFrame(self.calc.results_metr[str(year)]['corp'], index=ast_codes, columns=ind_codes)
        df_scorp2 = pd.DataFrame(self.calc.results_metr[str(year)]['scorp'], index=ast_codes, columns=ind_codes)
        df_soleprop2 = pd.DataFrame(self.calc.results_metr[str(year)]['soleprop'], index=ast_codes, columns=ind_codes)
        df_partner2 = pd.DataFrame(self.calc.results_metr[str(year)]['partner'], index=ast_codes, columns=ind_codes)
        # Save results to CSV files
        df_corp1.to_csv(OUTPUTPATH + 'coc_corp_' + self.key + '_' + str(year) + '.csv')
        df_scorp1.to_csv(OUTPUTPATH + 'coc_scorp_' + self.key + '_' + str(year) + '.csv')
        df_soleprop1.to_csv(OUTPUTPATH + 'coc_soleprop_' + self.key + '_' + str(year) + '.csv')
        df_partner1.to_csv(OUTPUTPATH + 'coc_partner_' + self.key + '_' + str(year) + '.csv')
        df_corp2.to_csv(OUTPUTPATH + 'metr_corp_' + self.key + '_' + str(year) + '.csv')
        df_scorp2.to_csv(OUTPUTPATH + 'metr_scorp_' + self.key + '_' + str(year) + '.csv')
        df_soleprop2.to_csv(OUTPUTPATH + 'metr_soleprop_' + self.key + '_' + str(year) + '.csv')
        df_partner2.to_csv(OUTPUTPATH + 'metr_partner_' + self.key + '_' + str(year) + '.csv')
        