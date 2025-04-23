# src/data_ingestion.py

import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def get_sp500_tickers():
    """
    Scrape the live list of S&P 500 tickers from Wikipedia
    by grabbing the table whose id="constituents".
    """
    url  = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    resp = requests.get(url)
    resp.raise_for_status()

    soup  = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', id='constituents')
    if table is None:
        raise RuntimeError("Could not find the S&P 500 constituents table on Wikipedia")

    tickers = []
    # Skip header row; start from second <tr>
    for row in table.find('tbody').find_all('tr')[1:]:
        cols = row.find_all('td')
        if not cols:
            continue
        sym = cols[0].get_text(strip=True).replace('.', '-')
        tickers.append(sym)
    return tickers

def fetch_option_data(ticker):
    tk      = yf.Ticker(ticker)
    spot    = tk.history(period='1d')['Close'].iloc[-1]
    records = []
    for exp in tk.options:
        chain = tk.option_chain(exp)
        for df, typ in [(chain.calls, 1), (chain.puts, 0)]:
            df2 = df.assign(
                ticker=ticker,
                option_type=typ,
                expiration=pd.to_datetime(exp),
                timestamp=pd.Timestamp.today(),
                underlying_price=spot
            )
            records.append(df2)
    return pd.concat(records, ignore_index=True)

def main():
    OUTPUT_DIR  = os.getenv('DATA_DIR', os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'raw')))
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    tickers_env = os.getenv('FRONTEND_TICKERS')
    if tickers_env:
        tickers = [t.strip() for t in tickers_env.split(',')]
    else:
        tickers = get_sp500_tickers()

    for t in tickers:
        try:
            df    = fetch_option_data(t)
            fname = os.path.join(OUTPUT_DIR, f"{t}_{datetime.today():%Y%m%d}.csv")
            df.to_csv(fname, index=False)
            print(f"Saved {fname}")
        except Exception as e:
            print(f"Failed to fetch {t}: {e}")

if __name__ == '__main__':
    main()
