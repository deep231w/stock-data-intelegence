import yfinance as yf
import pandas as pd
from datetime import datetime , timedelta

# TICKERS ={
#     "tcs":"TCS",
#     "hdfc":"HDFC",
#     "mahindra":"M&M",
#     "google":"GOOGL"
# }

TICKERS =[
    "TCS.NS",
    "HDFCBANK.NS",
    "M&M.NS",
    "GOOGL"
]

end_date=datetime.today()

def fetch_stock_data(ticker):
    print(f"Fetching {ticker}...")

    df = yf.download(ticker ,period="2y")
    print("df-", df)
    print("-" * 40)


def main():
    for ticker in TICKERS:
        fetch_stock_data(ticker)

if __name__ =="__main__":
    main()