# -*- coding: utf-8 -*-
"""
Created on Wed Oct 03 20:48:23 2018

@author: Patrick

Script for Tech portfolio
"""



import pandas as pd
import numpy as np
import pandas_datareader.data as web
import seaborn as sns
import datetime 
import time


from os import listdir
from os.path import isfile, join
from os import chdir
from os import getcwd

from Stock_extractor import *
from BetaScript import *
from Markowitz_example import *
path = "C:\\cygwin64\\home\\Patrick\\Quantfolio"
chdir(path)
print(getcwd())

def rand_weights(n):
    " Produces n random weights that sum to 1 "
    k = np.random.rand(n)
    return (k / sum(k))

tech_tickers = ["GOOG",
                "FB",
                "AMZN",
                "TSLA",
                "NFLX",
                "BABA",
                "MSFT",
                "NVDA",
                "AMD"]
n_stocks = len(tech_tickers)
start = datetime.datetime(2015, 4, 13)
end = datetime.datetime(2018, 10, 01)
df_open, df_high, df_low, df_close, df_volume = stock_extractor(tech_tickers, start, end)

df_ret = Log_returns(df_close)

# correlations
df_corr = df_ret.corr()
sns.heatmap(df_corr)


