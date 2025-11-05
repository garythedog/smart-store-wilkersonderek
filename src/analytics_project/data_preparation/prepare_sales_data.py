"""
Prepare sales data for ETL.

Run from the project root with:
    python -m analytics_project.data_preparation.prepare_sales_data
"""

from pathlib import Path
import pandas as pd

from analytics_project.utils_logger import get_logger

LOGGER = get_logger(__name__)

# ----- PATHS -----
# __file__ is this file: src/analytics_project/data_preparation/prepare_sales_data.py
# parents[0] -> data_preparation
# parents[1] -> analytics_project
# parents[2] -> src
# parents[3] -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SALES_RAW_PATH = DATA_RAW_DIR / "sales_data.csv"
SALES_CLEAN_PATH = DATA_PROCESSED_DIR / "sales_data_clean.csv"


def load_sales(path: Path) -> pd.DataFrame:
    """Load raw sales data."""
    LOGGER.info("Loading sales data from %s", path)
    df = pd.read_csv(path)
    LOGGER.info("Raw sales shape: %s", df.shape)
    return df


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean sales data:
    - remove duplicates
    - drop rows missing key fields (ids / dates)
    - clean QuantitySold if present
    - remove extreme numeric outliers
    """
    original_rows = len(df)

    # 1) Drop exact duplicate rows
    df = df.drop_duplicates()
    LOGGER.info("Dropped %d duplicate sales rows", original_rows - len(df))

    # 2) Drop rows missing key sales fields
    key_like = [
        "saleid",
        "sale_id",
        "salesid",
        "sales_id",
        "customerid",
        "customer_id",
        "productid",
        "product_id",
        "orderid",
        "order_id",
        "date",
        "orderdate",
    ]
    key_cols = [c for c in df.columns if c.lower() in key_like]
    if key_cols:
        before = len(df)
        df = df.dropna(subset=key_cols)
        LOGGER.info(
            "Dropped %d rows with missing key sales fields (%s)",
            before - len(df),
            key_cols,
        )

    # 3) Example: clean your new numeric column QuantitySold
    if "QuantitySold" in df.columns:
        missing_before = df["QuantitySold"].isna().sum()
        df["QuantitySold"] = df["QuantitySold"].fillna(0)
        LOGGER.info(
            "Filled %d missing QuantitySold values with 0",
            missing_before,
        )

        negatives = (df["QuantitySold"] < 0).sum()
        if negatives > 0:
            df.loc[df["QuantitySold"] < 0, "QuantitySold"] = 0
            LOGGER.info(
                "Set %d negative QuantitySold values to 0",
                negatives,
            )

    # 4) Remove extreme outliers in numeric columns (IQR method)
    #    Ignore numeric ID-like columns to avoid dropping valid keys.
    numeric_cols = [c for c in df.select_dtypes(include="number").columns if "id" not in c.lower()]
    if numeric_cols:
        LOGGER.info(
            "Removing outliers from numeric columns: %s",
            list(numeric_cols),
        )
        before = len(df)
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            df = df[(df[col] >= lower) & (df[col] <= upper)]
        LOGGER.info("Removed %d rows as numeric outliers", before - len(df))

    LOGGER.info("Final sales shape after cleaning: %s", df.shape)
    return df


def save_sales(df: pd.DataFrame, path: Path) -> None:
    """Save cleaned sales data to processed folder."""
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    LOGGER.info("Saved cleaned sales data to %s", path)


def main() -> None:
    """Run the sales data preparation steps."""
    LOGGER.info("=== Starting sales data preparation ===")

    df_raw = load_sales(SALES_RAW_PATH)
    df_clean = clean_sales(df_raw)
    save_sales(df_clean, SALES_CLEAN_PATH)

    LOGGER.info("=== Finished sales data preparation ===")


if __name__ == "__main__":
    main()
