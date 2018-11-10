# -*- coding: utf-8 -*-
"""
Created on Wed Nov 07 00:25:45 2018

@author: Patrick

Useful links:
    # Count variables in dataframe Variable counter
    "https://stackoverflow.com/questions/29791785/python-pandas-add-a-column-to-my-dataframe-that-counts-a-variable"

DESCRIPTION OF APPROACH 1:
    1. Perform all clustering methods
    2. Create df with sharpe and all clusters as columns
    3. For each cluster in each cluster_method
        - Find max OR
        - Find min
        - Append to count dataframe
    4. Cont how many times a certain stock is in each cluster.
    5. Take stocks with n highest counts and (2nd) highest sharpe ratio
    
Todo:
    ADD MORE CLUSTERING METHODS.
    
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

def get_cluster(df, cluster_method):
        """
        df is the dataframe with cluster beloning and sharpe ratio.
        cluster is the name of the cluster method in df e.g.
        
        df = df_res
        cluster_method = df_res.columns[1]
        
        """
        df_sub = df.iloc[0:,
                    [df.columns.get_loc("Sharpe"),
                     df.columns.get_loc(cluster_method)]]
    return df_sub

# Find max sharpe in each cluster for all different methods
def findMax(df, criteria = "sharpe"):
    """
    Find the max of the criteria variable in each cluster
    for all the methods (columns) in df with cluster belonging.
 
    default critera is risk adjusted return or sharpe ratio - sharpe 
        
    df - dataframe with criteria and clusterings
        
    NOTE: all cluster methods should have same amount of clusters
          last columns should be a clustering method
              
    DataFrame format:
    - Cluster methods should be columns.
    - Stocks should be indices.
    """
    # all cluster methods should give same amount of clusters
    # last column should be cluster
    clusters = len(df_res[df_res.columns[-1]].unique()) 
    
    df_count = pd.DataFrame()
    for i in range(1,len(df.columns)):
        # find the stock with highest sharpe for each cluster method
        cluster_method = df.columns[i]
        #cluster_n = 1
        for cluster_n in range(clusters):
            df_temp = df.loc[df[criteria] == df
                       .loc[df[cluster_method] == cluster_n]
                       [criteria].max()]
            df_count = df_count.append(df_temp)
    return df_count

# Find max sharpe in each cluster for all different methods
def findMin(df, criteria = "sharpe"):
    """
    Find the max of the criteria variable in each cluster
    for all the methods (columns) in df with cluster belonging.
 
    default critera is risk adjusted return or sharpe ratio - sharpe 
        
    df - dataframe with criteria and clusterings
        
    NOTE: all cluster methods should have same amount of clusters
          last columns should be a clustering method
              
    DataFrame format:
    - Cluster methods should be columns.
    - Stocks should be indices.
    """
    # all cluster methods should give same amount of clusters
    # last column should be cluster
    clusters = len(df_res[df_res.columns[-1]].unique()) 
    
    df_count = pd.DataFrame()
    for i in range(1,len(df.columns)):
        # find the stock with highest sharpe for each cluster method
        cluster_method = df.columns[i]
        #cluster_n = 1
        for cluster_n in range(clusters):
            df_temp = df.loc[df[criteria] == df
                       .loc[df[cluster_method] == cluster_n]
                       [criteria].min()]
            df_count = df_count.append(df_temp)
    return df_count
    

if __name__=="__main__":    
    # Data Pre-processing
    datasets = ["russel3000.csv", "test_set.csv"]
    df = pd.read_csv(datasets[0],  index_col = 0)
    df = df.dropna(axis=1) #removes all stocks with incomplete time series
    df = df.sample(300, axis=1)
    
    df_pct = df.pct_change()
    df_pct = df_pct.transpose()
    df_pct = df_pct.dropna(axis = 1)
    df_log_ret = np.log(df) - np.log(df.shift(1))
    df_log_ret = df_log_ret.transpose()
    df_log_ret = df_log_ret.dropna(axis = 1)

    df_res = pd.DataFrame()
    df_res["sharpe"] = sharpeRatio(df_log_ret)
    
    
    clusters = 30
    portfolio_components = clusters
    # Perform the different hierarchical clustering and append cluster belonging to df
    linkage = ["ward", "complete", "average"] # chaining phenomenon in single
    distance_measure = ["correlation", "cosine"]
    
    # append the cluster-belongings of each type of Hierarchical clustering to df_res
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
    
    df_count = findMax(df_res, criteria = "sharpe")
    df_count = findMin(df_res, criteria = "sharpe")
            
    
    # Count variables, sort, drop duplicates and take top votes stocks as components
    # Count variables in dataframe Variable counter
    "https://stackoverflow.com/questions/29791785/python-pandas-add-a-column-to-my-dataframe-that-counts-a-variable"
    df_count["count"] = df_count.groupby(df_count.index)["sharpe"].transform("count")
    df_count.sort_values(["count", "sharpe"], ascending = [False, False], inplace = True)
    df_count.drop_duplicates(inplace = True)
    stocks = df_count.head(portfolio_components).index
    
    df_stocks = df_log_ret[df_log_ret.index.isin(stocks)] #top 30 stocks
    df_stocks.transpose().cumsum().plot()