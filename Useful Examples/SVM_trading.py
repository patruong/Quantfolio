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

#data = web.get_data_yahoo("SPY", start = "2000-01-01", end = "2018-11-08")

stock = "^DJI"
data = web.DataReader(stock, "stooq", "2013-08-05", "2018-08-05")
stock = "F"
data = web.DataReader(stock, "quandl", "2013-08-05", "2018-08-05")
stock = "WFC"
data = web.DataReader(stock, "quandl", "2013-08-05", "2018-08-05")
stock = "DIS"
data = web.DataReader(stock, "quandl", "2013-08-05", "2018-08-05")
stock = "CAT"
data = web.DataReader(stock, "quandl", "2013-08-05", "2018-08-05")


df = data["2018-11-08":"2000-11-08"]
df = df.reindex(index=df.index[::-1]) #reverse rows
df = df[["Open", "High", "Low", "Close"]]

n = 10 # look-back period
t = 0.8 # 80 % training set, 20 % test set
split = int(t*len(df))

# Data preprocessing
df["high"] = df["High"].shift(1)
df["low"] = df["Low"].shift(1)
df["close"] = df["Close"].shift(1)
df = df.drop(["High", "Low", "Close"], axis = 1) #here ok ?

# Feature Engineering - Technical analysis 
df["RSI"] = ta.RSI(np.array(df["close"]), timeperiod = n)
df["SMA"] = df["close"].rolling(window=n).mean()
df["Corr"] = df["SMA"].rolling(window=n).corr(df["close"])
df["SAR"] = ta.SAR(np.array(df["high"]), np.array(df["low"]), 0.2, 0.2)
df["ADX"] = ta.ADX(np.array(df["high"]), np.array(df["low"]), np.array(df["close"]), timeperiod = n)
df["Return"] = np.log(df["Open"]/df["Open"].shift(1))
df = df.dropna()

########################
### Gaussian Mixture ###
########################

# Regime prediction
ss = StandardScaler()
unsup = mix.GaussianMixture(n_components = 4,
                            covariance_type = "spherical",
                            n_init = 100,
                            random_state = 42)
unsup.fit(np.reshape(ss.fit_transform(df[:split]), (-1, df.shape[1])))
regime = unsup.predict(np.reshape(ss.fit_transform(df[split:]), (-1, df.shape[1])))

# Create net dataframe with Regimes in it... why so overcomplicated??
Regimes = pd.DataFrame(regime, columns = ["Regime"], index=df[split:].index).join(df[split:], how = "inner").assign(market_cu_return=df[split:].Return.cumsum()).reset_index(drop=False).rename(columns={"index":"Date"})

# Plot Regimes
order = [0,1,2,3]
fig = sns.FacetGrid(data = Regimes, hue = "Regime", hue_order = order, aspect = 2, size = 4)
fig.map(plt.scatter, "Date", "market_cu_return", s= 4).add_legend()
plt.show()

##############
### SVM ######
##############

# plot mean and variance
for i in order:
    print("Mean for regime %i: "%i, unsup.means_[i][0])
    print("Covariance for regime %i: "%i, unsup.covariances_[i])

# Create prediction values
ss1 = StandardScaler()
columns = Regimes.columns.drop(["Regime","Date"])
Regimes[columns] = ss1.fit_transform(Regimes[columns])
Regimes["Signal"]=0
Regimes.loc[Regimes["Return"]>0, "Signal"] = 1 #class bull
Regimes.loc[Regimes["Return"]<0, "Signal"] = -1 #class bear

# non-optimized classifier
cls = SVC(C= 1.0, cache_size = 200, class_weight=None, coef0 = 0.0,
          decision_function_shape = None, degree = 3, gamma = "auto",
          kernel = "rbf", max_iter = -1, probability = False, random_state = None,
          shrinking = True, tol = 0.001, verbose = False)

# train the model
split2 = int(.8*len(Regimes))
X = Regimes.drop(["Signal", "Return", "market_cu_return", "Date"], axis = 1)
y = Regimes["Signal"]
cls.fit(X[:split2], y[:split2])

p_data = len(X)-split2

df["Pred_Signal"] = 0
df.iloc[-p_data:,df.columns.get_loc("Pred_Signal")] = cls.predict(X[split2:])

print(df["Pred_Signal"][-p_data:])
df["str_ret"] = df["Pred_Signal"]*df["Return"].shift(-1) #this will need to account for fees and spread

df["strategy_cu_return"]=0
df["market_cu_return"]=0
df.iloc[-p_data:,df.columns.get_loc("strategy_cu_return")] = np.nancumsum(df["str_ret"][-p_data:])
df.iloc[-p_data:,df.columns.get_loc("market_cu_return")] = np.nancumsum(df["Return"][-p_data:])
Sharpe = (df["strategy_cu_return"][-1] - df["market_cu_return"][-1])/np.nanstd(df["strategy_cu_return"][-p_data:])

plt.plot(df["strategy_cu_return"][-p_data:], color = "g", label = "Strategy Returns")
plt.plot(df["market_cu_return"][-p_data:], color = "r", label = "Market Returns")
plt.figtext(0.14, 0.9, s="Sharpe ratio: %.2f"%Sharpe)
plt.legend(loc="best")
plt.show()