import pandas as pd
import numpy as np

def handle_missing_values(df, threshold=0.02):
    """
    Clean missing values in a DataFrame based on threshold.
    If missing ratio < threshold → drop rows
    Else → fill values (mean for numeric, mode for categorical)
    
    Args:
        df (pd.DataFrame): input DataFrame
        threshold (float): missing value threshold (e.g., 0.02 = 2%)

    Returns:
        pd.DataFrame: cleaned DataFrame
    """
    total_rows = len(df)
    
    for col in df.columns:
        missing_ratio = df[col].isnull().sum() / total_rows

        if missing_ratio == 0:
            continue

        if missing_ratio < threshold:
            df = df[df[col].notna()]
        else:
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                # Categorical column
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col].fillna(mode_val[0], inplace=True)
                else:
                    df[col].fillna("Unknown", inplace=True)
            else:
                # Numerical column
                df[col].fillna(df[col].mean(), inplace=True)

    return df
