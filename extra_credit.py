# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 00:06:54 2015

@author: tank
"""


import numpy as np
import pandas as pd
import random as rand
import time
import math
import QLearner as ql
import matplotlib.pyplot as plt
import talib

from util import get_data



# convert the location to a single integer
def discretize(pos):
    return pos[0]*10 + pos[1]


def get_indicators(start_date, end_date, symbols):
    """Simulate and assess the performance of a stock portfolio."""
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(symbols, dates)  # automatically adds SPY
    prices = prices_all[symbols]  # only portfolio symbols
   # prices_SPY = prices_all['SPY']  # only SPY, for comparison later
   
    sym=symbols[1]
        
    x1=(prices[sym]-pd.rolling_mean(prices[sym], 20))/(2*pd.rolling_std(prices[sym],20))  
    x1_dis=pd.cut(x1, 10, labels=False)
    
    x2=prices[sym].pct_change(20)
    x2_dis=pd.cut(x2, 10, labels=False)
    x3= pd.rolling_std(prices[sym].pct_change(1),20)
    x3_dis=pd.cut(x3, 10, labels=False)
    
    #return pd.concat([x1_,x2_0,x3_0], axis=1).dropna(), prices
    tempdf=pd.concat([x1_dis,x2_dis,x3_dis], axis=1).dropna()
    tempdf.columns=['x1','x2','x3']

    print tempdf.dtypes
    
    
  
    tempdf['holding']=np.random.randint(0, 3, size=len(tempdf))
    #0 = no position , 1 = negative positin 2 =holding long
    tempdf['s']=1000*tempdf['holding']+100*tempdf['x3']+10*tempdf['x2']+ 1*tempdf['x1']
    print tempdf.head(50)
    return tempdf, prices


def cannonball_run2():
    
    # Define training input parameters
    training_start_date = '2008-01-01'
    training_end_date = '2009-12-31'
    symbols=['ML4T-399','IBM']
    indicators_training, prices_training =get_indicators(training_start_date,training_end_date,symbols)   
    prices_training['daily_return']=prices_training[symbols[1]].pct_change(1)

    
    
    
    # Define testing input parameters
    testing_start_date = '2010-01-01'
    testing_end_date = '2010-12-31'
    symbols_test=['ML4T-399','IBM']
    indicators_testing,prices_testing=get_indicators(testing_start_date,testing_end_date,symbols_test)
    prices_training['daily_return']=prices_training[symbols[1]].pct_change(1)
 
    

# run the code to test a learner
if __name__=="__main__":

 
    cannonball_run2()

  