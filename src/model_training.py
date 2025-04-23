import os
import glob
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error

# Directories (override with env vars if needed)
HERE          = os.path.dirname(__file__)
PROC_DIR      = os.getenv('PROCESSED_DIR', os.path.abspath(os.path.join(HERE, '..', 'data', 'processed')))
MODELS_DIR    = os.getenv('MODELS_DIR', os.path.abspath(os.path.join(HERE, '..', 'models')))

FEATURE_COLS  = [
    'underlying_price', 'strike', 'T', 'r',
    'option_type', 'moneyness', 'hist_vol'
]

def load_all_features():
    paths = glob.glob(os.path.join(PROC_DIR, '*.parquet'))
    if not paths:
        raise ValueError(f"No processed files in {PROC_DIR}")
    return pd.concat([pd.read_parquet(p) for p in paths], ignore_index=True)

def main():
    os.makedirs(MODELS_DIR, exist_ok=True)
    data = load_all_features()
    X    = data[FEATURE_COLS]
    y    = data['mid_price']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    param_grid = {'n_estimators': [50,100], 'max_depth': [5,10]}
    rf         = RandomForestRegressor(random_state=42)
    grid       = GridSearchCV(
        rf, param_grid,
        cv=3, scoring='neg_mean_absolute_error', n_jobs=-1
    )
    grid.fit(X_train, y_train)

    best  = grid.best_estimator_
    preds = best.predict(X_test)
    print("Test MAE:", mean_absolute_error(y_test, preds))

    model_fp = os.path.join(MODELS_DIR, 'rf_model.pkl')
    joblib.dump(best, model_fp)
    print(f"Model saved to {model_fp}")

if __name__ == '__main__':
    main()
