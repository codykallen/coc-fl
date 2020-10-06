"""
Data preparation.

Things to do:
    Read in BEA asset data.
    Read in BEA investment data.
    Create array of assets by industry and asset type.
    Create array of investment by industry and asset type.
    Read in BEA assets by legal form.
    Read in BEA investment by legal form.
    Split asset and investment arrays into separate ones for:
        Corporations
        Sole proprietorships
        Partnerships
        Nonprofits
        Households
        Tax-exempt cooperatives
    Read in IRS balance sheet data for all corps and S corps
    Split Corp asset and investment arrays into C corp and S corp arrays.
    Read in financing split by industry.
"""

import copy
import numpy as np
import pandas as pd
from config import INPUTPATH, OUTPUTPATH, ind_codes

# Read in and store data files
file_stock_AI = pd.ExcelFile(INPUTPATH + 'BEA/detailnonres_stk1.xlsx')
file_inv_AI = pd.ExcelFile(INPUTPATH + 'BEA/detailnonres_inv1.xlsx')
file_resid = pd.ExcelFile(INPUTPATH + 'BEA/detailresidential.xlsx')
file_stock_L = pd.ExcelFile(INPUTPATH + 'BEA/legalform_stk.xls')
file_inv_L = pd.ExcelFile(INPUTPATH + 'BEA/legalform_inv.xls')
file_irsC = pd.ExcelFile(INPUTPATH + 'IRS/13co06ccr.xls')
file_irsS = pd.ExcelFile(INPUTPATH + 'IRS/13co07s.xls')

def read_and_clean(ind, dattype):
    """
    Reads the relevant asset by industry data from the Excel files.
    Parameters:
        ind: String for the BEA industry code
        data: String for asset stock ('stock') or investment ('inv')
    Returns a DF of the relevant measure for 2019
    """
    if dattype == 'inv':
        data1 = pd.read_excel(file_inv_AI, sheet_name=ind, header=5)
    elif dattype == 'stock':
        data1 = pd.read_excel(file_stock_AI, sheet_name=ind, header=5)
    else:
        raise ValueError('Data file must be inv or stock')
    # Drop empty row and aggregate rows
    data1.drop([0, 1, 41, 74], axis=0, inplace=True)
    # Drop unwanted asset types
    data1.drop([30, 38, 59, 93, 94], axis=0, inplace=True)
    # Keep only asset identifier and 2019 values
    data1.reset_index(inplace=True)
    #data2 = data1.filter(items=['Asset Codes', '2019'], axis=1)
    codes = data1['Asset Codes']
    measure = np.array(data1['2019'])
    data2 = pd.DataFrame({'asset': codes, ind: measure})
    #data2 = data1[['Asset Codes', '2019']]
    #data2.rename({'Asset Codes': 'asset', '2019': ind}, axis=1, inplace=True)
    #data2.set_index('asset', inplace=True)
    return data2

# Read in stock and investment data by asset type and industry
stock_data = read_and_clean(ind_codes[0], 'stock')
inv_data = read_and_clean(ind_codes[0], 'inv')
for ind in ind_codes[1:]:
    newdf1 = read_and_clean(ind, 'stock')
    newdf2 = read_and_clean(ind, 'inv')
    stock_data = stock_data.merge(right=newdf1, how='outer', on='asset')
    inv_data = inv_data.merge(right=newdf2, how='outer', on='asset')
stock_data.set_index('asset', inplace=True)
inv_data.set_index('asset', inplace=True)
    

# Read in nonresidential stock and investment data by legal organization
legal_stock = pd.read_excel(file_stock_L, sheet_name='Sheet0', header=5)
stock_byform = dict()
stock_byform['total'] = legal_stock.loc[1, '2019']
stock_byform['corp'] = legal_stock.loc[19, '2019']
stock_byform['sole prop'] = legal_stock.loc[63, '2019']
stock_byform['partner'] = legal_stock.loc[67, '2019']
stock_byform['households'] = legal_stock.loc[75, '2019'] 
stock_byform['nonprofit'] = legal_stock.loc[71, '2019']
stock_byform['coop'] = legal_stock.loc[79, '2019']

legal_inv = pd.read_excel(file_inv_L, sheet_name='Sheet0', header=5)
inv_byform = dict()
inv_byform['total'] = legal_inv.loc[1, '2019']
inv_byform['corp'] = legal_inv.loc[19, '2019']
inv_byform['sole prop'] = legal_inv.loc[63, '2019']
inv_byform['partner'] = legal_inv.loc[67, '2019']
inv_byform['households'] = legal_inv.loc[75, '2019'] 
inv_byform['nonprofit'] = legal_inv.loc[71, '2019']
inv_byform['coop'] = legal_inv.loc[79, '2019']


