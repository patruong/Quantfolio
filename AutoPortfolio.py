# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 21:42:00 2018

@author: Patrick

# BASIC SCRIPT CLUSTER WITH CORRELATION AND OPTIMIZE
"""

import pandas as pd
import numpy as np
import sklearn.cluster as cluster
import time
import matplotlib.pyplot as plt
import pandas_datareader.data as web

def sharpeRatio(returns, riskFree_rate = 0.01):
    """
    Sharpe ratio - risk-adjusted return for daily data
    """
    years = len(returns.columns)/252
    rf = riskFree_rate*years
    mu = returns.mean(axis=1)
    std = returns.std(axis=1)
    sharpe = (mu-rf)/std
    return sharpe

def standardize(df):
    df = (df - df.mean())/df.std()
    return df

def corrDist(df):
    dist = 1 - df.corr()
    return dist

def printClusters(df_res, t=1):
    for i in range(clusters):
        print(df_res[df_res["cluster"] == i])
        time.sleep(t)
        
## LOAD IN DATA    
datasets = ["russel3000.csv", "test_set.csv"]
df = pd.read_csv(datasets[0],  index_col = 0)
df = df.dropna(axis=1) #removes all stocks with incomplete time series
df = df.sample(100, axis=1)


GS = web.DataReader("GS", 'quandl', '2018-08-30', '2018-10-30')
SBUX = web.DataReader("SBUX", 'quandl', '2018-08-30', '2018-10-30')
#NXPI = web.DataReader("NXPI", 'quandl', '2018-08-30', '2018-10-30')
#SFIX = web.DataReader("SFIX", 'quandl', '2018-08-30', '2018-10-30')
#JNJ = web.DataReader("JNJ", 'quandl', '2018-08-30', '2018-10-30')
#BRK = web.DataReader("BRK", 'quandl', '2018-08-30', '2018-10-30')
CNC = web.DataReader("CNC", 'quandl', '2018-08-30', '2018-10-30')
#SFM = web.DataReader("SFM", 'quandl', '2018-08-30', '2018-10-30')
DWDP = web.DataReader("DWDP", 'quandl', '2018-08-30', '2018-10-30')
FB = web.DataReader("FB", 'quandl', '2018-08-30', '2018-10-30')
AAPL = web.DataReader("AAPL", 'quandl', '2018-08-30', '2018-10-30')



df_pct = df.pct_change()
df_pct = df_pct.transpose()
df_pct = df_pct.dropna(axis = 1)
df_log_ret = np.log(df) - np.log(df.shift(1))
df_log_ret = df_log_ret.transpose()
df_log_ret = df_log_ret.dropna(axis = 1)

# Create a results df
df_res = pd.DataFrame()
df_res["sharpe"] = sharpeRatio(df_log_ret)

# Clustering
df_standardized = standardize(df_log_ret.transpose()) 
clusters = 10
dist = corrDist(df_standardized)
HC = cluster.AgglomerativeClustering(affinity='precomputed', 
                                     compute_full_tree='auto',
                                     connectivity=None, linkage='average', 
                                     memory=None, n_clusters=clusters,
                                     pooling_func='deprecated')
clustering = HC.fit(dist)
df_res["cluster"] = clustering.labels_

# find best sharpe stock in each cluster
def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)

stock_list = []
for i in range(clusters):
    topSharpe = df_res[df_res["sharpe"] == df_res[df_res["cluster"] == i]["sharpe"].max()]
    topSharpe = topSharpe[topSharpe["cluster"] == i]
    stock = topSharpe.index
    stock_list.append(stock[0])
    
# mean-variance portfolio 
df_portfolio = df_log_ret.transpose()[stock_list]

def randomPortfolio(returns):
    """
    returns - df_portfolio
    """
    p = returns.mean()
    w = pd.Series(rand_weights(returns.columns.shape[0]), index = returns.columns)
    S = returns.corr()
    
    mu = np.dot(w,p)
    sigma = np.sqrt(np.dot(w.T, np.dot(S, w)))
    return mu, sigma

def generateRandomPortfolios(returns, n_portfolios = 500):
    """
    returns - df_portfolio
    """
    n_portfolios = n_portfolios
    means, stds = np.column_stack([
        randomPortfolio(returns) 
        for _ in range(n_portfolios)
    ])
    return means, stds

means, stds = generateRandomPortfolios(df_portfolio, n_portfolios = 500)
#plt.plot(stds, means, 'o', markersize=5)
#plt.xlabel('std')
#plt.ylabel('mean')
#plt.title('Mean and standard deviation of returns of randomly generated portfolios')

# Portfolio Optimization
import cvxopt as opt
from cvxopt import blas, solvers

def optimal_portfolio(returns):
    """
    
    """
    n = len(returns)
    returns = np.asmatrix(returns)
    
    N = 100
    mus = [10**(5.0 * t/N - 1.0) for t in range(N)]
    
    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(returns))
    pbar = opt.matrix(np.mean(returns, axis=1))
    
    # Create constraint matrices
    G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
    h = opt.matrix(0.0, (n ,1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)
    
    # Calculate efficient frontier weights using quadratic programming
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x'] 
                  for mu in mus]
    ## CALCULATE RISKS AND RETURNS FOR FRONTIER
    returns = [blas.dot(pbar, x) for x in portfolios]
    risks = [np.sqrt(blas.dot(x, S*x)) for x in portfolios]
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    m1 = np.polyfit(returns, risks, 2)
    x1 = np.sqrt(m1[2] / m1[0])
    # CALCULATE THE OPTIMAL PORTFOLIO
    wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
    return np.asarray(wt), returns, risks, portfolios

weights, returns, risks, portfolios = optimal_portfolio(df_portfolio.T)

plt.plot(stds, means, 'o')
plt.ylabel('mean')
plt.xlabel('std')
plt.plot(risks, returns, 'y-o')