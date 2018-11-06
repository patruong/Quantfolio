# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 22:03:44 2018

@author: Patrick
"""


import backtrader as bt

def BuyAndHold(size):
    size = size
    class MyStrategy(bt.Strategy):
        def __init__(self):
            pass
        def next(self):
            if not self.position:
                self.buy(size=size)
    return MyStrategy

def GoldenCross(size):
    size = size
    class MyStrategy(bt.Strategy):
        params = dict(period1=20,
                      period2=50,
                      period3 = 200)
        def __init__(self):
            self.sma_50 = bt.talib.SMA(self.data, timeperiod=self.params.period2)
            self.sma_200 = bt.talib.SMA(self.data, timeperiod=self.params.period3)
    
        def next(self):
            if not self.position:
                if self.sma_50 > self.sma_200:
                    self.buy(size=size)
            else:
                if self.sma_50 < self.sma_200:
                    self.sell(size=size)
    return MyStrategy

def RSI(size, period = 21, rsi_low = 30, rsi_high = 70):
    size = size
    period = period
    rsi_low = rsi_low
    rsi_high = rsi_high
    class firstStrategy(bt.Strategy):
    
        def __init__(self):
            self.rsi = bt.indicators.RSI_SMA(self.data.close, period=period)
    
        def next(self):
            if not self.position:
                if self.rsi < rsi_low:
                    self.buy(size=size)
            else:
                if self.rsi > rsi_high:
                    self.sell(size=size)
    return firstStrategy