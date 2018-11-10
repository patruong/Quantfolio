# -*- coding: utf-8 -*-
"""
Created on Wed Nov 07 00:25:45 2018

@author: Patrick

Todo:
    - get visual clustering to list, so can use for further processing
    - implement information ratio as risk-adjusted return

1. implement multiple clustering procedures
2. compute highest risk-adjusted return of x clusters, where x is the desired number of stocks in portfolio.
(2.1) compute optimal number of x
3. compute highest risk-adjusted return stock in x clusters
4. calculate number of times stock is represented as best stock in cluster.
5. use highest voted stocks, which never occur in same cluster as portfolio component OR use highest voted stocks as components.
"""

import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from sklearn.cluster import AgglomerativeClustering

import plot_dendrogram


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


def plot_dendrogram(model, **kwargs):
    # Authors: Mathew Kallada
    # License: BSD 3 clause
    """
    =========================================
    Plot Hierarachical Clustering Dendrogram 
    =========================================
    This example plots the corresponding dendrogram of a hierarchical clustering
    using AgglomerativeClustering and the dendrogram method available in scipy.
    """
    # Children of hierarchical clustering
    children = model.children_

    # Distances between each pair of children
    # Since we don't have this information, we can use a uniform one for plotting
    distance = np.arange(children.shape[0])

    # The number of observations contained in each cluster level
    no_of_observations = np.arange(2, children.shape[0]+2)

    # Create linkage matrix and then plot the dendrogram
    linkage_matrix = np.column_stack([children, distance, no_of_observations]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)
               
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
    


def clusterHierarchical(df, n_clusters, distance, linkage):
        model = AgglomerativeClustering(n_clusters = n_clusters,
                                     affinity = distance,
                                     linkage = linkage)
        clustering = model.fit(df)
        return clustering

if __name__=="__main__":    
    # Data Pre-processing
    datasets = ["russel3000.csv", "test_set.csv"]
    df = pd.read_csv(datasets[0],  index_col = 0)
    df = df.dropna(axis=1) #removes all stocks with incomplete time series
    df = df.sample(300, axis=1)
    df = df.transpose()
    df_pct = df.pct_change()
    df_pct = df_pct.dropna(axis = 0)
    df_log_ret = np.log(df) - np.log(df.shift(1))
    df_log_ret = df_log_ret.dropna(axis = 0)

    df_res = pd.DataFrame()
    df_res["Sharpe"] = sharpeRatio(df_log_ret)
    
    clusters = 30
    linkage = ["ward", "complete", "average"] # chaining phenomenon in single
    distance_measure = ["correlation", "cosine"]

    
    for link in linkage:
        if link == "ward":
            dist = "euclidean"
            clustering = clusterHierarchical(df = df_log_ret,
                                             n_clusters = clusters,
                                             distance = dist,
                                             linkage = link)
            col_name = "HC_"+link+"_"+dist
            df_res[col_name] = np.transpose(clustering.labels_)
            continue
        for dist in distance_measure:
            clustering = clusterHierarchical(df = df_log_ret,
                                             n_clusters = clusters,
                                             distance = dist,
                                             linkage = link)
            col_name = "HC_"+link+"_"+dist
            df_res[col_name] = np.transpose(clustering.labels_)
    
            
