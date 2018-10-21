# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 22:16:50 2018

@author: Patrick
"""

import backtrader as bt

import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import scipy as sp
import strategy as strat
from datetime import datetime




#Variable for our starting cash
startcash = 10000

#Create an instance of cerebro
cerebro = bt.Cerebro()

#Add our strategy
C = strat.GoldenCross(size = 20)
C = strat.BuyAndHold(size = 20)
cerebro.addstrategy(C)

#Get Apple data from Yahoo Finance.
data = bt.feeds.Quandl(
    dataname='GS',
    fromdate = datetime(2013,8,5),
    todate = datetime(2018,8,5),
    buffered= True,
    apikey=API_KEY
    )

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