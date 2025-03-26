import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from pathlib import Path
import numpy as np


matplotlib.use("TkAgg")

def loadPrices(fileName):
    dat = pd.read_csv(fileName, index_col=0)
    dat.index = pd.DatetimeIndex(dat.index)
    # dat['dat_int'] = np.array(list(range(1, len(dat) + 1))) / 10
    return dat


def normalizeValues(table, newColumn, existingColum):
    priceAtT0 = table.iloc[0][existingColum]
    table[newColumn] = table.apply(lambda row: (row[existingColum] / priceAtT0), axis=1)
    return table

path_csv_BYN = a = Path(__file__).parent.joinpath('byn').joinpath("USDBYN2010_2020.csv")
usdByn = loadPrices(path_csv_BYN)
usdByn = normalizeValues(usdByn, 'procent', 'price')

Xaxis = usdByn.index
Yaxis = usdByn['procent'].values

Y_max = usdByn[usdByn['procent'] == usdByn['procent'].max()]


plt.plot(Xaxis, Yaxis, 'black')
plt.axvline(date(2010, 12, 19), c='red')
plt.axvspan(date(2010, 6, 19), date(2010, 12, 19), alpha=0.3)
plt.axvline(date(2015, 10, 11), c='red')
plt.axvspan(date(2015, 4, 11), date(2015, 10, 11), alpha=0.3)
plt.axvline(date(2020, 8, 9), c='red')
plt.axvspan(date(2020, 2, 9), date(2020, 8, 9), alpha=0.3)
max_price = usdByn.loc[Y_max.index[0]]
plt.axhline(max_price['procent'], label='{:.3f} BYN, {}'.format(max_price['price'], Y_max.index[0].date()))
plt.legend(loc='upper left')

plt.grid()
plt.show()






# import datetime as dt
# data_df['Date'] = pd.to_datetime(data_df['Date'])
# data_df['Date']=data_df['Date'].map(dt.datetime.toordinal)