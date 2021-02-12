import pandas as pd
import requests
import time
from datetime import date
from pathlib import Path

" USD Cur_ID = 145 ondate=2016-7-01"
"https://www.nbrb.by/api/exrates/rates/145?ondate=2016-7-01"

Cur_ID = 145


# load json file with nbrb.by site
def load_prices(val, filename):
    url = 'https://www.nbrb.by/api/exrates/rates/{}?ondate={}'.format(val, filename)
    while True:
        try:
            dat = requests.get(url, timeout=5)
            break
        except:
            time.sleep(3)
    dat = dat.json()
    return dat


# make list calendar
def make_calendar(start_date):
    dates = pd.period_range(start_date, date.today())
    return dates


def make_table(calMas):
    table = pd.DataFrame(columns=['price'])
    for i in calMas:
        a = load_prices(Cur_ID, i)
        if a['Cur_OfficialRate'] > 100:
            table.loc[i] = [a['Cur_OfficialRate'] / 10000]
        else:
            table.loc[i] = [a['Cur_OfficialRate']]
        print(i)
    # table = table.set_index(pd.DatetimeIndex(table['date']))
    # table = table.drop('date', 1)
    return table


file_name = path_csv_BYN = a = Path(__file__).parent.joinpath('byn').joinpath("USDBYN2010_2020.csv")
if Path(file_name).exists():
    table = pd.read_csv(file_name, index_col=0)
    date_start = table.index[-1]
    calendar_mas = make_calendar(date_start)
    print('calendar created')
    table_p = make_table(calendar_mas)
    table_price = pd.concat([table, table_p])
    print(table_price)

else:
    calendar_mas = make_calendar('2010-10-01')
    print('calendar created')
    table_price = make_table(calendar_mas)
    print(table_price)
table_price.to_csv(file_name)
