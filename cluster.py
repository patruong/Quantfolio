# -*- coding: utf-8 -*-
"""
Created on Wed Nov 07 00:25:45 2018

@author: Patrick

Todo:
    - get visual clustering to list, so can use for further processing
    - implement information ratio as risk-adjusted return
"""

import pandas as pd

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np

# Data
datasets = ["russel3000.csv", "test_set.csv"]
df = pd.read_csv(datasets[1],  index_col = 0)
df = df.dropna(axis=1) #removes all stocks with incomplete time series
df = df.sample(30, axis=1)
df = df.transpose()
df_pct = df.pct_change()
df_pct = df_pct.dropna()
df_log_ret = np.log(df) - np.log(df.shift(1))
df_log_ret = df_log_ret.dropna()

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

def plot_hierarchicalClustering(data, method = "complete", metric = "correlation"):
    Z = linkage(data, method = method, metric = metric)
    
    # calculate full dendrogram
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
        labels = data.index
    )
    plt.show()

def plot_truncHierarchicalClustering(data, method = "complete", metric = "correlation"):
    """
    Todo
    - can i put labels on dots???
    """
    plt.title('Hierarchical Clustering Dendrogram (truncated)')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        Z = linkage(data, method = method, metric = metric) ,
        truncate_mode='lastp',  # show only the last p merged clusters
        p=12,  # show only the last p merged clusters
        show_leaf_counts=False,  # otherwise numbers in brackets are counts
        leaf_rotation=90.,
        leaf_font_size=12.,
        show_contracted=True,  # to get a distribution impression in truncated branches
        labels = data.index
    )
    plt.show()
    
