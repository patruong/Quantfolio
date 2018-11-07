# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 22:45:53 2018

@author: Patrick
"""

"""
NOTE BT is using OPEN prices of day2 to do trade strategy because
https://community.backtrader.com/topic/15/convincing-strategy-to-buy-at-close-of-current-bar-in-backtest


"""
import backtrader as bt
import backtrader.feeds as btfeeds

import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import scipy as sp

import API_KEY as KEY
from datetime import datetime

import strategy as strat
import analysis

def preprocess_pandasDatareader_quandl_df(df):
    """
    Rearrange pandas-datareader quandl source df to use
    adj. open prices instead of raw open prices.
    
    This adjustment makes the data same format as bt.feeds 
    original data format i.e. using adj. open of day 2.
    """
    df = df.reindex(index=df.index[::-1])
    df = df.drop(["Open", "High", "Low", "Close", "Volume", "ExDividend", "SplitRatio"], 1)
    df.columns = ["Open", "High", "Low", "Close", "Volume"]
    return df

def Backtest(startCapital, strategy, data):
    """
    startCapital = starting capital
    strategy = a strategy from strategy.py
    
    """
    #Variable for our starting cash
    startcash = startCapital

    #Create an instance of cerebro
    cerebro = bt.Cerebro()
    
    #Add our strategy
    cerebro.addstrategy(strategy)
    
    #Add the data to Cerebro
    cerebro.adddata(data)
    
    # Set our desired cash start
    cerebro.broker.setcash(startcash)
    
    # Run over everything
    cerebro.run()
    
    #Get final portfolio Value
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash
    
    #Print out the final result
    print('Final Portfolio Value: ${}'.format(portvalue))
    print('P/L: ${}'.format(pnl))
    
    #Finally plot the end results
    cerebro.plot(style='candlestick')
    
if __name__ == "__main__":
    API_KEY = KEY.quandlAPI_KEY()
    
    startcash = 10000
    
    MyStrat = strat.BuyAndHold(size = 1)
    MyStrat = strat.RSI(size = 1, period = 21, rsi_low = 30, rsi_high = 70)
    
    #Get data - quandl to bt.feed
    #stock = "GS".
    #data = bt.feeds.Quandl(
    #    dataname= stock,
    #    fromdate = datetime(2013,8,5),
    #    todate = datetime(2018,8,5),
    #    buffered= True,
    #    apikey=API_KEY
    #    )
    
    # Get data as dataframe
    stock = "GS"
    df = web.DataReader(stock, "quandl", "2013-08-05", "2018-08-05")
    
    # Rearrange data for bt.feeds readin of pandas-datareader format
    df = preprocess_pandasDatareader_quandl_df(df)
    
    datap = bt.feeds.PandasData(dataname = df)
    #Backtest(startCapital = 10000, strategy = MyStrat, data = datap)

    #Create an instance of cerebro
    cerebro = bt.Cerebro()    

    #Add our strategy
    cerebro.addstrategy(MyStrat)

    #Add the data to Cerebro
    cerebro.adddata(datap)
    
    # Set our desired cash start
    cerebro.broker.setcash(startcash)
    
    # Add the analyzers we are interested in
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

    # Run over everything
    strategies = cerebro.run()
    firstStrat = strategies[0]
        
    #Get final portfolio Value
    portvalue = cerebro.broker.getvalue()
    
    #Print out the final result
    print('Final Portfolio Value: ${}'.format(portvalue))
    
    #Finally plot the end results
    cerebro.plot(style='candlestick')
    
    # print the analyzers
    analysis.printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())
    analysis.printSQN(firstStrat.analyzers.sqn.get_analysis())
    analysis.printSQNref()
