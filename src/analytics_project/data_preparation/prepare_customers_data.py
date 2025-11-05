"""
Prepare customers data for ETL.

Run from the project root with:
    python -m analytics_project.data_preparation.prepare_customers_data
"""

from pathlib import Path
import pandas as pd

from analytics_project.utils_logger import get_logger

LOGGER = get_logger(__name__)

# ----- PATHS -----
# __file__ is this file: src/analytics_project/data_preparation/prepare_customers_data.py
# parents[0] -> data_preparation
# parents[1] -> analytics_project
# parents[2] -> src
# parents[3] -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

CUSTOMERS_RAW_PATH = DATA_RAW_DIR / "customers_data.csv"
CUSTOMERS_CLEAN_PATH = DATA_PROCESSED_DIR / "customers_data_clean.csv"


def load_customers(path: Path) -> pd.DataFrame:
    """Load raw customers data."""
    LOGGER.info("Loading customers data from %s", path)
    df = pd.read_csv(path)
    LOGGER.info("Raw customers shape: %s", df.shape)
    return df


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean customers data:
    - remove duplicates
    - handle missing values
    - remove extreme outliers in numeric columns
    - handle issues you introduced in added columns (e.g., TotalSpend)
    """
    original_rows = len(df)

    # 1) Drop exact duplicate rows
    df = df.drop_duplicates()
    LOGGER.info("Dropped %d duplicate rows", original_rows - len(df))

    # 2) Drop rows missing key fields (ID / name)
    key_cols = [
        c for c in df.columns if c.lower() in ["customerid", "customer_id", "name", "customername"]
    ]
    if key_cols:
        before = len(df)
        df = df.dropna(subset=key_cols)
        LOGGER.info(
            "Dropped %d rows with missing key fields (%s)",
            before - len(df),
            key_cols,
        )

    # 3) Example: fix nulls in your new numeric column TotalSpend
    if "TotalSpend" in df.columns:
        missing_before = df["TotalSpend"].isna().sum()
        df["TotalSpend"] = df["TotalSpend"].fillna(0)
        LOGGER.info("Filled %d missing TotalSpend values with 0", missing_before)

    # 4) Remove extreme outliers in numeric columns (IQR method)
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) > 0:
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

    LOGGER.info("Final customers shape after cleaning: %s", df.shape)
    return df


def save_customers(df: pd.DataFrame, path: Path) -> None:
    """Save cleaned customers data to processed folder."""
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    LOGGER.info("Saved cleaned customers data to %s", path)


def main() -> None:
    """Run the customers data preparation steps."""
    LOGGER.info("=== Starting customers data preparation ===")

    df_raw = load_customers(CUSTOMERS_RAW_PATH)
    df_clean = clean_customers(df_raw)
    save_customers(df_clean, CUSTOMERS_CLEAN_PATH)

    LOGGER.info("=== Finished customers data preparation ===")


if __name__ == "__main__":
    main()
