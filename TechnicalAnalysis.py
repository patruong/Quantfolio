# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 23:30:54 2018

@author: Patrick
"""

"""
Tools > Preferences > IPython console > Graphics > Graphics backend > Backend: Automatic / Inline

Note to self:
C:\Users\Patrick\Anaconda3\lib\site-packages\matplotlib\cbook.py:136: 
    MatplotlibDeprecationWarning: The finance module has been deprecated 
    in mpl 2.0 and will be removed in mpl 2.2. Please use the module 
    mpl_finance instead.
    warnings.warn(message, mplDeprecation, stacklevel=1) 
"""
from iexfinance import get_historical_data
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.finance as finplt




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
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = tick_interval))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        #plt.gca().invert_xaxis()
        plt.gcf().autofmt_xdate(rotation=90, ha="center")
    # or use matplotlib
    else:
        plt.plot(df["date"], df["ratio1"])
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = tick_interval))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
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

def RSI_signal(rsi_data, treshold_low = 30, treshold_high = 70):
    """
    Input RSI value, or RSI value-series. 
    Get the latest signal.
    
    ToDo: make RSI signal series output?
    """
    try:
        rsi = rsi_data[-1]
    except:
        rsi = rsi_data
    
    if rsi < 0:
        raise ValueError("Input value: "+str(rsi)+". RSI values should be between [0,100].")
    elif rsi > 100:
        raise ValueError("Input value: "+str(rsi)+". RSI values should be between [0,100].")
        
    if rsi < treshold_low:
        signal = "Buy"
    elif rsi > treshold_high:
        signal = "Sell"
    else:
        signal = "Neutral"
    return signal


def MA_crossing(price_data, low = 50, high = 200):
    """
    Detect if low MA is higher than high MA.
    """
    if price_data.rolling(low).mean()[-1] == price_data.rolling(high).mean()[-1]:
        signal = "Neutral"
    else:
        signal_boolean = (price_data.rolling(low).mean() > price_data.rolling(high).mean())[-1]
        if signal_boolean == True:
            signal = "Buy"
        else:
            signal = "Sell"
            
    return signal


def ADL(df):
    """
    Accumulation Distribution
    
    Input:
        - df with low, high, close and volume
    """
    money_flow_multiplier = ((df.close-df.low)-(df.high-df.close)) / (df.high-df.low) 
    money_flow_volume = money_flow_multiplier * df.volume
    ADL = money_flow_volume.cumsum()
    return ADL


def plot_ADL(df):
    """
    Plot ADL against close price curve
    Input:
        - df is DataFrame with open low,high, close
    """
    fig, ax1 = plt.subplots()
    
    #ax1.plot(ADL(df))
    ax1 = ADL(df).plot()
    ax1.set_ylabel("ADL")
    
    ax2 = ax1.twinx()
    ax2.plot(df.close, color = "red")
    ax2.set_ylabel("Price")
    
    fig.tight_layout()


def plot_OCHL(df, up = "b", down = "r", grid_on = True):
    

    #Reset the index to remove Date column from index
    df_ohlc = df.reset_index()
    
    #Naming columns
    df_ohlc.columns = ["Date","Open","High",'Low',"Close", "Volume"]
    
    #Converting dates column to float values
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    
    #Making plot
    fig = plt.figure()
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1) #CHECK WHAT IS THIS FUNCTION?
    ax1.grid(True)
    #Converts raw mdate numbers to dates
    ax1.xaxis_date()
    plt.xlabel("Date")
    #print(df_ohlc)
    
    #Making candlestick plot
    finplt.candlestick_ohlc(ax1,df_ohlc.values,width=1, colorup='g', colordown='k',alpha=0.75)
    plt.ylabel("Price")
    plt.gcf().autofmt_xdate(rotation=90, ha="center")
    plt.legend()
    
    main_data.plot()
   # plt.show()
    
fig = plt.figure()
ax1 = plt.subplot2grid((5,4), (0,0), rowspan = 4, colspan = 4)
ax1.plot(df.index, df.open)
ax1.plot(df.index, df.high)
ax1.plot(df.index, df.low)
ax1.plot(df.index, df.close)
plt.ylabel("Stock price")
ax1.grid(True)
plt.gcf().autofmt_xdate(rotation=90, ha="center")

ax2 = plt.subplot2grid((5,4), (4,0), rowspan = 1, colspan = 4, sharex = ax1)
ax2.bar(df.index, df.volume)
plt.ylabel("Volume")
ax2.grid(True)
plt.gcf().autofmt_xdate(rotation=90, ha="center")

ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))


if __name__ == "__main__":

    plot_data(df.close)
    
    # DataFrames
    raw_df = df #We usually use closing prices for all analysis, therefore main_data = df.close
    main_data = pd.DataFrame(df.close, index = df.index)
    main_price = pd.DataFrame(df.close, index = df.index)
    main_returns = log_return(main_data)
    
    
    # MA 
    main_data["MA20"] = main_price.close.rolling(20).mean()
    main_data["MA50"] = main_price.close.rolling(50).mean()
    main_data["MA200"] = main_price.close.rolling(200).mean()

    # RSI 
    main_data["RSI"] = RSI(main_price)
    #plot_RSI(main_data.RSI)
    ax = main_data.RSI.plot()
    ax.axhline(70, color = "r")
    ax.axhline(30, color = "r")
    
    RSI_signal(main_data.RSI) 
    
    plot_OCHL(df)
    
    
    plot_data(main_data)
