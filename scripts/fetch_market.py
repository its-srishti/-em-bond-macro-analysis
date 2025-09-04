# scripts/fetch_market.py
import yfinance as yf
import pandas as pd
import os

os.makedirs('data/raw', exist_ok=True)

start = "2010-01-01"
end = "2024-12-01"

# tickers (use Yahoo tickers)
tickers = {
    'USD_INDEX': 'DX-Y.NYB',   # sometimes alternate tickers exist; test in your session
    'BRENT': 'BZ=F'
}

for name, ticker in tickers.items():
    print("Downloading", ticker)
    df = yf.download(ticker, start=start, end=end, progress=False)
    if 'Adj Close' in df.columns:
        series = df[['Adj Close']].rename(columns={'Adj Close': name}).reset_index()
    elif 'Close' in df.columns:
        series = df[['Close']].rename(columns={'Close':name}).reset_index()
    else:
        series = df.reset_index()

    series.to_csv(f"data/raw/{name.lower()}_daily.csv", index=False)
    print("Saved data/raw/{}_daily.csv".format(name.lower()))