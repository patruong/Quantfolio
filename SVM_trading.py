# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 23:56:03 2018

@author: Patrick

Py36

Source:
    https://www.quantinsti.com/blog/trading-using-machine-learning-python-svm-support-vector-machine

"""

from pandas_datareader import data as web
import numpy as np
import pandas as pd
from sklearn import mixture as mix
import seaborn as sns
import matplotlib.pyplot as plt
import talib as ta
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import fix_yahoo_finance
