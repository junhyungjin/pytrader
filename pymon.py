import datetime
import webreader
import numpy as np

def calculate_estimated_dividend_to_treasury(self, code):
    estimated_dividend_yield = webreader.get_estimated_dividend_yield(code)
    if np.isnan(estimated_dividend_yield):
        estimated_dividend_yield = webreader.get_dividend_yield(code)

    current_3year_treasury = webreader.get_current_3year_treasury()
    estimated_dividend_to_treasury = float(estimated_dividend_yield) / float(current_3year_treasury)
    return estimated_dividend_to_treasury

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    #pymon.run()
    print(pymon.calculate_estimated_dividend_to_treasury('058470'))
