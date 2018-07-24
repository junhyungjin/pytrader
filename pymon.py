import sys
import time
from pandas import DataFrame
import datetime
import webreader
import numpy as np

class PyMon:
    
    def __init__(self):
        df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
        df.종목코드 = df.종목코드.map('{:06d}'.format)
        kospi_codes = df[["회사명","종목코드"]]
        
        
    def update_buy_list(self, buy_list):
        f = open("buy_list.txt", "wt")
        for code in buy_list:
            f.writelines("매수;", code, ";시장가;10;0;매수전")
        f.close()

    def run(self):
        buy_list = []
        num = len(self.kosdaq_codes)

        for i, code in enumerate(self.kosdaq_codes):
            print(i, '/', num)
            if self.check_speedy_rising_volume(code):
                buy_list.append(code)

        self.update_buy_list(buy_list)

def calculate_estimated_dividend_to_treasury(self, code):
    estimated_dividend_yield = webreader.get_estimated_dividend_yield(code)
    
    if np.isnan(estimated_dividend_yield):
        estimated_dividend_yield = webreader.get_dividend_yield(code)
        
        if estimated_dividend_yield == "":
            estimated_dividend_yield = 0

    current_3year_treasury = webreader.get_current_3year_treasury()
    estimated_dividend_to_treasury = float(estimated_dividend_yield) / float(current_3year_treasury)
    return estimated_dividend_to_treasury

def get_min_max_dividend_to_treasury(self, code):
    previous_dividend_yield = webreader.get_previous_dividend_yield(code)
    three_years_treasury = webreader.get_3year_treasury()
    now = datetime.datetime.now()
    cur_year = now.year
    previous_dividend_to_treasury = {}

    for year in range(cur_year-5, cur_year):
        if year in previous_dividend_yield.keys() and year in three_years_treasury.keys():
            ratio = float(previous_dividend_yield[year]) / float(three_years_treasury[year])
            previous_dividend_to_treasury[year] = ratio
    
    print(previous_dividend_to_treasury)
    min_ratio = min(previous_dividend_to_treasury.values())
    max_ratio = max(previous_dividend_to_treasury.values())

    return (min_ratio, max_ratio)

def buy_check_by_dividend_algorithm(self, code):
    estimated_dividend_to_treasury = self.calculate_estimated_dividend_to_treasury(code)
    (min_ratio, max_ratio) = self.get_min_max_dividend_to_treasury(code)

    if estimated_dividend_to_treasury >= max_ratio:
        return (1, estimated_dividend_to_treasury)
    else:
        return (0, estimated_dividend_to_treasury)
    
if __name__ == "__main__":
    pymon = PyMon()
    print(pymon.get_min_max_dividend_to_treasury('058470'))
