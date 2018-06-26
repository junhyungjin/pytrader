#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 17:05:43 2018

@author: hjjun
"""
import datetime
import numpy as np
from bs4 import BeautifulSoup

def get_financial_statements(code):
    url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=%s&fin_typ=0&freq_typ=Y" % (code)
    print(url)
    
def get_estimated_dividend_yield(code):
    df = get_financial_statements(code)
    dividend_yield = df.ix["현금배당수익률"]
    
    now = datetime.datetime.now()
    cur_year = now.year
    
    if str(cur_year) in dividend_yield.index:
        cur_year_dividend_yield = dividend_yield[str(cur_year)]
        if np.isnan(cur_year_dividend_yield):
            return dividend_yield[str(cur_year-1)]
        else:
            return cur_year_dividend_yield
    else:
        return dividend_yield[str(cur_year-1)]
    
    
def get_3year_treasury():
    url = "http://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=288401&amp;idx_cd=2884&amp;freq=Y&amp;period=1998:2017"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    tr_data = soup.find_all('tr', id='tr_288401_1')
    td_data = tr_data[0].find_all('td')
    
    treasury_3year = {}
    start_year = 1998
    
    for x in td_data:
        treasury_3year[start_year] = x.text
        start_year += 1
    
    #print(treasury_3year)
    return treasury_3year
       
def get_dividend_yield(code):
    url = "http://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd=" + code
    html = requests.get(url).text
    
    soup = BeautifulSoup(html, 'lxml')
    td_data = soup.find_all('td', {'class': 'cmp-table-cell td0301'})
    dt_data = td_data[0].find_all('dt')
    
    dividend_yield = dt_data[5].text
    dividend_yield = dividend_yield.split(' ')[1]
    dividend_yield = dividend_yield[:-1]
    
    return dividend_yield
    
    
if __name__ == "__main__":
    get_3year_treasury()
    dividend_yield = get_dividend_yield('058470')
    print(dividend_yield)
    esstimated_dividend_yield = get_estimated_dividend_yield('058470')
    print(estimated_dividend_yield)