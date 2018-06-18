import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf
import matplotlib.ticker as ticker

fmin_df = pd.read_csv("/Users/hjjun/pytrader/A233740_5min_cybos.csv", index_col=[0], parse_dates=True)
day_df = fmin_df.resample('M').apply({'Open':'first', 'High':'max','Low':'min','Close':'last', 'Vol':'last'})
day_df = day_df[day_df['Vol']>0]

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)

day_loc = []
day_list = []

for i, day in enumerate(day_df.index):
    if day.dayofweek == 0:
        day_loc.append(i)
        day_list.append(day.strftime('%Y-%m-%d'))

ax.xaxis.set_major_locator(ticker.FixedLocator(day_loc))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(day_list))

mpf.candlestick2_ohlc(ax, day_df['Open'], day_df['High'], day_df['Low'], day_df['Close'], width=0.5, colorup='r', colordown='b')

plt.grid()
plt.show()