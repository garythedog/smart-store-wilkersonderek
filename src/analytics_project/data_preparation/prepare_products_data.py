"""
Prepare products data for ETL.

Run from the project root with:
    python -m analytics_project.data_preparation.prepare_products_data
"""

from pathlib import Path
import pandas as pd

from analytics_project.utils_logger import get_logger

LOGGER = get_logger(__name__)

# ----- PATHS -----
# __file__ is this file: src/analytics_project/data_preparation/prepare_products_data.py
# parents[0] -> data_preparation
# parents[1] -> analytics_project
# parents[2] -> src
# parents[3] -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PRODUCTS_RAW_PATH = DATA_RAW_DIR / "products_data.csv"
PRODUCTS_CLEAN_PATH = DATA_PROCESSED_DIR / "products_data_clean.csv"


def load_products(path: Path) -> pd.DataFrame:
    """Load raw products data."""
    LOGGER.info("Loading products data from %s", path)
    df = pd.read_csv(path)
    LOGGER.info("Raw products shape: %s", df.shape)
    return df


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean products data:
    - remove duplicates
    - handle missing key values
    - clean StockQuantity (if present)
    - remove extreme outliers in numeric columns
    """
    original_rows = len(df)

    # 1) Drop exact duplicate rows
    df = df.drop_duplicates()
    LOGGER.info("Dropped %d duplicate product rows", original_rows - len(df))

    # 2) Drop rows missing key product fields
    key_cols = [
        c
        for c in df.columns
        if c.lower() in ["productid", "product_id", "sku", "name", "productname"]
    ]
    if key_cols:
        before = len(df)
        df = df.dropna(subset=key_cols)
        LOGGER.info(
            "Dropped %d rows with missing key product fields (%s)",
            before - len(df),
            key_cols,
        )

    # 3) Example: clean your new numeric column StockQuantity
    if "StockQuantity" in df.columns:
        # Fill missing with 0
        missing_before = df["StockQuantity"].isna().sum()
        df["StockQuantity"] = df["StockQuantity"].fillna(0)
        LOGGER.info(
            "Filled %d missing StockQuantity values with 0",
            missing_before,
        )

        # Fix negative values (set any negatives to 0)
        negatives = (df["StockQuantity"] < 0).sum()
        if negatives > 0:
            df.loc[df["StockQuantity"] < 0, "StockQuantity"] = 0
            LOGGER.info(
                "Set %d negative StockQuantity values to 0",
                negatives,
            )

    # 4) Remove extreme outliers in numeric columns (IQR method)
    #    We'll ignore any numeric ID columns so we don't delete valid products.
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

    LOGGER.info("Final products shape after cleaning: %s", df.shape)
    return df


def save_products(df: pd.DataFrame, path: Path) -> None:
    """Save cleaned products data to processed folder."""
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    LOGGER.info("Saved cleaned products data to %s", path)


def main() -> None:
    """Run the products data preparation steps."""
    LOGGER.info("=== Starting products data preparation ===")

    df_raw = load_products(PRODUCTS_RAW_PATH)
    df_clean = clean_products(df_raw)
    save_products(df_clean, PRODUCTS_CLEAN_PATH)

    LOGGER.info("=== Finished products data preparation ===")


if __name__ == "__main__":
    main()
