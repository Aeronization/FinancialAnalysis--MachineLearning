# We will be getting and displaying stock information on the S&P500 Companies.
# Source will be from Wikipedia.

#Imports
import bs4 as bs
import pickle
import requests
import os
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import time
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use("ggplot")

"""
# This will grab all of the S&P 500 companies names.
def save_spx_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        #ticker = ticker.replace(".", "-").strip()
        tickers.append(ticker)

    with open('spxTickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

save_spx_tickers()
"""

#
#
#

"""
def get_data_from_morningstar(reload_sp500=False):
    if reload_sp500:
        tickers = save_spx_tickers()
    else:
        with open('spxTickers.pickle', 'rb') as f:
            tickers = pickle.load(f)

    if not os.path.exists("stock_dfs"):
        os.makedirs("stock_dfs")

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2017,12,31)

    # Some of the iterations errored out. Not sure what is causing this issue.
    #for ticker in tickers[0:500]:
    for ticker in tickers:
        print(ticker)

        if not os.path.exists("stock_dfs/{}.csv".format(ticker)):
            # Need to skip these tickers as they do not work.
            if ticker in {"ANDV","BKNG","BHF","CBRE","DWDP","DXC","EVRG","JEF","TPR","UAA","WELL"}:
                print(ticker + " Skip")
            else:
                try:
                    df = web.DataReader(ticker,"morningstar",start,end)
                    df.to_csv("stock_dfs/{}.csv".format(ticker))
                except:
                    print("Could not get data for "+ticker)
        else:
            print("Already have {}".format(ticker))

get_data_from_morningstar()
"""

#
#
#

"""
# This will create a new csv file containing all of the S&P500 stock prices at close.
def compile_data():
    with open('spxTickers.pickle', 'rb') as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        if ticker in {"ANDV", "BKNG", "BHF", "CBRE", "DWDP", "DXC", "EVRG", "JEF", "TPR", "UAA", "WELL"}:
            print(ticker + " Skip")
        else:
            df = pd.read_csv("stock_dfs/{}.csv".format(ticker))

            if not df.empty:
                print(ticker, count)
                df.set_index("Date", inplace=True)
                df.rename(columns = {"Close": ticker}, inplace=True)
                df.drop(["Symbol", "Open", "High", "Low", "Volume"], 1, inplace=True)

                if main_df.empty:
                    main_df = df
                else:
                     main_df = main_df.join(df)
            else:
                 print("Data missing from "+ticker)

    print(main_df.head())
    main_df.to_csv("S&P500_joined_close.csv")

compile_data()
"""

"""
# Once we have the S&P500 file we can then start to read some of that data.
def visualize_data():
    df = pd.read_csv("S&P500_joined_close.csv")
    df_corr = df.corr()

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)

    plt.tight_layout()
    plt.show()

visualize_data()
"""