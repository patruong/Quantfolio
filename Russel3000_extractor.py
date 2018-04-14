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

path = "C:\\cygwin64\\home\\Patrick\\Quantfolio"
chdir(path)
print(getcwd())

ticker_df = pd.read_csv("Russell3000-Tickers.csv")
tickers = ticker_df["Ticker"]

start = datetime.datetime(2015, 4 ,13)
end = datetime.datetime(2018,04,13)
    
company_list = ["GOOG",
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
    
    df = pd.DataFrame()
    
    for i in company_list:
        f = web.DataReader(i, "iex", start, end)
        df[i] = f.close
        time.sleep(2)