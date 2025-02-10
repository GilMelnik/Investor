import os
import shutil
from time import sleep
from datetime import datetime

import yfinance as yf
import pandas as pd


def get_symbols():
    # Get the list of S&P 500 tickers
    wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500_tickers = pd.read_html(wiki_url)[0]["Symbol"].tolist()
    sp500_tickers = [sym.replace('.', '-') for sym in sp500_tickers]
    return sp500_tickers


# Define function to fetch financial data
def get_financial_data(symbol, metrics):
    stock = yf.Ticker(symbol)
    info = stock.info
    stock_data = {"symbol": symbol}
    stock_data.update({metric: info.get(metric, None) for metric in metrics})
    return stock_data


def get_last_updated_time(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if len(files) == 0:
        return None, None
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(folder_path, f)))
    latest_file_path = os.path.join(folder_path, latest_file)
    last_updated_time = datetime.fromtimestamp(os.path.getctime(latest_file_path))
    return latest_file, last_updated_time


def delete_previous(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)  # Delete file or symbolic link
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Delete subdirectory


def save_csv(df, outputs_path):
    delete_previous(outputs_path)
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file_path = f"{outputs_path}/{now}.csv"
    df.to_csv(file_path, index=False)
    return file_path


def get_data():
    # Fetch data for all S&P 500 companies
    sp500_tickers = get_symbols()[:20]
    metrics = [
        'enterpriseValue',
        'marketCap',
        'beta',
        'debtToEquity',
        'returnOnEquity',
        "trailingPE",
        "enterpriseToEbitda",
        "totalRevenue",
        "revenueGrowth",
        "debtToEquity",
        "operatingCashflow",
        # "interestIncome",
        # "interestExpense",
        # "netInterestIncome"
    ]
    data = dict()
    for symbol in sp500_tickers:
        data[symbol] = get_financial_data(symbol, metrics)
        sleep(3)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame.from_dict(data, orient="index")
    return df


if __name__ == "__main__":
    data = get_data()
    save_csv(data, "/home/melniknoob/Investor/static/reports/")
    print('done')
