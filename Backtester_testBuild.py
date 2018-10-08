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
                  period=50)
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data, period=period=self.params.period1)
        self.sma_2 = bt.talib.SMA(self.data, period=period=self.params.period2)
    def next(self):
        if self.sma > self.data.close:
            # Do something
            pass

        elif self.sma < self.data.close:
            # Do something else
            pass