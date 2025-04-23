## How the ML-Driven Black-Scholes Pricer Works

This project builds a machine-learning approximation to the classical Black–Scholes option-pricing model, trained on real market data from the S & P 500. Instead of relying on a fixed volatility input, the model learns the true—and often imperfect—pricing surface observed in the market.

### 1. Data Ingestion  
- **Universe**: All tickers in the S & P 500 (or a user-specified subset via `FRONTEND_TICKERS`).  
- **Raw Data**: Fetches live option chains (calls and puts) and underlying closing prices using `yfinance`.  
- **Storage**: Saves each day’s raw option data as CSV in `data/raw/`.

### 2. Feature Engineering  
For each option quote, the pipeline computes:  
1. **Time to Maturity** \(T\): days until expiration, in years.  
2. **Moneyness** \(\frac{S}{K}\): ratio of spot price \(S\) to strike \(K\).  
3. **Historical Volatility**: 30-day rolling standard deviation of log returns (annualized).  
4. **Risk-Free Rate** \(r\): assumed constant (e.g. 1.5% annual).  
5. **Mid-Price**: target variable, \(\tfrac{\text{bid} + \text{ask}}{2}\).  
These engineered features are saved as Parquet files in `data/processed/`.

### 3. Model Training  
- **Algorithm**: `RandomForestRegressor` (chosen for its flexibility capturing nonlinear surfaces).  
- **Inputs**: \([S, K, T, r, \text{option_type}, \mathrm{moneyness}, \mathrm{hist\_vol}]\).  
- **Target**: observed option mid-price.  
- **Evaluation**: train/test split (time-based), optimized via grid search on MAE, and finally serialized to `models/rf_model.pkl`.

### 4. Real-Time Prediction API  
A **FastAPI** server exposes a `/predict` endpoint:  
1. Accepts a JSON payload with `symbol`, `strike`, `expiration`, and `option_type`.  
2. Pulls the latest spot price and 30-day historical volatility via `yfinance`.  
3. Constructs the same feature vector used during training.  
4. Returns the ML model’s predicted option price.  

### 5. Frontend Interface  
A modern React + Vite UI lets users:  
- Enter option parameters via a clean form.  
- Toggle between light and dark themes.  
- Receive instant quotes powered by your ML model.  

---

By learning directly from market quotes, this model adapts to real-world deviations from the idealized Black–Scholes assumptions—capturing skew, term structure, and micro-pricing effects that a static implied volatility cannot. It provides an end-to-end pipeline from live data ingestion through feature engineering, model training, and web-based inference.  
