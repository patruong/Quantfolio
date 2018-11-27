# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 00:43:13 2018

@author: Patrick

Clustering Approach 2
    - Cluster stocks
    - For each cluster find stock with highest(max) and lowest(min) sharpe.
    - Append to count dataframe
        - max, max_stock, min, min_stock, cluster
    (- Reiterade for all clustering algorithms)

The idea is that each clusters have stocks that behave similarily within,
but dissimilar between clusters. We then want to short the worst case 
in each cluster and long best case, to get a market neutral strategy.



"""


import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from sklearn.cluster import AgglomerativeClustering

import random
random.seed(555)

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
               
    
def clusterHierarchical(df, n_clusters, distance, linkage):
        model = AgglomerativeClustering(n_clusters = n_clusters,
                                     affinity = distance,
                                     linkage = linkage)
        clustering = model.fit(df)
        return clustering

def addCluster(df, clustering):
        """
        Function takes dataframe and adds cluster column
        """
        df["cluster"] = clustering.labels_
        return df
    
if __name__=="__main__":    
    # Data Pre-processing
    datasets = ["russel3000.csv", "test_set.csv"]
    df = pd.read_csv(datasets[0],  index_col = 0)
    df = df.dropna(axis=1) #removes all stocks with incomplete time series
    df = df.sample(100, axis=1)
    
    df_pct = df.pct_change()
    df_pct = df_pct.transpose()
    df_pct = df_pct.dropna(axis = 1)
    df_log_ret = np.log(df) - np.log(df.shift(1))
    df_log_ret = df_log_ret.transpose()
    df_log_ret = df_log_ret.dropna(axis = 1)

    # Create a results df
    df_res = pd.DataFrame()
    df_res["sharpe"] = sharpeRatio(df_log_ret)
    
    ##############
    # Clustering #
    ##############
    
    clusters = 5
    portfolio_components = clusters

    linkage = "complete"
    distance_measure = "correlation"
    
    # append the cluster-belongings of each type of Hierarchical clustering to df_res
    clustering = clusterHierarchical(df = df_log_ret,
                                     n_clusters = clusters,
                                     distance = distance_measure,
                                     linkage = linkage)
    
    df_res = addCluster(df_res, clustering)
    
    ####################################
    # Find min and max of each cluster #
    ####################################
    
    def ClusterMinMax(df, drop_singletons == True):
        """
        df - input from addCluster
        drop_singletons - drop singleton clusters from df.
        
        NOT FINISHED
        """
        clusters = len(df_res[df_res.columns[-1]].unique()) 
        criteria = "sharpe"
        
        df_group = pd.DataFrame(columns=["cluster", "max", "min"])
        for i in range(clusters):
                
            group = i
            group_max = df_res.loc[df_res["cluster"] == group].max()["sharpe"]
            group_max_stock = df_res[df_res["sharpe"] == df_res.loc[df_res["cluster"] == group].max()["sharpe"]].index[0]
            group_min = df_res.loc[df_res["cluster"] == group].min()["sharpe"]
            group_min_stock = df_res[df_res["sharpe"] == df_res.loc[df_res["cluster"] == group].min()["sharpe"]].index[0]
            df_group = df_group.append({"cluster": int(group), 
                                        "max":group_max, 
                                        "min":group_min,
                                        "TICKER_max":group_max_stock,
                                        "TICKER_min":group_min_stock}, ignore_index = True)
        if drop_singletons == True:        
            #drop singleton clusters
            df_group = df_group[df_group["min"] != df_group["max"]]
        return df_group
    #######################################
    # Calculate distance between clusters #
    #######################################
    """
    Look in to mahalanobis distance clustering of stocks.
    """
    import seaborn as sns; sns.set(color_codes = True)
    g = sns.clustermap(df_log_ret.transpose(), metric = "correlation")
    
    # Give sns.clustermap a pre-computed distance matrix
    #https://stackoverflow.com/questions/38705359/how-to-give-sns-clustermap-a-precomputed-distance-matrix
    
    import pandas as pd, seaborn as sns
    import scipy.spatial as sp, scipy.cluster.hierarchy as hc
    from sklearn.datasets import load_iris
    sns.set(font="monospace")
    
    iris = load_iris()
    X, y = iris.data, iris.target
    DF = pd.DataFrame(X, index = ["iris_%d" % (i) for i in range(X.shape[0])], columns = iris.feature_names)
    
    DF_corr = DF.T.corr()
    DF_dism = 1 - DF_corr   # distance matrix
    linkage = hc.linkage(sp.distance.squareform(DF_dism), method='average')
    sns.clustermap(DF_dism, row_linkage=linkage, col_linkage=linkage)
        
    ############
    # Plotting #
    ############
    
    plt.title('Hierarchical Clustering Dendrogram')
    plot_dendrogram(clustering, labels=clustering.labels_)
    plt.show()
    
    