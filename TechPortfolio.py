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
from Markowitz import *

path = "C:\\cygwin64\\home\\Patrick\\Quantfolio"
chdir(path)
print(getcwd())


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

weights = rand_weights(n_stocks)

# Generate random portfolio

n_portfolios = 10000
means, stds = np.column_stack([
        random_portfolio(df_ret.T) 
        for _ in xrange(n_portfolios)
        ])

plt.plot(stds, means, 'o', markersize = 5)
plt.xlabel("std")
plt.ylabel("mean")
plt.title("Mean and standard deviation of returns of randomly generated portfolios")


weights, returns, risks, portfolios = optimal_portfolio(df_ret.T)
plt.plot(stds, means, 'o')
plt.xlabel("std")
plt.ylabel("mean")
plt.plot(risks, returns, "y-o")

# Risk and returns
risk_reward_df = pd.DataFrame([risks, returns], index = ["Std", "Mean"]).T

# Portfolio Weights - find desired portfolio in risk_reward_df
portfolio_n = 43
pd.DataFrame(np.array(portfolios[portfolio_n]), index = df_ret.T.index, columns=["weights"])

portfolio_n = 0
pd.DataFrame(np.array(portfolios[portfolio_n]), index = df_ret.T.index, columns=["weights"])


# log returns are additive
np.e**(0.002*252)
