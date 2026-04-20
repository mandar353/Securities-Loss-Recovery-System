import pandas as pd
from pathlib import Path
from app.services.twitter_logic import calculate_twitter_loss
from app.services.kraft_logic import calculate_kraft_loss
import os
import io

ROW_BASED_REQUIRED_COLUMNS = (
    {"purchase_price", "sale_price"},
    {"purchases", "sales"},
)

NUMERIC_COLUMNS = {
    "purchases",
    "sales",
    "holdings",
    "price per share",
    "purchase_price",
    "sale_price",
    "quantity",
    "price_per_share",
}


def _has_required_columns(columns):
    normalized = set(columns)
    return any(required.issubset(normalized) for required in ROW_BASED_REQUIRED_COLUMNS)


def _coerce_numeric_columns(df):
    for column in df.columns:
        if column in NUMERIC_COLUMNS:
            df[column] = pd.to_numeric(df[column], errors="coerce")


async def process_file(file, output_dir="data/output"):
    content = await file.read()
    df = pd.read_excel(io.BytesIO(content))

    df.columns = [col.lower().strip() for col in df.columns]
    _coerce_numeric_columns(df)

    group_cols = []
    if "fund name" in df.columns:
        group_cols.append("fund name")
    if "entity" in df.columns:
        group_cols.append("entity")

    # -------------------------------
    # CASE 1: GROUP BASED DATA
    # -------------------------------
    if group_cols and {"purchases", "sales", "holdings"}.issubset(df.columns):

        agg_df = (
            df.groupby(group_cols)
            .agg({"purchases": "sum", "sales": "sum", "holdings": "sum"})
            .reset_index()
        )

        agg_df["recognized_loss"] = agg_df.apply(
            lambda row: max(0.0, float(row["purchases"] or 0) - float(row["sales"] or 0)),
            axis=1,
        )

        # 🔥 ADD MISSING COLUMNS (IMPORTANT FIX)
        agg_df["total_investment"] = agg_df["purchases"]
        agg_df["total_sale"] = agg_df["sales"]
        agg_df["eligible"] = True

        df = df.merge(
            agg_df[group_cols + ["recognized_loss", "total_investment", "total_sale", "eligible"]],
            on=group_cols,
            how="left"
        )

    # -------------------------------
    # CASE 2: ROW BASED DATA
    # -------------------------------
    elif _has_required_columns(df.columns):

        calculator = calculate_twitter_loss if "twitter" in file.filename.lower() else calculate_kraft_loss

        result_df = df.apply(calculator, axis=1)

        df = pd.concat([df, result_df], axis=1)

    else:
        raise ValueError(
            "Unsupported Excel format. Expected columns like purchase_price/sale_price "
            "or purchases/sales."
        )

    # -------------------------------
    # COLUMN STANDARDIZATION
    # -------------------------------
    column_mapping = {
        "purchases": "purchase_price",
        "sales": "sale_price",
        "holdings": "quantity",
        "price per share": "price_per_share",
    }

    df = df.rename(columns=column_mapping)

    # -------------------------------
    # SAFE SUMMARY (NO ERROR GUARANTEE)
    # -------------------------------
    summary = {
        "total_loss": float(df.get("recognized_loss", pd.Series([0]*len(df))).sum()),
        "total_investment": float(df.get("total_investment", pd.Series([0]*len(df))).sum()),
        "total_sale": float(df.get("total_sale", pd.Series([0]*len(df))).sum()),
        "eligible_records": int(df.get("eligible", pd.Series([0]*len(df))).sum())
    }

    # -------------------------------
    # SAVE OUTPUT
    # -------------------------------
    output_filename = f"processed_{file.filename}"
    output_path = Path(output_dir) / output_filename

    os.makedirs(output_path.parent, exist_ok=True)
    df.to_excel(output_path, index=False)

    return {
        "message": "Processed successfully",
        "summary": summary,
        "output_filename": output_filename,
        "download_url": f"/download/{output_filename}",
    }