# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 00:13:16 2018

@author: Patrick
"""

import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import unicodedata

def get_AvanzaWarrantList():
    """
    Function to scrape avanza warrant list.
    """
    url = "https://www.avanza.se/borshandlade-produkter/warranter-torg/lista.html"
    
    response = urllib2.Request(url)
    page = urllib2.urlopen(response)
    soup = BeautifulSoup(page, "html.parser")
    
    #print(soup.prettify())
    table = soup.find("select", {"class":"underlyingInstrument chosen-items"})
    
    unicode_str = table.get_text()
    table_str = unicodedata.normalize("NFKD", unicode_str).encode("ascii", "ignore")
    avanza_list = table_str.split("\n")
    avanza_list.pop()
    avanza_list.pop(0)
    
    df = pd.DataFrame(avanza_list, columns = ["Warrants"])
    return df

def main():
    df = get_AvanzaWarrantList()
    df.to_csv("Avanza_warrantList.csv", index = False)

if __name__ == "__main__":
    main()
