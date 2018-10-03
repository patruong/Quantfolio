# -*- coding: utf-8 -*-
"""
Created on Wed Oct 03 22:12:15 2018

@author: Patrick
"""


"""
Markowitz Portfolio Optimization
blog.quantopian.com/markowitz-portfolio-optimization-2
"""

#from __future__ import print_function

#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import cvxopt as opt
from cvxopt import blas,solvers
import pandas as pd

def rand_weights(n):
    " Produces n random weights that sum to 1 "
    k = np.random.rand(n)
    return (k / sum(k))

#print rand_weights(n_assets)

def random_portfolio(returns):
    " Returns the mean and standard deviation for a random portfolio"
    
    p = np.asmatrix(np.mean(returns, axis = 1))
    w = np.asmatrix(rand_weights(returns.shape[0]))
    C = np.asmatrix(np.cov(returns))
    
    mu = w * p.T
    sigma = np.sqrt(w * C * w.T)
    
    # This recursion reduces outliers to keep plots pretty
    if sigma > 2:
        return random_portfolio(returns)
    return mu, sigma


def optimal_portfolio(returns):
    n = len(returns)
    returns = np.asmatrix(returns)
    
    N = 100
    mus = [10**(5.0 * t / N - 1.0) for t in range(N)]
    
    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(returns))
    pbar = opt.matrix(np.mean(returns, axis = 1))
    
    # Create constraint matrices
    G = -opt.matrix(np.eye(n)) # negative identitity matrix
    h = opt.matrix(0.0, (n, 1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)
    
    # Calculate efficient frontier weights using quadratic programming
    # We have linear component -pbar negative because we do not 
    # want to account for return twice mu and -pbar
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)["x"] 
                    for mu in mus]
    
    ## CALCULATE RISK AND RETURNS FOR FRONTIER
    returns = [blas.dot(pbar, x) for x in portfolios]
    risks = [np.sqrt(blas.dot(x, S*x)) for x in portfolios]
    
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    m1 = np.polyfit(returns, risks, 2)
    x1 = np.sqrt(m1[2] / m1[0])
    
    ## CALCULATE THE OPTIMAL PORTFOLIO
    wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
    return np.asarray(wt), returns, risks, portfolios

