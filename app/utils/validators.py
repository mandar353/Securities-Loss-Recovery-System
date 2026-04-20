import pandas as pd

def validate_excel_columns(df, required_columns):
    # Case-insensitive column matching
    df_columns_lower = [col.lower().strip() for col in df.columns]
    missing = []
    
    for req_col in required_columns:
        if req_col.lower() not in df_columns_lower:
            missing.append(req_col)
    
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Found columns: {list(df.columns)}")
    return True

def validate_numeric_columns(df, numeric_columns):
    """Convert numeric columns to float, skip if not present"""
    for col in df.columns:
        col_lower = col.lower().strip()
        if col_lower in [c.lower() for c in numeric_columns]:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except Exception as e:
                print(f"Warning: Could not convert {col} to numeric: {e}")
    return True