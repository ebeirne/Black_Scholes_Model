import os
import joblib
import numpy as np
import pandas as pd
import yfinance as yf

# locate the trained model regardless of cwd
HERE       = os.path.dirname(__file__)
MODEL_PATH = os.getenv(
    'MODEL_PATH',
    os.path.abspath(os.path.join(HERE, '..', 'models', 'rf_model.pkl'))
)
MODEL = joblib.load(MODEL_PATH)

def make_features(symbol, strike, expiration, option_type):
    tk   = yf.Ticker(symbol)
    # spot price
    S    = tk.history(period='1d')['Close'].iloc[-1]
    # time to maturity
    T    = max((pd.to_datetime(expiration) - pd.Timestamp.today()).days, 1) / 365
    # 30-day hist vol
    hist = tk.history(period='60d')['Close']
    logr = np.log(hist).diff().dropna()
    vol  = logr.std() * np.sqrt(252)

    return np.array([[S, strike, T, 0.015, option_type, S/strike, vol]])

def predict(symbol, strike, expiration, option_type):
    X = make_features(symbol, strike, expiration, option_type)
    return float(MODEL.predict(X))

MODEL_PATH = os.getenv('MODEL_PATH', os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'models', 'rf_model.pkl')
))

if not os.path.isfile(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 1000:
    raise RuntimeError(
        f"Model file missing or too small ({MODEL_PATH}). "
        "Please retrain by running src/model_training.py"
    )

MODEL = joblib.load(MODEL_PATH)
