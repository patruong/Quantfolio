# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 23:38:00 2018

@author: Patrick
"""

import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime 
import time

from os import listdir
from os.path import isfile, join
from os import chdir
from os import getcwd

#path = "C:\\cygwin64\\home\\Patrick\\Quantfolio"
#chdir(path)
#print(getcwd())

def stock_extractor(tickers, start, end, sleep_time = 1):
    df_open = pd.DataFrame()
    df_high = pd.DataFrame()
    df_low = pd.DataFrame()
    df_close = pd.DataFrame()
    df_volume = pd.DataFrame()
    
    
    for i in tickers:
        f = web.DataReader(i, "iex", start, end)
        df_open[i] = f.open
        df_high[i] = f.high
        df_low[i] = f.low
        df_close[i] = f.close
        df_volume[i] = f.volume
        time.sleep(sleep_time)
    
    return df_open, df_high, df_low, df_close, df_volume

if __name__ == "__main__":
    
    start = datetime.datetime(2015, 4 ,13)
    end = datetime.datetime(2018,04,13)
    
    # tickers small test set
    tickers = ["GOOG",
                    "F",
                    "GS",
                    "ABB",
                    "ALE",
                    "ALV",
                    "BCO",
                    "CAT",
                    "CMG",
                    "DB",
                    "GE",
                    "JNJ",
                    "MON",
                    "MS",
                    "NKE",
                    "ORA",
                    "PFE",
                    "RWT",
                    "SBUX",
                    "T",
                    "TGT",
                    "XOM"]
    
    #ticker_df = pd.read_csv("Russell3000-Tickers.csv")
    #tickers = ticker_df["Ticker"] # takes long time!
    
    df_open, df_high, df_low, df_close, df_volume = stock_extractor(tickers, start, end)


