import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fmin_df = pd.read_csv("/Users/hjjun/pytrader/A233740_5min_cybos.csv", index_col=[0], parse_dates=True)
day_df = fmin_df.resample('D').apply({'Open':'first', 'High':'max','Low':'min','Close':'last', 'Vol':'last'})
day_df.dropna(inplace=True)    

fig = plt.figure(figsize=(12,8))

top_axes = plt.subplot2grid((4,4),(0,0), rowspan=3, colspan=4)
bottom_axes = plt.subplot2grid((4,4),(3,0), rowspan=1, colspan=4)
bottom_axes.get_yaxis().get_major_formatter().set_scientific(False)

top_axes.plot(day_df.index, day_df['Close'], label='Close')
bottom_axes.plot(day_df.index, day_df['Vol'])

plt.tight_layout()
plt.show()