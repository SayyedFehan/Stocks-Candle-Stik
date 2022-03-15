from datetime import date, timedelta
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpdates

def stock_info(t, sym, api):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_"+t+"&symbol="+sym+".BSE&outputsize=full&apikey="+api
    response = requests.get(url)
    return response.json()

def number_of_days(n):
    days = 0
    for i in range(n):
        days += 365
    return days


if __name__ == "__main__":
    f = open("creds.json")
    d = json.load(f)
    api = d["api_key"]
    my_d = {}
    ty = input("Enter type of data you want to extract. For example daily, weekly or monthly:- ").upper()
    stock = input("Enter the stock symbol you want to get the information of:- ").upper()
    years = input("Enter number of year you want the data for:- ")
    data = stock_info(ty, stock, api)
    number = number_of_days(int(years))
    d = date.today()
    for i in data["Time Series (Daily)"]:
        my_d[i] = data["Time Series (Daily)"][i]
        if i == str(d - timedelta(number + 1)) or i == str(d - timedelta(number + 2)) or i == str(d - timedelta(number + 3)) or i == str(d - timedelta(number + 4)) or i == str(d - timedelta(number + 5)) or i == str(d - timedelta(number + 6)) or i == str(d - timedelta(number + 7)):
            break
    raw_df = pd.DataFrame.from_dict(my_d)
    df = raw_df.transpose()
    df['index'] = df.index
    df.reset_index(level=0, inplace=True)
    df = df.rename(columns = {'index':'Date'})
    df.drop(['level_0'], axis=1, inplace=True)
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]
    for i in cols:
        if i != "Date":
            df[i] = df[i].astype(float)
    df = df[['Date', '1. open', '2. high',
         '3. low', '4. close']]
    df['Date'] = pd.to_datetime(df['Date'])

    df['Date'] = df['Date'].map(mpdates.date2num)
    
    fig, ax = plt.subplots()
    
    candlestick_ohlc(ax, df.values, width = 0.6,
                    colorup = 'green', colordown = 'red',
                    alpha = 0.8)
    ax.grid(True)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    
    plt.title(stock + " " + years +" year's stocks data.")
    
    date_format = mpdates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    
    fig.tight_layout()

    plt.show()
