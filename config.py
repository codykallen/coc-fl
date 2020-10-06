"""
Various quantities and relevant paths
for use by classes.
"""
INPUTPATH = 'data_files/'
OUTPUTPATH = 'output/'

# Number of industries
nind=62
# Numbers of asset types
ntype = 92

# List of industry codes (exclude Federal Reserve Banks)
ind_codes = ['110C', '113F', '2110', '2120', '2130', '2200', '2300',
             '3210', '3270', '3310', '3320', '3330', '3340', '3350',
             '336M', '336O', '3370', '338A', '311A', '313T', '315A',
             '3220', '3230', '3240', '3250', '3260', '4200', '44RT',
             '4810', '4820', '4830', '4840', '4850', '4860', '487S',
             '4930', '5110', '5120', '5130', '5140', '5250',
             '5220', '5230', '5240', '5310', '5320', '5411', '5415',
             '5412', '5500', '5610', '5620', '6100', '6210', '622H',
             '6230', '6240', '711A', '7130', '7210', '7220', '8100']

# List of asset types
ast_codes = ['EP1A', 'EP1B', 'EP1C', 'EP1D', 'EP1E', 'EP1F', 'EP1G', 'EP1H',
             'EP20', 'EP34', 'EP35', 'EP36', 'EP31', 'EP12', 'EI11', 'EI12',
             'EI21', 'EI22', 'EI30', 'EI40', 'EI50', 'EI60', 'ET11', 'ET12',
             'ET20', 'ET30', 'ET40', 'ET50', 'EO12', 'EO30', 'EO21', 'EO40',
             'EO22', 'EO50', 'EO60', 'EO72', 'EO80', 'SOO1', 'SB31', 'SB32',
             'SOO2', 'SC03', 'SC04', 'SC01', 'SOMO', 'SC02', 'SI00', 'SU30',
             'SU60', 'SU40', 'SU50', 'SU20', 'SM01', 'SM02', 'SB20', 'SB41',
             'SB42', 'SB43', 'SB45', 'SU11', 'SU12', 'SB44', 'SB46', 'SN00',
             'SO01', 'SO02', 'SO03', 'SO04', 'ENS1', 'ENS2', 'ENS3', 'RD11',
             'RD12', 'RD23', 'RD21', 'RD22', 'RD24', 'RD25', 'RD31', 'RD32',
             'RDOM', 'RD70', 'RD40', 'RD50', 'RD60', 'RD80', 'AE10', 'AE20',
             'AE30', 'AE40', 'AE50', 'RES']

# List of cateogies for main tables
catlist = ['All', 'C corporations', 'S corporations',
           'Sole proprietorships', 'Partnerships',
           'Equipment', 'Structures', 'Residential',
           'Intellectual property']

