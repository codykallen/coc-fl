# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 20:00:16 2020

@author: cody_
"""

import os
os.chdir('C:/Users/cody_/Documents/GitHub/coc-fl')
import numpy as no
import pandas as pd
from parameter import Parameter
from policy import Policy
from calculator import Calculator
from outputBuilder import OutputBuilder

pol1 = Policy()
parm1 = Parameter()
calc1 = Calculator(parm1, pol1)

calc1.calc_all_basic(2021)

ob = OutputBuilder(calc1, 'base')
ob.store_raw(2021)



