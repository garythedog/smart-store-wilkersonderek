"""
data_prep.py
-------------
Reusable utilities for reading raw CSV files into pandas DataFrames.
This is the first step of our BI pipeline.

Run from the project root:
    uv run python -m analytics_project.data_prep
"""

from pathlib import Path
import logging
import pandas as pd

# Try to use shared logger if available; fallback to basic logging
try:
    from .utils_logger import get_logger

    logger = get_logger(__name__)
except Exception:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.warning("utils_logger not found; using basic logger.")

# ---------- Project Paths ----------
PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


def read_csv_to_df(path: Path | str, **kwargs) -> pd.DataFrame:
    """Read a CSV file into a pandas DataFrame with logging."""
    p = Path(path)
    if not p.exists():
        logger.error("File not found: %s", p)
        raise FileNotFoundError(p)

    kwargs.setdefault("encoding", "utf-8")
    kwargs.setdefault("low_memory", False)

    logger.info("Reading CSV: %s", p)
    df = pd.read_csv(p, **kwargs)
    logger.info("Loaded %s -> rows=%s, cols=%s", p.name, df.shape[0], df.shape[1])
    return df


def main() -> None:
    """Smoke test: Read every CSV in data/raw and print their shapes."""
    logger.info("Starting data prep smoke test")

    if not RAW_DIR.exists():
        logger.error("RAW_DIR does not exist: %s", RAW_DIR)
        return

    csv_files = sorted(RAW_DIR.glob("*.csv"))
    if not csv_files:
        logger.warning("No CSV files found in %s", RAW_DIR)
        return

    for csv_file in csv_files:
        logger.info("Processing: %s", csv_file.name)
        df = read_csv_to_df(csv_file)
        print(f"\n=== {csv_file.name} ===")
        print(f"Shape: {df.shape}")
        print(df.head(3))
        logger.info("✅ %s loaded: %s rows × %s cols", csv_file.name, *df.shape)

    logger.info("Smoke test complete.")


if __name__ == "__main__":
    main()
