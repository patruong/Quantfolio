# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 16:55:34 2018

@author: Patrick

Libraries for finance
https://financetrain.com/best-python-librariespackages-finance-financial-data-scientists/
https://www.linkedin.com/pulse/best-python-librariespackages-finance-financial-data-majid-aliakbar/
https://www.quora.com/What-are-good-Python-packages-for-Portfolio-Analysis-of-activity
https://github.com/wilsonfreitas/awesome-quant
"""

import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime 
import time



# Log-return form raw prices
def Log_returns(df):
    ""
    df_ret = pd.DataFrame(data = np.log(df[1:].values/df[:-1].values), 
                          index = df[1:].index, 
                          columns = df.columns)
    return df_ret


# Plot cumulative returns:
def Plot_cumsum(df):
    df.cumsum().plot()

# Cumulative returns
def Cumulative_returns(df_log, sort = True):
    "df_log - dataframe of log returns"
    df_cumsum = df_log.cumsum().tail(1).transpose()
    if sort == True:
        df_sorted_cumsum = df_cumsum[df_cumsum.columns[0]].sort_values(ascending = False)
        return df_sorted_cumsum
    else:
        return df_cumsum[df_cumsum.columns[0]]

# Average returns
def Average_returns(df_log, sort = True):
    "df_log - dataframe of log returns"
    if sort == True:
        return df_log.mean().sort_values(ascending = False)
    else:
        return df_log.mean()

# Standard deviation - Volatility of returns
def Volatility_returns(df_log, sort = True):
    "df_log - dataframe of log returns"
    if sort == True:
        return df_log.std().sort_values(ascending = False)
    else:
        return df_log.std()
    
# Sharpe Ratio 
def SharpeRatio(df_log, rf = 1.02, days_per_year = 365, sort = True):
    "365 days is often used for risk-free rate"
    "df_log - log returns"
    # Convert yearly rf to daily rf
    log_rf = np.log(rf)
    daily_log_rf = log_rf/days_per_year
    df_rf = daily_log_rf
    
    #mean daily return - daily rf
    sharpeRatio = (df_log.mean()-df_rf)/df_log.std() 
    if sort == True:
        return sharpeRatio.sort_values(ascending = False)
    else:
        return sharpeRatio
    
# Maximum Draw down
def Maximum_Drawdown(df_log, sort = True):
    if sort == True:
        return (-(1-np.exp(df_log.min()))).sort_values(ascending=True)
    else:
        return (-(1-np.exp(df_log.min())))


# Covariance matrix
#df_log.corr()



if __name__ == "__main__":
    """
    start = datetime.datetime(2015, 2 ,9)
    end = datetime.datetime(2017,5,24)
    
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
    """
    df_logRet = Log_returns(df)
    
    stats_df = pd.DataFrame()
    stats_df["Cumulative Returns"] = Cumulative_returns(df_logRet)
    stats_df["Average Returns"] =  Average_returns(df_logRet)
    stats_df["Volatility"] = Volatility_returns(df_logRet)
    stats_df["Sharpe Ratio"] = SharpeRatio(df_logRet)
    stats_df["Maximum Drawdown"] = Maximum_Drawdown(df_logRet)
