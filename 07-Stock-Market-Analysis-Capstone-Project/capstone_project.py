import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, date2num, WeekdayLocator, DayLocator, MONDAY

import datetime

import pandas_datareader
import pandas_datareader.data as web

from pandas_datareader.google.daily import GoogleDailyReader


@property
def url(self):
    return "http://finance.google.com/finance/historical"

GoogleDailyReader.url = url


#READING DATA
start = datetime.datetime(2012,1,1)
end = datetime.datetime(2017,1,1)


tesla = web.DataReader('TSLA', 'google', start, end)
ford = web.DataReader('F', 'google', start, end)
gm = web.DataReader('GM', 'google', start, end)

#create a new column on the dataframe named total traded
tesla['Total Traded'] = tesla['Open']*tesla['Volume']
ford['Total Traded'] = ford['Open']*ford['Volume']
gm['Total Traded'] = gm['Open']*gm['Volume']


print(tesla.head())

# visualize de data

def plot_opening():
    plt.interactive(False)
    tesla['Open'].plot(label='Tesla', figsize=(12,8), title='Opening Prices')
    gm['Open'].plot(label='GM')
    ford['Open'].plot(label='Ford')
    plt.pyplot.legend()
    plt.pyplot.show()


def plot_volume():
    plt.interactive(False)
    tesla['Volume'].plot(label='Tesla', figsize=(12,8), title='Opening Prices')
    gm['Volume'].plot(label='GM')
    ford['Volume'].plot(label='Ford')
    plt.pyplot.legend()
    plt.pyplot.show()

    print(ford['Volume'].argmax()) # maximum volume ford

def plot_total_traded():
    tesla['Total Traded'].plot(label='Tesla', figsize=(16, 8))
    gm['Total Traded'].plot(label='GM')
    ford['Total Traded'].plot(label='Ford')
    plt.pyplot.legend()
    plt.pyplot.show()


#plotting moving averages
def plot_ma50_ma200(ticker):
    ticker['MA50'] = ticker['Open'].rolling(50).mean()
    ticker['MA200'] = ticker['Open'].rolling(200).mean()
    ticker[['Open', 'MA50', 'MA200']].plot(figsize=(16,8))
    plt.pyplot.show()


def plot_scatter_matrix():
    car_comp = pd.concat([tesla['Open'], gm['Open'], ford['Open']], axis=1)
    car_comp.columns = ['Tesla Open', 'GM Open', 'Ford Open']
    scatter_matrix(car_comp, figsize=(10, 10),alpha=0.2, hist_kwds={'bins':50})
    plt.pyplot.show()


def candle_stick_chart():
    ford_reset = ford.loc['2012-01'].reset_index()
    #ford_reset.info()
    ford_reset['date_ax'] = ford_reset['Date'].apply(lambda date: date2num(date))
    list_of_cols = ['date_ax', 'Open', 'High', 'Low', 'Close']
    ford_values = [tuple(vals) for vals in ford_reset[list_of_cols].values]

    mondays = WeekdayLocator(MONDAY) #major ticks on the mondays
    alldays = DayLocator() # minor ticks on the days
    weekFormatter = DateFormatter('%b %d') #e.g., Jan 12
    dayFormatter = DateFormatter('%d') #e.g, 12

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)

    candlestick_ohlc(ax, ford_values, width=0.4, colorup='g', colordown='r')
    plt.show()


def daily_percent_change(): #daily returns
    tesla['returns'] = (tesla['Close'] / tesla['Close'].shift(1)) #one way

    tesla['returns'] = tesla['Close'].pct_change(1) #another way
    ford['returns'] = ford['Close'].pct_change(1)
    gm['returns'] = gm['Close'].pct_change(1)

    # #plots - separate
    # tesla['returns'].hist(bins=100)
    # ford['returns'].hist(bins=100)
    # gm['returns'].hist(bins=100)
    #
    # #plots - combined
    # tesla['returns'].hist(bins=100, label='Tesla', figsize=(10,8), alpha=0.4)
    # ford['returns'].hist(bins=100, label='Ford', figsize=(10,8), alpha=0.4)
    # gm['returns'].hist(bins=100, label='GM', figsize=(10,8), alpha=0.4)
    # plt.legend()
    # #plt.show()

    # #plot kde
    # tesla['returns'].plot(kind='kde', label='Tesla', figsize=(10,8))
    # ford['returns'].plot(kind='kde', label='Ford', figsize=(10,8))
    # gm['returns'].plot(kind='kde', label='GM', figsize=(10,8))
    # plt.legend()
    # plt.show()

    # #box plot comparing returns
    box_df = pd.concat([tesla['returns'], ford['returns'], gm['returns']], axis=1)
    box_df.columns = (['Tesla Ret', 'Ford Ret', 'GM Ret'])
    # box_df.plot(kind='box', figsize=(8,11))
    # plt.show()

    #compare daily returns between stocks  - scatter matrix
    #scatter_matrix(box_df, figsize=(8, 8), alpha=0.2, hist_kwds={'bins': 100})
    #plt.show()

    #scatter plot of relationship of 2 stocks
    box_df.plot(kind='scatter', x='Ford Ret', y='GM Ret', alpha=0.5, figsize=(8,8))
    plt.show()


def comulative_daily_return():
    #Ii(1+rt)*it-1
    tesla['returns'] = tesla['Close'].pct_change(1)  # another way
    ford['returns'] = ford['Close'].pct_change(1)
    gm['returns'] = gm['Close'].pct_change(1)


    tesla['Cumulative Return'] = (1 + tesla['returns']).cumprod()
    ford['Cumulative Return'] = (1 + ford['returns']).cumprod()
    gm['Cumulative Return'] = (1 + gm['returns']).cumprod()

    # plot comulative return agians the time series index
    tesla['Cumulative Return'].plot(label='Tesla', figsize=(16,8))
    ford['Cumulative Return'].plot(label='Ford')
    gm['Cumulative Return'].plot(label='GM')
    plt.legend()
    plt.show()



#plot_volume()
#plot_total_traded()
#plot_ma50_ma200(gm)
#plot_scatter_matrix()
#candle_stick_chart()
#daily_percent_change()
comulative_daily_return()











