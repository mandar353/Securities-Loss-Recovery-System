import pandas as pd

def read_file(file):
    return pd.read_excel(file)

def save_file(df, path):
    df.to_excel(path, index=False)