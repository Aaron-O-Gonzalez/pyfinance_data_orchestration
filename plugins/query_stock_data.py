import pandas as pd

def query_data(datafile_path):
    stock_df = pd.read_csv(datafile_path)
    print(stock_df.head(20))