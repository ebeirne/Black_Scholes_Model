import os
import glob
import pandas as pd
import numpy as np

# Directories (override with env vars if you like)
HERE          = os.path.dirname(__file__)
RAW_DIR       = os.getenv('DATA_DIR', os.path.abspath(os.path.join(HERE, '..', 'data', 'raw')))
PROCESSED_DIR = os.getenv('PROCESSED_DIR', os.path.abspath(os.path.join(HERE, '..', 'data', 'processed')))

def load_raw(path):
    return pd.read_csv(path, parse_dates=['expiration', 'timestamp'])

def add_features(df):
    df = df.dropna(subset=['bid', 'ask'])
    df['mid_price'] = (df.bid + df.ask) / 2
    df['T']         = (df.expiration - df.timestamp).dt.days.clip(lower=1) / 365
    df['moneyness'] = df['underlying_price'] / df['strike']
    # 30-day historical vol
    df['log_ret']   = np.log(df['underlying_price']).diff()
    df['hist_vol']  = df['log_ret'].rolling(30).std() * np.sqrt(252)
    df['r']         = 0.015  # or pull from a Treasury API
    # drop any rows missing the new features
    return df.dropna(subset=['mid_price', 'T', 'moneyness', 'hist_vol'])

def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    csv_files = glob.glob(os.path.join(RAW_DIR, '*.csv'))

    for raw_fp in csv_files:
        df_feat = add_features(load_raw(raw_fp))
        out_fp  = os.path.join(
            PROCESSED_DIR,
            os.path.basename(raw_fp).replace('.csv', '.parquet')
        )
        df_feat.to_parquet(out_fp, index=False)
        print(f"Processed {raw_fp} → {out_fp}")

if __name__ == '__main__':
    main()
