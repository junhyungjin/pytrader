import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf
import matplotlib.ticker as ticker

fmin_df = pd.read_csv("/Users/hjjun/pytrader/A233740_5min_cybos.csv", index_col=[0], parse_dates=True)
day_df = fmin_df.resample('D').apply({'Open':'first', 'High':'max','Low':'min','Close':'last', 'Vol':'last'})
day_df = day_df[day_df['Vol']>0]

day_df['MA5'] = day_df['Close'].rolling(window=5).mean()
day_df['MA20'] = day_df['Close'].rolling(window=20).mean()
day_df['MA60'] = day_df['Close'].rolling(window=60).mean()

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)

ax.plot(day_df.index, day_df['Close'], label='Close')
ax.plot(day_df.index, day_df['MA5'], label='MA5')
ax.plot(day_df.index, day_df['MA20'], label='MA20')
ax.plot(day_df.index, day_df['MA60'], label='MA60')
ax.legend(loc='upper right')

plt.grid()
plt.show()