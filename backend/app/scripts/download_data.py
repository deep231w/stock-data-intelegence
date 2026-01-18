import yfinance as yf
import pandas as pd
from datetime import datetime , timedelta

TICKERS ={
    "tcs":"TCS.NS",
    "hdfc":"HDFCBANK.NS",
    "mahindra":"M&M.NS",
    "google":"GOOGL"
}

# TICKERS =[
#     "TCS.NS",
#     "HDFCBANK.NS",
#     "M&M.NS",
#     "GOOGL"
# ]

end_date=datetime.today()

def fetch_stock_data(name ,ticker):
    print("ticker inside fetch stock data-", name)
    print(f"Fetching {ticker}...")

    df = yf.download(ticker ,period="2y")
    df=df.reset_index()
    df["symbol"]=name

    df.columns= [c[0].lower() if isinstance(c,tuple) else c.lower()
                 for c in df.columns]
    df["daily_return"]=(df["close"]-df["open"])/df["open"]
    df["ma_7"]=df["close"].rolling(7).mean()
    df["week52_high"] = df["high"].rolling(252).max()
    df["week52_low"] = df["high"].rolling(252).min()

    print("df-", df)
    print("-" * 40)
    return df


def main():
    for name, ticker in TICKERS.items():
        # print(f"ticker is-",name, ticker)
        fetch_stock_data(name ,ticker)

if __name__ =="__main__":
    main()