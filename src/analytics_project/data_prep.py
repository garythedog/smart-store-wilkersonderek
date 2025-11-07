from pathlib import Path

from analytics_project.data_scrubber import DataScrubber


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def prep_customers() -> None:
    raw_path = RAW_DIR / "customers_data.csv"
    out_path = PROCESSED_DIR / "customers_data_clean.csv"

    scrubber = (
        DataScrubber.from_csv(raw_path)
        .standardize_column_names()
        .strip_whitespace()
        .drop_empty_rows()
        .drop_duplicates()
    )

    scrubber.to_csv(out_path, index=False)


def prep_products() -> None:
    raw_path = RAW_DIR / "products_data.csv"
    out_path = PROCESSED_DIR / "products_data_clean.csv"

    scrubber = (
        DataScrubber.from_csv(raw_path)
        .standardize_column_names()
        .strip_whitespace()
        .drop_empty_rows()
        .drop_duplicates()
    )

    scrubber.to_csv(out_path, index=False)


def prep_sales() -> None:
    raw_path = RAW_DIR / "sales_data.csv"
    out_path = PROCESSED_DIR / "sales_data_clean.csv"

    scrubber = (
        DataScrubber.from_csv(raw_path)
        .standardize_column_names()
        .strip_whitespace()
        .drop_empty_rows()
        .drop_duplicates()
    )

    scrubber.to_csv(out_path, index=False)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    prep_customers()
    prep_products()
    prep_sales()
    print("Data prep complete. Clean files written to:", PROCESSED_DIR)


if __name__ == "__main__":
    main()
