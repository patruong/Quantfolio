# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 00:53:10 2018

@author: Patrick
"""

"""
Source:
    https://towardsdatascience.com/trading-strategy-technical-analysis-with-python-ta-lib-3ce9d6ce5614
"""
# set path
from os import listdir
from os.path import isfile, join
from os import chdir
from os import getcwd
directory = "C:\\cygwin64\\home\\Patrick\\Quantfolio"
chdir(directory)
print(getcwd())

import pandas_datareader.data as web
import pandas_datareader
import pandas as pd
import numpy as np
from talib import RSI, BBANDS
import matplotlib.pyplot as plt

def get_data(symbol, start, end):
    price = web.DataReader(name=symbol, data_source='quandl', start=start, end=end)
    price = price.iloc[::-1]
    price = price.dropna()
    close = price['AdjClose'].values
    #up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    #rsi = RSI(close, timeperiod=14)
    #print("RSI (first 10 elements)\n", rsi[14:24])
    return price, close

def bbp(price):
    up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    bbp = (price['AdjClose'] - low) / (up - low)
    return bbp

# Add technical indicators to df
def add_technicals(price, close):
    price["RSI"] = RSI(close, timeperiod=14)
    price["BBP"] = bbp(price)
    price["BB_up"], price["BB_mid"], price["BB_low"] = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    return price

# Calculating holding based on RSI and BBP strategy
def RSI_BBP_strategy(price, max_holding = 100):
    index = price.index
    holdings = pd.DataFrame(index=price.index, data={'Holdings': np.array([np.nan] * index.shape[0])})
    holdings.loc[((price['RSI'] < 30) & (price['BBP'] < 0)), 'Holdings'] = max_holding
    holdings.loc[((price['RSI'] > 70) & (price['BBP'] > 1)), 'Holdings'] = 0
    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)

    holdings['Order'] = holdings.diff()
    holdings.dropna(inplace=True)
    
    return holdings, index

# Calculate gains
def calculate_gains(price, holdings, currentPrice = True):
    """
    if currentPrice == True, then if strat not sell at last price, then use last price as sell price
    else if currentPrice == False, then remove last buy order, if no sell 
    """
    buy_and_sell_Prices = pd.DataFrame(holdings["Order"]*price["Close"], columns = ["Close"])
    buy_and_sell_Prices.fillna(0, inplace = True)
    buy_and_sell_Prices = -buy_and_sell_Prices.loc[buy_and_sell_Prices["Close"] != 0.0]
    buyPrices = -buy_and_sell_Prices.loc[buy_and_sell_Prices["Close"] < 0 ]
    sellPrices = buy_and_sell_Prices.loc[buy_and_sell_Prices["Close"] > 0 ] 
    try:
        diffPrices = sellPrices.values - buyPrices
    except:
        tmp_index = buyPrices.index
        tmp_cols = buyPrices.columns
        if currentPrice == True:
            "Last closing price as sell price"
            sellPrices = sellPrices.append(price.tail(1)*max_holding)["Close"]
            buyPrices = buyPrices["Close"]
        else:
            "Drop last buy order, because no selling point"
            tmp_index = tmp_index[:-1]
            buyPrices = buyPrices.drop(buyPrices.index[len(buyPrices)-1])
        temp_diffPrices = sellPrices.values - buyPrices.values
        diffPrices = pd.DataFrame(temp_diffPrices, index = tmp_index, columns = tmp_cols)

    totalGain = diffPrices.sum()
    
    wins = (diffPrices["Close"]>0)*1
    loss = (diffPrices["Close"]<0)*1
    
    earnings = wins * diffPrices["Close"]
    losses = loss * diffPrices["Close"]
    
    totalEarnings = np.matmul(wins, diffPrices.values)
    totalLoss = np.matmul(loss, diffPrices.values)
    
    WLRatio = 1/(totalEarnings/totalLoss)
    #WLRatio = WLRatios.sum()
    return (buyPrices, sellPrices, wins, loss, earnings, losses,
            totalEarnings, totalLoss, diffPrices, totalGain, WLRatio)


# Plotting
def plot_strat():
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

def testVar():
    start = '2015-04-22' #Baseline test
    end = '2017-04-22' #Baseline test
    symbol = "AAPL"
    symbol = 'MCD' #Baseline test
    return symbol, start, end

if __name__ == "__main__":
    symbol, start, end = testVar()
    
    start = '2010-04-22' #Baseline test
    end = '2018-04-22' #Baseline test
    symbol = "AAPL"
    
    # Read in data
    tickers = pd.read_csv("SP500-Tickers.csv") 

    price, close = get_data(symbol, start, end)
    price = add_technicals(price, close)
    holdings, index = RSI_BBP_strategy(price, max_holding = 100)
    buyPrices, sellPrices, wins, loss, earnings, losses, totalEarnings, totalLoss, diffPrices, totalGain, WLRatio = calculate_gains(price, holdings, currentPrice = False)
    plot_strat()

    win_list = []
    lose_list = []
    gains_list = []
    WLRatio_list = []
    
    for symbol in tickers["ticker"]:
        try:
            price, close = get_data(symbol, start, end)
            price = add_technicals(price, close)
            holdings, index = RSI_BBP_strategy(price, max_holding = 100)
            buyPrices, sellPrices, wins, loss, earnings, losses, totalEarnings, totalLoss, diffPrices, totalGain, WLRatio = calculate_gains(price, holdings)
            
            win_list.append(wins.sum())
            lose_list.append(loss.sum())
            gains_list.append(totalGain)
            WLRatio_list.append(WLRatio)
            print(symbol, "Done!")
        except:
            print("skipped: ", symbol)
            pass
            
    totalWins = sum(win_list)
    totalLose = sum(lose_list)
    totalGains = sum(gains_list).values[0]
    avgGains = (sum(gains_list)/len(gains_list)).values[0]
    
    res_list = [totalWins, totalLose, avgGains, totalGains]
    res_df = pd.DataFrame(res_list, index = ["Wins", "Losses", "avg Gains", "total Gains"], columns = ["RSI and normalized BB"])
