# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 00:53:10 2018

@author: Patrick
"""

import pandas_datareader.data as web
import pandas_datareader
import pandas as pd
import numpy as np
from talib import RSI, BBANDS
import matplotlib.pyplot as plt
start = '2015-04-22'
end = '2017-04-22'

# Read in data 
symbol = 'MCD'
max_holding = 100
price = web.DataReader(name=symbol, data_source='quandl', start=start, end=end)
price = price.iloc[::-1]
price = price.dropna()
close = price['AdjClose'].values
up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
rsi = RSI(close, timeperiod=14)
print("RSI (first 10 elements)\n", rsi[14:24])

def bbp(price):
    up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    bbp = (price['AdjClose'] - low) / (up - low)
    return bbp

# Add technical indicators to df
price["RSI"] = RSI(close, timeperiod=14)
price["BBP"] = bbp(price)
index = price.index
price["BB_up"], price["BB_mid"], price["BB_low"] = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

# Calculating holding based on RSI and BBP strategy
holdings = pd.DataFrame(index=price.index, data={'Holdings': np.array([np.nan] * index.shape[0])})
holdings.loc[((price['RSI'] < 30) & (price['BBP'] < 0)), 'Holdings'] = max_holding
holdings.loc[((price['RSI'] > 70) & (price['BBP'] > 1)), 'Holdings'] = 0
holdings.ffill(inplace=True)
holdings.fillna(0, inplace=True)

holdings['Order'] = holdings.diff()
holdings.dropna(inplace=True)

# Calculate gains
buy_and_sell_Prices = pd.DataFrame(holdings["Order"]*price["Close"], columns = ["prices"])
buy_and_sell_Prices.fillna(0, inplace = True)
buy_and_sell_Prices = -buy_and_sell_Prices.loc[buy_and_sell_Prices["prices"] != 0.0]
buyPrices = -buy_and_sell_Prices.loc[buy_and_sell_Prices["prices"] < 0 ]
sellPrices = buy_and_sell_Prices.loc[buy_and_sell_Prices["prices"] > 0 ] 
diffPrices = sellPrices.values - buyPrices
totalGain = diffPrices.sum()


# Plotting
fig, (ax0, ax1, ax2) = plt.subplots(3, 1, sharex=True, figsize=(12, 8))
ax0.plot(index, price['AdjClose'], label='AdjClose')
ax0.set_xlabel('Date')
ax0.set_ylabel('AdjClose')
ax0.grid()
for day, holding in holdings.iterrows():
    order = holding['Order']
    if order > 0:
        ax0.scatter(x=day, y=price.loc[day, 'AdjClose'], color='green')
    elif order < 0:
        ax0.scatter(x=day, y=price.loc[day, 'AdjClose'], color='red')

ax1.plot(index, price['RSI'], label='RSI')
ax1.fill_between(index, y1=30, y2=70, color='#adccff', alpha='0.3')
ax1.set_xlabel('Date')
ax1.set_ylabel('RSI')
ax1.grid()

ax2.plot(index, price['BB_up'], label='BB_up')
ax2.plot(index, price['AdjClose'], label='AdjClose')
ax2.plot(index, price['BB_low'], label='BB_low')
ax2.fill_between(index, y1=price['BB_low'], y2=price['BB_up'], color='#adccff', alpha='0.3')
ax2.set_xlabel('Date')
ax2.set_ylabel('Bollinger Bands')
ax2.grid()

fig.tight_layout()
plt.show()