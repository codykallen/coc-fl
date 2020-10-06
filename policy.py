import pandas as pd


class Policy():
    """
	Policy class. 

	Reads in policy parameters and stores them. 
	"""

    def __init__(self, POLFILE='policy_baseline.csv'):
        self.policies = pd.read_csv(POLFILE)
        self.policies.set_index('year', inplace=True)
        ccrfile = pd.ExcelFile('CCR_rules.xlsx')
        ccrRules = dict()
        for year in range(2020, 2030):
            sheetname = self.policies.loc[year, 'ccr_sheet']
            ccr1 = pd.read_excel(ccrfile, sheet_name=sheetname)
            ccr1.rename({'Asset code': 'asset'}, axis=1, inplace=True)
            ccrRules[str(year)] = ccr1.set_index('asset')
        ccr2 = pd.read_excel(ccrfile, sheet_name='foreign')
        ccr2.rename({'Asset code': 'asset'}, axis=1, inplace=True)
        ccrRules['foreign'] = ccr1.set_index('asset')
        self.ccrRules = ccrRules
        
    def read_ccr(self, year):
        """
        Return DF of capital cost recovery rules for the given year.
        """
        if type(year) is not int:
            if year == 'foreign':
                return self.ccrRules['foreign']
            else:
                print('Warning: year must be an integer!')
                return None
        else:
            if year < 2020:
                print('Warning: year must be >= 2020')
                return None
            elif year > 2029:
                return self.ccrRules['2029']
            else:
                return self.ccrRules[str(year)]
    
    def fetch(self, term, year):
        """
        Return the value of the policy parameter "term" in the given year.
        """
        return self.policies.loc[year, term]

