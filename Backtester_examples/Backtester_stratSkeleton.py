# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 18:59:02 2018

@author: Patrick
"""

import backtrader as bt
class MyStrategy(bt.Strategy):

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(period=15)

    def next(self):
        if self.sma > self.data.close:
            # Do something
            pass

        elif self.sma < self.data.close:
            # Do something else
            pass