import yfinance as yf
import pandas as pd


def get_symbols():
    # Get the list of S&P 500 tickers
    wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500_tickers = pd.read_html(wiki_url)[0]["Symbol"].tolist()
    return sp500_tickers


# Define function to fetch financial data
def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    stock_data = {
        "Enterprise Value": info.get('enterpriseValue', None),
        "Market cap": info.get('marketCap', None),
        "Beta": info.get('beta', None),
        "Debt to Equity": info.get('debtToEquity', None),
        "Return on Equity": info.get('returnOnEquity', None),
        "Free Cash Flow": info.get('freeCashFlow', None),
        "Operating Cash Flow": info.get('operatingCashFlow', None),
    }
    return stock_data


def main():
    # Fetch data for all S&P 500 companies
    sp500_tickers = get_symbols()
    data = {ticker: get_financial_data(ticker) for ticker in sp500_tickers}

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame.from_dict(data, orient="index")
    df.to_csv("sp500_financials.csv")


if __name__ == "__main__":
    main()
