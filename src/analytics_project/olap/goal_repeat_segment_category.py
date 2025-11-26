"""
OLAP Goal:
Identify which product categories generate the most repeat-purchase revenue,
and how revenue varies by region.

This script demonstrates:
- SLICING   → filter to repeat customers only (2+ transactions)
- DICING    → breakdown by Category × Region
- DRILLDOWN → pivot table summary
- VISUALIZATION → bar chart, stacked bar chart, pie chart
"""

import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Helper: Get database path
# ---------------------------------------------------------
def get_db_path() -> Path:
    project_root = Path(__file__).resolve().parents[3]
    db_path = project_root / "data" / "dw" / "smart_sales.db"
    return db_path


# ---------------------------------------------------------
# Load data from DW
# ---------------------------------------------------------
def load_data():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)

    fact_sales = pd.read_sql("SELECT * FROM fact_sales;", conn)
    dim_customers = pd.read_sql("SELECT * FROM dim_customer;", conn)
    dim_products = pd.read_sql("SELECT * FROM dim_product;", conn)

    conn.close()
    return fact_sales, dim_customers, dim_products


# ---------------------------------------------------------
# Prepare merged dataset + repeat-customer slice
# ---------------------------------------------------------
def prepare_sales_data(fact_sales, dim_customers, dim_products) -> pd.DataFrame:
    # Ensure date is datetime
    fact_sales["SaleDate"] = pd.to_datetime(fact_sales["SaleDate"])

    # Create YearMonth (even if 1 month)
    fact_sales["YearMonth"] = fact_sales["SaleDate"].dt.to_period("M").astype(str)

    # Merge customer dimension (Region)
    sales_cust = fact_sales.merge(
        dim_customers[["CustomerID", "Region"]],
        on="CustomerID",
        how="left",
    )

    # Merge product dimension (Category)
    sales_full = sales_cust.merge(
        dim_products[["ProductID", "Category"]],
        on="ProductID",
        how="left",
    )

    # Ensure SaleAmount is numeric
    sales_full["SaleAmount"] = pd.to_numeric(sales_full["SaleAmount"], errors="coerce")

    # Identify repeat customers: 2+ transactions
    purchase_counts = sales_full.groupby("CustomerID")["TransactionID"].nunique()
    repeat_customers = purchase_counts[purchase_counts >= 2].index

    # Mark repeat customers
    sales_full["IsRepeatCustomer"] = sales_full["CustomerID"].isin(repeat_customers)

    # Slice: keep only repeat customers
    repeat_sales = sales_full[sales_full["IsRepeatCustomer"]].copy()

    return repeat_sales


# ---------------------------------------------------------
# Summaries (Category, Category×Region, Pivot)
# ---------------------------------------------------------
def summarize_by_category(repeat_sales):
    summary = (
        repeat_sales.groupby("Category")
        .agg(
            TotalRepeatRevenue=("SaleAmount", "sum"),
            RepeatPurchases=("TransactionID", "nunique"),
        )
        .reset_index()
        .sort_values("TotalRepeatRevenue", ascending=False)
    )
    return summary


def summarize_category_region(repeat_sales):
    summary = (
        repeat_sales.groupby(["Category", "Region"])
        .agg(TotalRepeatRevenue=("SaleAmount", "sum"))
        .reset_index()
        .sort_values("TotalRepeatRevenue", ascending=False)
    )
    return summary


def pivot_category_region(repeat_sales):
    pivot = repeat_sales.pivot_table(
        index="Category", columns="Region", values="SaleAmount", aggfunc="sum", fill_value=0
    )
    pivot["Total"] = pivot.sum(axis=1)
    return pivot.sort_values("Total", ascending=False)


# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------
def plot_revenue_by_category(category_summary, output_dir: Path):
    ax = category_summary.plot(
        x="Category", y="TotalRepeatRevenue", kind="bar", legend=False, figsize=(10, 5)
    )
    ax.set_title("Repeat-Purchase Revenue by Product Category")
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Total Repeat Revenue")
    plt.tight_layout()

    path = output_dir / "revenue_by_category.png"
    plt.savefig(path)
    plt.close()
    return path


def plot_category_region_stacked(category_region_summary, output_dir: Path):
    pivot = category_region_summary.pivot(
        index="Category", columns="Region", values="TotalRepeatRevenue"
    ).fillna(0)

    ax = pivot.plot(kind="bar", stacked=True, figsize=(12, 6))
    ax.set_title("Repeat-Purchase Revenue by Category and Region")
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Total Repeat Revenue")
    plt.tight_layout()

    path = output_dir / "revenue_category_region_stacked.png"
    plt.savefig(path)
    plt.close()
    return path


def plot_category_share(category_summary, output_dir: Path):
    plt.figure(figsize=(7, 7))
    plt.pie(
        category_summary["TotalRepeatRevenue"],
        labels=category_summary["Category"],
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title("Category Share of Repeat-Purchase Revenue")
    plt.tight_layout()

    path = output_dir / "revenue_category_share.png"
    plt.savefig(path)
    plt.close()
    return path


# ---------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------
def main():
    print("Loading data...")
    fact_sales, dim_customers, dim_products = load_data()

    print("Preparing sales data (Slicing repeat customers)...")
    repeat_sales = prepare_sales_data(fact_sales, dim_customers, dim_products)

    print("Summarizing revenue by category...")
    category_summary = summarize_by_category(repeat_sales)
    print(category_summary)

    print("\nSummarizing revenue by category and region...")
    category_region_summary = summarize_category_region(repeat_sales)
    print(category_region_summary)

    print("\nCreating pivot table summary...")
    pivot = pivot_category_region(repeat_sales)
    print(pivot)

    # Figure output directory
    project_root = Path(__file__).resolve().parents[3]
    figs_dir = project_root / "figures" / "olap"
    figs_dir.mkdir(parents=True, exist_ok=True)

    print("\nCreating charts...")
    cat_chart = plot_revenue_by_category(category_summary, figs_dir)
    stacked_chart = plot_category_region_stacked(category_region_summary, figs_dir)
    pie_chart = plot_category_share(category_summary, figs_dir)

    print(f"\nSaved chart: {cat_chart}")
    print(f"Saved chart: {stacked_chart}")
    print(f"Saved chart: {pie_chart}")

    print("\nOLAP analysis complete.")


if __name__ == "__main__":
    main()
