# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 00:09:19 2018

@author: Patrick
"""

import pandas as pd
import urllib2
from bs4 import BeautifulSoup

def get_SP500():
    """
    Function to scrape wikipedia and get SP500 tickers
    
    No idea to give the function parameter choice since each
    BeautifulSoup is unique to each webpage.
    """
    
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    response = urllib2.Request(url)
    page = urllib2.urlopen(response)
    soup = BeautifulSoup(page)
    
    
    
    table = soup.find("table", {"class": "wikitable sortable"})
    
    ticker_df = pd.DataFrame()
    
    tickers = []
    sectors = []
    
    for i in range(len(table.findAll("tr"))):
        i_elem = table.findAll("tr")[i]
        col = i_elem.findAll("td")
        if len(col) > 0:
            
            tickers.append(col[0].string.strip())
            sectors.append(col[3].string.strip().lower().replace(" ", "_"))  #strip() removes white space character
            
    
    ticker_df["ticker"] = tickers    
    ticker_df["sector"] = sectors
    
    return ticker_df

if __name__ == "__main__":
    tickers_df = get_SP500()
    tickers_df.to_csv("SP500-Tickers.csv", index = False, sep = ",")