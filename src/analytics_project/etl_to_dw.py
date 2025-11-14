"""
ETL to Data Warehouse (P4)
Creates a star schema in SQLite and loads data from data/processed CSVs.

Fact table:    fact_sales
Dimensions:    dim_customer, dim_product
Source files:  data/processed/customers_data_clean.csv
               data/processed/products_data_clean.csv
               data/processed/sales_data_clean.csv
"""

import pathlib
import sqlite3
import sys

import pandas as pd

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

# Project root (two levels up from this file: src/analytics_project/etl_to_dw.py)
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
DW_DIR = DATA_DIR / "dw"
DW_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DW_DIR / "smart_sales.db"  # matches Dr. Case's examples


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------


def create_schema(conn: sqlite3.Connection) -> None:
    """Create star schema tables and indexes if they do not exist."""
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dim_customer (
            CustomerID INTEGER PRIMARY KEY,
            Name TEXT,
            Region TEXT,
            JoinDate TEXT,
            LoyaltyPoints_Num INTEGER,
            PreferredContactMethod_Cat TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dim_product (
            ProductID INTEGER PRIMARY KEY,
            ProductName TEXT,
            Category TEXT,
            UnitPrice REAL,
            CurrentDiscount_Pct REAL,
            Supplier_Cat TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS fact_sales (
            TransactionID INTEGER PRIMARY KEY,
            SaleDate TEXT,
            CustomerID INTEGER,
            ProductID INTEGER,
            StoreID INTEGER,
            CampaignID INTEGER,
            SaleAmount REAL,
            BonusPoints_Num INTEGER,
            PaymentType_Cat TEXT,
            FOREIGN KEY (CustomerID) REFERENCES dim_customer (CustomerID),
            FOREIGN KEY (ProductID) REFERENCES dim_product (ProductID)
        )
        """
    )

    # Helpful indexes for queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_sales_customer ON fact_sales (CustomerID)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales (ProductID)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_sales_store ON fact_sales (StoreID)")

    conn.commit()


def delete_existing_records(conn: sqlite3.Connection) -> None:
    """Clear existing data so the DW can be fully reloaded."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fact_sales")
    cursor.execute("DELETE FROM dim_customer")
    cursor.execute("DELETE FROM dim_product")
    conn.commit()


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------


def load_customers(conn: sqlite3.Connection) -> None:
    """Load customer dimension from processed CSV."""
    path = PROCESSED_DIR / "customers_data_clean.csv"
    df = pd.read_csv(path)

    # Normalize column names from CSV (all lowercase)
    df.columns = df.columns.str.strip().str.lower()

    # Map CSV column names -> DW column names
    rename_map = {
        "customerid": "CustomerID",
        "name": "Name",
        "region": "Region",
        "joindate": "JoinDate",
        "loyaltypoints_num": "LoyaltyPoints_Num",
        "preferredcontactmethod_cat": "PreferredContactMethod_Cat",
    }
    df = df.rename(columns=rename_map)

    # Keep only the DW columns in the correct order
    cols = list(rename_map.values())
    df = df[cols]

    # Remove duplicate customers (keep first occurrence)
    df = df.drop_duplicates(subset=["CustomerID"])

    # Convert date to ISO format YYYY-MM-DD
    df["JoinDate"] = pd.to_datetime(df["JoinDate"]).dt.strftime("%Y-%m-%d")

    df.to_sql("dim_customer", conn, if_exists="append", index=False)


def load_products(conn: sqlite3.Connection) -> None:
    """Load product dimension from processed CSV."""
    path = PROCESSED_DIR / "products_data_clean.csv"
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    rename_map = {
        "productid": "ProductID",
        "productname": "ProductName",
        "category": "Category",
        "unitprice": "UnitPrice",
        "currentdiscount_pct": "CurrentDiscount_Pct",
        "supplier_cat": "Supplier_Cat",
    }
    df = df.rename(columns=rename_map)

    cols = list(rename_map.values())
    df = df[cols]

    # Remove duplicate products (keep first occurrence)
    df = df.drop_duplicates(subset=["ProductID"])

    df.to_sql("dim_product", conn, if_exists="append", index=False)


def load_sales(conn: sqlite3.Connection) -> None:
    """Load fact table from processed sales CSV."""
    path = PROCESSED_DIR / "sales_data_clean.csv"
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    rename_map = {
        "transactionid": "TransactionID",
        "saledate": "SaleDate",
        "customerid": "CustomerID",
        "productid": "ProductID",
        "storeid": "StoreID",
        "campaignid": "CampaignID",
        "saleamount": "SaleAmount",
        "bonuspoints_num": "BonusPoints_Num",
        "paymenttype_cat": "PaymentType_Cat",
    }
    df = df.rename(columns=rename_map)

    cols = list(rename_map.values())
    df = df[cols]

    # Remove duplicate transactions (keep first occurrence)
    df = df.drop_duplicates(subset=["TransactionID"])

    # Convert dates to datetime, coerce invalid ones to NaT
    df["SaleDate"] = pd.to_datetime(
        df["SaleDate"],
        errors="coerce",
        # infer_datetime_format=True  # optional; you can remove this if you like
    )

    # Drop rows where SaleDate could not be parsed
    df = df.dropna(subset=["SaleDate"])

    # Format to ISO string YYYY-MM-DD for the DW
    df["SaleDate"] = df["SaleDate"].dt.strftime("%Y-%m-%d")

    df.to_sql("fact_sales", conn, if_exists="append", index=False)


# ---------------------------------------------------------------------------
# Main ETL orchestration
# ---------------------------------------------------------------------------


def load_data_to_dw() -> None:
    """Main function to create schema and load data into the DW."""
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Using database at: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)

    try:
        create_schema(conn)
        delete_existing_records(conn)

        load_customers(conn)
        load_products(conn)
        load_sales(conn)

        conn.commit()
        print("Data warehouse load completed successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    # Optional: add project root to sys.path (helps if you later import local modules)
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.append(str(PROJECT_ROOT))

    load_data_to_dw()
