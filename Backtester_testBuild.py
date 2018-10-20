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


# collect data for Facebook 
start = "2013-08-05"
end = "2018-08-05"
df = web.DataReader(name='GS', data_source='iex', start=start, end=end)
df.to_csv("GS.csv")

print('SMA:', bt.talib.MA_Type.SMA)
print('T3:', bt.talib.MA_Type.T3)
print(bt.talib.SMA.__doc__)

class MyStrategy(bt.Strategy):
    params = dict(period1=20,
                  period2=50,
                  period3 = 200)
    def __init__(self):
        self.sma_20 = bt.indicators.SimpleMovingAverage(self.data, period=self.params.period1)
        self.sma_50 = bt.talib.SMA(self.data, timeperiod=self.params.period2)
        self.sma_200 = bt.talib.SMA(self.data, timeperiod=self.params.period3)
    #def next(self):
    #    if self.sma > self.data.close:
            # Do something
    #        pass

    #    elif self.sma < self.data.close:
            # Do something else
    #       pass
    def next(self):
    #    pass
        if not self.position:
            if self.sma_50 > self.sma_200:
                self.buy(size=1)
        else:
            if self.sma_50 < self.sma_200:
                self.sell(size=1)   
#Variable for our starting cash
startcash = 10000

#Create an instance of cerebro
cerebro = bt.Cerebro()

#Add our strategy
cerebro.addstrategy(MyStrategy)

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