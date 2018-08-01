#-*-coding:utf-8

import re
import sys
import time
from pandas import DataFrame
import datetime
import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_date_str(s):
    date_str = ''
    r = re.search("\d{4}", s)
    if r:
        date_str = r.group()

    return date_str

def get_financial_statements(code):
    url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=%s&fin_typ=0&freq_typ=Y" % (code)
    
    df_list = pd.read_html(url, encoding="utf-8")
    df = df_list[0]
    df = df.set_index('주요재무정보')
    cols = list(df.columns)
    cols.remove('연간')
    cols = [get_date_str(x) for x in cols]
    df = df.ix[:, :-1]
    df.columns = cols
    
    return df

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
    
    if not td_data:
        return ""
    
    dt_data = td_data[0].find_all('dt')
    
    dividend_yield = dt_data[5].text
    dividend_yield = dividend_yield.split(' ')[1]
    dividend_yield = dividend_yield[:-1]
    
    return dividend_yield

def get_estimated_dividend_yield(code):
    df = get_financial_statements(code)
    dividend_yield = df.ix["현금배당수익률"]
    
    now = datetime.datetime.now()
    cur_year = now.year
    
    if str(cur_year) in dividend_yield.index and not np.isnan(dividend_yield[str(cur_year)]):
        return dividend_yield[str(cur_year)]
    elif str(cur_year-1) in dividend_yield.index and not np.isnan(dividend_yield[str(cur_year-1)]):
        return dividend_yield[str(cur_year-1)]
    else:
        return np.NaN
    
def get_current_3year_treasury():
    url = "http://info.finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page=1"
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml')
    tbody_data = soup.find_all('tbody')
    tr_data = tbody_data[0].find_all('tr')
    td_data = tr_data[0].find_all('td')
    return td_data[1].text
    
def get_previous_dividend_yield(code):
    df = get_financial_statements(code)
    dividend_yield = df.ix['현금배당수익률']

    now = datetime.datetime.now()
    cur_year = now.year

    previous_dividend_yield = {}

    for year in range(cur_year-5, cur_year):
        if str(year) in dividend_yield.index:
            previous_dividend_yield[year] = dividend_yield[str(year)]

    return previous_dividend_yield

def calculate_estimated_dividend_to_treasury(code):
    estimated_dividend_yield = get_estimated_dividend_yield(code)
    
    if np.isnan(estimated_dividend_yield):
        estimated_dividend_yield = get_dividend_yield(code)
        
        if estimated_dividend_yield == "":
            estimated_dividend_yield = 0

    current_3year_treasury = get_current_3year_treasury()
    estimated_dividend_to_treasury = float(estimated_dividend_yield) / float(current_3year_treasury)
    return estimated_dividend_to_treasury

def get_min_max_dividend_to_treasury(code):
    previous_dividend_yield = get_previous_dividend_yield(code)
    three_years_treasury = get_3year_treasury()
    now = datetime.datetime.now()
    cur_year = now.year
    previous_dividend_to_treasury = {}

    for year in range(cur_year-5, cur_year):
        if year in previous_dividend_yield.keys() and year in three_years_treasury.keys():
            ratio = float(previous_dividend_yield[year]) / float(three_years_treasury[year])
            previous_dividend_to_treasury[year] = ratio
    
    print(previous_dividend_to_treasury)
    if previous_dividend_to_treasury:
        min_ratio = min(previous_dividend_to_treasury.values())
        max_ratio = max(previous_dividend_to_treasury.values())
    else:
        min_ratio = 0
        max_ratio = 0

    return (min_ratio, max_ratio)
def buy_check_by_dividend_algorithm(code):
    estimated_dividend_to_treasury = calculate_estimated_dividend_to_treasury(code)
    (min_ratio, max_ratio) = get_min_max_dividend_to_treasury(code)

    if estimated_dividend_to_treasury >= max_ratio and max_ratio != 0:
        return (1, estimated_dividend_to_treasury)
    else:
        return (0, estimated_dividend_to_treasury)
    
def get_kospi_codes():
    df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
    df.종목코드 = df.종목코드.map('{:06d}'.format)
    kospi_codes = df[["회사명","종목코드"]]
    return kospi_codes
        
        
def update_buy_list(buy_list):
    f = open("buy_list.txt", "wt")
    for code in buy_list:
        f.writelines("매수;", code, ";시장가;10;0;매수전")
    f.close()
    
def run_dividend():
    
    kospi_codes = get_kospi_codes()
    buy_list = []
    top_five = []
    
    for row in kospi_codes.itertuples():
        ret = buy_check_by_dividend_algorithm(row[2])
        
        if ret[0] == 1:
            print("Buy: " + row[2] + ":" + row[1] + " " + str(ret[1]))
            print("---------------------------------------------------")
            buy_list.append((row[2], row[1], ret[1]))
        else:
            print("Don't Buy: " + row[2] + ":" + row[1] + " " + str(ret[1]))
            print("---------------------------------------------------")
            pass
    
    sorted_list = sorted(buy_list, key=lambda t:t[1], reverse=True)
    
    for i in range(0,5):
        code = sorted_list[i][0]
        top_five.append(code)
                  
    print(top_five)
    update_buy_list(top_five)
                  
if __name__ == "__main__":
    run_dividend()