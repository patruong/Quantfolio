import numpy as np
import pandas as pd

class preprocess(object):
    def log_return(self, prices):
        """ 
        Function takes price data df and convert to log-returns
        """
        logRet = np.log(prices)-np.log(prices.shift(1))        
        return logRet
    def pct_change(self, prices):
        " Function takes price df and convert to returns"
        ret = prices.pct_change()
        return red

