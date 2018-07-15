# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 23:30:54 2018

@author: Patrick
"""

from iexfinance import get_historical_data
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates



# Read-in Data
 
ticker = 'TSLA'

start_date='2016-01-01'
end_date='2018-07-13'
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
     
data = get_historical_data(ticker, start=start_date, end=end_date, output_format='pandas')
df = data
df['date'] = pd.to_datetime(data.index)
df = df.set_index('date')

# Plot data
def plot_data(df, tick_interval = 40, usePandas = True):
    #usePandas=True
    tick_interval = tick_interval
    #Either use pandas
    if usePandas:
        df.plot(x_compat=True)
        plt.gca().xaxis.set_major_locator(dates.DayLocator(interval = tick_interval))
        plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
        #plt.gca().invert_xaxis()
        plt.gcf().autofmt_xdate(rotation=90, ha="center")
    # or use matplotlib
    else:
        plt.plot(df["date"], df["ratio1"])
        plt.gca().xaxis.set_major_locator(dates.DayLocator(interval = tick_interval))
        plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
        #plt.gca().invert_xaxis()
    
    plt.show()

def log_return(df):
    "price data df to log-return df"
    log_returns = np.log(df) - np.log(df.shift(1))
    return log_returns
    

def RSI(df, period = 14, SMMA = True, alpha = False, price_data = True):
    """
    Takes price data or return data and return RSI as defined by Wilders 
    original formula (wikipedia RSI).
    
    SMMA = True : Wilders original formula with exponential RSI.
    SMMA = False : Use normal MA.
    alpha = specify alpha for exponential MA. Not used in normal MA.
    price_data = True : if input is price_data.
    price_data = False : if input is (log) return data.
    """
    
    if price_data == True:
        main_returns = log_return(df)
    else:
        main_returns = df
        
    if alpha == False:
        alpha = 1/period
    
    if SMMA == True:
        "SMMA as defined by Wilders original formulation of RSI (WIKI)"
        rolling_sum_of_gains = main_returns[main_returns > 0].fillna(0).ewm(alpha = alpha).mean()
        rolling_sum_of_losses = -1*main_returns[main_returns < 0].fillna(0).ewm(alpha = alpha).mean()
    else:
        "Normal MA RSI"
        rolling_sum_of_gains = main_returns[main_returns > 0].fillna(0).rolling(period).mean()
        rolling_sum_of_losses = -1*main_returns[main_returns < 0].fillna(0).rolling(period).mean()
    
    RS = rolling_sum_of_gains / rolling_sum_of_losses
    RSI = 100 - (100 / (1 + RS))
    
    return RSI

def plot_RSI(rsi_data, overbought = 70, oversold = 30):
    "Input RSI data"
    
    ax = main_data.RSI.plot()
    ax.axhline(70, color = "r")
    ax.axhline(30, color = "r")
    



if __name__ == "__main__":

    plot_data(df.close)
    
    main_data = pd.DataFrame(df.close, index = df.index)
    main_price = pd.DataFrame(df.close, index = df.index)
    main_returns = log_return(main_data)
    
    
    # MA 
    main_data["MA20"] = main_price.close.rolling(20).mean()
    main_data["MA50"] = main_price.close.rolling(50).mean()
    main_data["MA200"] = main_price.close.rolling(200).mean()

    # RSI 
    main_data["RSI"] = RSI(main_price)
    plot_RSI(main_data.RSI)
    
    
    plot_data(main_data)
