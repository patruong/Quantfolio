# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 23:40:51 2018

@author: Patrick

This file contains functions for computing theoretical
components.

"""

import numpy as np
import matplotlib.pyplot as plt

"""
Components from https://quantdare.com/kelly-criterion/
"""
def odds(x,y):
    """
    Function for computing payout of odds if 1 unit of currency was invested.
    
    Odds ratio x:y
    """
    payout = (x+y)/y
    return payout

#def oddsBet(betsize, x,y):
#    """
#    Function for computing payout of odds if betsize unit of currency is invested.
#    
#    Odds ratio x:y
#    """
#    
#    payout = (x*betsize + y) / y
#    return payout

def ExpectedGainOdds(p,f,c):
    """
    p - probability of win
    f - fraction of wealth invested
    odds (c:1)
    """
    ExpGain = p*np.log((c*f+1)) + (1-p)*np.log(1-f)
    return ExpGain

def optimalFraction(p,c):
    """
    Optimal fraction for ExpectedGainOdds
    
    Basically, set the derivative of ExpGain w.r.t f to 0
    """
    if p > 1/c:
        opt = (p*c-1)/(c-1)
    else:
        opt = 0
    return opt

def coinflip(p):
    "p - probability of heads"
    return 1 if np.random.uniform() < p else 0

coins = []
for i in range(bets):
    coins.append(coinflip(p))
    
bets = 2000
budget = 100
p = 0.53
c = 2
optF = optimalFraction(p,c)
bet_fractions = [optF/2, optimalFraction(p,c), optF*2, optF*4]


# Try to plot the one in kelly criterion
budget = 100
budgetList = [budget]
for i in range(len(coins)):
    if np.isnan(budget):
        print(i)
        break
    coin = coins[i]
    betsize = 0.25*budget
    budget = budget - betsize
    if coin != 0:
        payout = betsize*odds(2,1)
    else:
        payout = 0
    budget = budget + payout
    budgetList.append(budget)

df = pd.DataFrame(retList)
plt.plot(np.log(budgetList))
#returns = (budgetList[1:]/budgetList[:-1])
#accLogReturns = np.log(returns.cumsum())
#plt.plot(accLogReturns)