# Read in IRS corporate data and extract asset info
irs_corp = pd.read_excel(file_irsC, sheet_name='CRTAB06', header=13)
irs_stock_corp = (irs_corp.loc[12, 1] - irs_corp.loc[13, 1] +
                  irs_corp.loc[17, 1] - irs_corp.loc[18, 1])
irs_scorp = pd.read_excel(file_irsS, sheet_name='Table 7', header=6)
irs_stock_scorp = (irs_corp.loc[13, 1] - irs_corp.loc[14, 1] +
                   irs_corp.loc[18, 1] - irs_corp.loc[19, 1])

# Update asset and investment for corporations
stock_byform['scorp'] = stock_byform['corp'] * irs_stock_scorp / irs_stock_corp
stock_byform['ccorp'] = stock_byform['corp'] - stock_byform['scorp']
inv_byform['scorp'] = inv_byform['corp'] * irs_stock_scorp / irs_stock_corp
inv_byform['ccorp'] = inv_byform['corp'] - inv_byform['scorp']

# Recompute stock data as shares instead of levels
stock_total = 0.0
inv_total = 0.0
for ind in ind_codes:
    stock_total += sum(stock_data[ind])
    inv_total += sum(inv_data[ind])
formlist = ['total', 'ccorp', 'scorp', 'sole prop', 'partner', 'households',
            'nonprofit', 'coop']
stocks = dict()
invs = dict()
for form in formlist:
    stock_data2 = copy.deepcopy(stock_data)
    inv_data2 = copy.deepcopy(inv_data)
    for ind in ind_codes:
        stock_data2[ind] = stock_data[ind] / stock_total * stock_byform[form]
        inv_data2[ind] = inv_data[ind] / inv_total * inv_byform[form]
        #stock_data2.set_index('asset', inplace=True)
        #inv_data2.set_index('asset', inplace=True)
    stocks[form] = copy.deepcopy(stock_data2)
    invs[form] = copy.deepcopy(inv_data2)

# Add residential capital to each category in residential investment data
#   BEA Fixed Assets, Tables 5.1 and 5.7
res_stk_scorp = 253.1 * irs_stock_scorp / irs_stock_corp
res_stk_ccorp = 253.1 - res_stk_scorp
res_stk_soleprop = (1893.2 * stock_byform['sole prop'] /
                    (stock_byform['sole prop'] + stock_byform['partner']))
res_stk_partner = 1893.2 - res_stk_soleprop
res_inv_scorp = 10.4 * irs_stock_scorp / irs_stock_corp
res_inv_ccorp = 10.4 - res_inv_scorp
res_inv_soleprop = (70.6 * inv_byform['sole prop'] /
                    (inv_byform['sole prop'] + inv_byform['partner']))
res_inv_partner = 70.6 - res_inv_soleprop

stocks['ccorp'].append(pd.Series(name='RES'))
stocks['ccorp'].loc['RES','5310'] = res_stk_ccorp
stocks['scorp'].append(pd.Series(name='RES'))
stocks['scorp'].loc['RES','5310'] = res_stk_scorp
stocks['sole prop'].append(pd.Series(name='RES'))
stocks['sole prop'].loc['RES','5310'] = res_stk_soleprop
stocks['partner'].append(pd.Series(name='RES'))
stocks['partner'].loc['RES','5310'] = res_stk_partner

invs['ccorp'].append(pd.Series(name='RES'))
invs['ccorp'].loc['RES','5310'] = res_inv_ccorp
invs['scorp'].append(pd.Series(name='RES'))
invs['scorp'].loc['RES','5310'] = res_inv_scorp
invs['sole prop'].append(pd.Series(name='RES'))
invs['sole prop'].loc['RES','5310'] = res_inv_soleprop
invs['partner'].append(pd.Series(name='RES'))
stocks['partner'].loc['RES','5310'] = res_inv_partner


# Save the relevant results
stocks['ccorp'].to_csv(OUTPUTPATH + 'capital/stock_ccorp.csv')
stocks['scorp'].to_csv(OUTPUTPATH + 'capital/stock_scorp.csv')
stocks['sole prop'].to_csv(OUTPUTPATH + 'capital/stock_soleprop.csv')
stocks['partner'].to_csv(OUTPUTPATH + 'capital/stock_partner.csv')
invs['ccorp'].to_csv(OUTPUTPATH + 'capital/inv_ccorp.csv')
invs['scorp'].to_csv(OUTPUTPATH + 'capital/inv_scorp.csv')
invs['sole prop'].to_csv(OUTPUTPATH + 'capital/inv_soleprop.csv')
invs['partner'].to_csv(OUTPUTPATH + 'capital/inv_partner.csv')




