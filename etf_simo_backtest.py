import pandas as pd
import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
START_MONEY = 100000000

fig, ax = plt.subplots()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.set_title('KOSDAQ(LEV) SIMO')

def buy(buy_price, money):
    amt = money / buy_price
    return 0, amt

def sell(sell_price, amt):
    money = sell_price * amt
    return money, 0

def plot_coin():
    fig.autofmt_xdate()
    plt.legend(['simo'], loc='upper left')
    plt.show()
    
def process():
    fmin_df = pd.read_csv("/Users/hjjun/pytrader/A233740_5min_cybos.csv", index_col=[0], parse_dates=True)
    day_df = fmin_df.resample('D').apply({'Open':'first', 'High':'max','Low':'min','Close':'last'})
    day_df.dropna(inplace=True)
    day_df['T_Open'] = day_df['Open'].shift(-1)
    money = START_MONEY
    
    for i, r in day_df.iterrows():
        one_pm_dt = i + datetime.timedelta(hours=12)
        if day_df.loc[i, 'Open'] < fmin_df.loc[one_pm_dt, 'Open']:
            money, amt = buy(fmin_df.loc[one_pm_dt, 'Open'], money)
            money, amt = sell(day_df.loc[i, 'T_Open'], amt)
            day_df.loc[i, 'Equity'] = money
        else:
            day_df.loc[i, 'Equity'] = money
    
    ax.plot(day_df.index, day_df['Equity'])
    print(day_df['Equity'].tail())
    
process()
plot_coin()
