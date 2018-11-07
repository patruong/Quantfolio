#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 17:06:23 2018

@author: ptruong

Py36

Implement SVM with feature engineering, 10 technical indicators as features.

Source
- http://epchan.blogspot.com/2010/10/data-mining-and-artificial-intelligence.html
- https://www2.eecs.berkeley.edu/Pubs/TechRpts/2010/EECS-2010-63.pdf

"""

import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime 
import time
import matplotlib.pyplot as plt
import talib as ta

close = np.random.random(100)

output = ta.SMA(close)

EMA7 = ta.EMA(close, timeperiod = 7)
EMA50 = ta.EMA(close, timeperiod = 50)
EMA200 = ta.EMA(close, timeperiod = 200)
MACD = 
# Data readin
stock = "^DJI"
df = web.DataReader(stock, "stooq", "2013-08-05", "2018-08-05")

# subsetting data
df_part = df.head(706)
df_invert = (0-df_part)+50000




"""
- EMA7
- EMA50
- EMA200
- MACD(26,12,9)
- RSI
- ADX
- Lag Profits
- High
- Low
-Closing price > EMA200

Volume???
"""


