import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from datetime import date

def download_stock_data(stock_symbol):
    start_date = date.today()
    end_date = start_date + timedelta(days=1)
    stock_df = yf.download(stock_symbol, start=start_date, end=end_date, interval='1m')
    path = stock_symbol+"_"+"data.csv"
    stock_df.to_csv(path, header = False)