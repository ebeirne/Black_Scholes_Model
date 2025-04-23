import pandas as pd

def load_csv(file_path):
    """Load a CSV file into a DataFrame"""
    return pd.read_csv(file_path)