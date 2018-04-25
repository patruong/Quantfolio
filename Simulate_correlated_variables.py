# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 01:32:38 2018

@author: Patrick
"""

import numpy as np
from matplotlib.pyplot import scatter
import matplotlib.pyplot as plt
import pandas as pd



from os import listdir
from os.path import isfile, join
from os import chdir
from os import getcwd

path = "C:\\Users\\Patrick\\Desktop\\Thesis In\\DiffMap"
chdir(path)
print(getcwd())

xx = np.array([-0.51, 51.2])
yy = np.array([0.33, 51.6])
means = [xx.mean(), yy.mean()]  
stds = [xx.std() / 3, yy.std() / 3]
corr = 0.8         # correlation
covs = [[stds[0]**2          , stds[0]*stds[1]*corr], 
        [stds[0]*stds[1]*corr,           stds[1]**2]] 

m = np.random.multivariate_normal(means, covs, 1000).T
scatter(m[0], m[1])

means = [0 , 1, 5]
corr = 0.9
covs = [[1, corr, corr],
        [corr, 1, corr],
        [corr, corr, 1]]
m = np.random.multivariate_normal(means, covs, 1000).T
scatter(m[2], m[1])

#########################################################
## Generate correlated variables multivariate Normal ####
#########################################################

n = 10
corr = 0.9
mean_min = -0.1
mean_max = 0.1
means = [np.random.randint(mean_min, mean_max) for i in range(n)]

covs = []
for i in range(n):
    corr_array = [corr for j in range(n)]
    corr_array[i] = 1
    covs.append(corr_array)
m = np.random.multivariate_normal(means, covs, 1000).T
#scatter(m[2], m[1])

df = pd.DataFrame(m.T)


#####################################################
#### Multivariate Laplace 
#####################################################

def Multivariate_Laplace(n = 20, corr = 0, mean_min = -1*10, mean_max = 1*10):
    #n = 20
    #corr = 0.9
    #mean_min = -1 * 10
    #mean_max = 1 * 10
    means = [float(np.random.randint(mean_min, mean_max))/100 for i in range(n)] # np.random.randint(-100,100)/100
    
    covs1 = []
    for i in range(n):
        corr_array = [corr for j in range(n)]
        corr_array[i] = 1
        covs1.append(corr_array)
    m_norm1 = np.random.multivariate_normal(means, covs1, 1000).T
    
    covs2 = []
    for i in range(n):
        corr_array = [corr for j in range(n)]
        corr_array[i] = 1
        covs2.append(corr_array)
    m_norm2 = np.random.multivariate_normal(means, covs2, 1000).T
    
    covs3 = []
    for i in range(n):
        corr_array = [corr for j in range(n)]
        corr_array[i] = 1
        covs3.append(corr_array)
    m_norm3 = np.random.multivariate_normal(means, covs3, 1000).T
    
    covs4 = []
    for i in range(n):
        corr_array = [corr for j in range(n)]
        corr_array[i] = 1
        covs4.append(corr_array)
    m_norm4 = np.random.multivariate_normal(means, covs4, 1000).T
    
    df1 = pd.DataFrame(m_norm1.T)
    df2 = pd.DataFrame(m_norm2.T)
    df3 = pd.DataFrame(m_norm3.T)
    df4 = pd.DataFrame(m_norm4.T)
    
    df_laplace = df1*df2 + df3*df4
    
    #"test" 
    #np.cumsum(df_laplace[9]).plot()
    #np.cumsum(df_laplace).plot()
    
    #((df_laplace.corr() - np.diag(np.ones(20))).min()).min()
    return df_laplace


#####################################################
#### Multivariate Laplace High correlation blocks and zero blocks
#####################################################

def Multivariate_Laplace_hcBlocks(n = 20, corr = 0, mean_min = -1*10, mean_max = 1*10):
    n = 10
    corr = 0.9
    mean_min = -1 * 10
    mean_max = 1 * 10
    means = [float(np.random.randint(mean_min, mean_max))/100 for i in range(n)] # np.random.randint(-100,100)/100
    
    covs1 = []
    for i in range(n):
        corr_array = [corr if j < n/2 and i < n/2 
                      else corr if j >= n/2 and i > n/2 
                      else 0 
                      for j in range(n)]
        corr_array[i] = 1
        covs1.append(corr_array)
    m_norm1 = np.random.multivariate_normal(means, covs1, 1000).T
    
    covs2 = []
    for i in range(n):
        corr_array = [corr if j < n/2 and i < n/2 
                      else corr if j >= n/2 and i > n/2 
                      else 0 
                      for j in range(n)]
        corr_array[i] = 1
        covs2.append(corr_array)
    m_norm2 = np.random.multivariate_normal(means, covs2, 1000).T
    
    covs3 = []
    for i in range(n):
        corr_array = [corr if j < n/2 and i < n/2 
                      else corr if j >= n/2 and i > n/2 
                      else 0 
                      for j in range(n)]
        corr_array[i] = 1
        covs3.append(corr_array)
    m_norm3 = np.random.multivariate_normal(means, covs3, 1000).T
    
    covs4 = []
    for i in range(n):
        corr_array = [corr if j < n/2 and i < n/2 
                      else corr if j >= n/2 and i > n/2 
                      else 0 
                      for j in range(n)]
        corr_array[i] = 1
        covs4.append(corr_array)
    m_norm4 = np.random.multivariate_normal(means, covs4, 1000).T
    
    df1 = pd.DataFrame(m_norm1.T)
    df2 = pd.DataFrame(m_norm2.T)
    df3 = pd.DataFrame(m_norm3.T)
    df4 = pd.DataFrame(m_norm4.T)
    
    df_laplace = df1*df2 + df3*df4
    return df_laplaced

"test" 
#np.cumsum(df_laplace[9]).plot()
#np.cumsum(df_laplace).plot()

#((df_laplace.corr() - np.diag(np.ones(20))).min()).min()


################################
### Simulate variables #########
################################

#n = 20
for i in range(0,100+1):
    for j in range(5, 50+1,5):
        #sims = Multivariate_Laplace(n=j, corr = float(i)/100)
        sims = Multivariate_Laplace_hcBlocks(n=j, corr = float(i)/100)
        sim_str = "HCsims_n"+str(j)+"_corr"+str(i)+".csv"
        sims.to_csv(sim_str, index = False, sep = ",")