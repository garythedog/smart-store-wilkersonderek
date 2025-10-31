"""
data_prep.py
-------------
Reusable utilities for reading raw CSV files into pandas DataFrames
as the first step of our BI pipeline.

Run from the project root:
    uv run python -m analytics_project.data_prep

This module:
- Defines project path constants (PROJECT_DIR, DATA_DIR, RAW_DIR, PROCESSED_DIR)
- Exposes read_csv_to_df(path, **kwargs) with logging and basic validation
- Provides a main() that reads one sample CSV from data/raw for a smoke test
"""

from __future__ import annotations

from pathlib import Path
import logging
from typing import Any, Dict

import pandas as pd

# Try to use our shared project logger; fall back to a simple logger if unavailable.
try:
    from .utils_logger import get_logger  # type: ignore

    logger = get_logger(__name__)
except Exception:  # pragma: no cover
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.warning("utils_logger not found; using basicConfig logger.")


# ---------- Project paths ----------
# repo_root/src/analytics_project/data_prep.py  -> repo_root
PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


def read_csv_to_df(path: Path | str, **kwargs: Dict[str, Any]) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame with helpful logging.

    Parameters
    ----------
    path : Path | str
        Path to the CSV file.
    **kwargs :
        Additional keyword args passed directly to pandas.read_csv
        (e.g., parse_dates=['col'], dtype={'col': 'Int64'}, sep=';', encoding='utf-8').

    Returns
    -------
    pd.DataFrame
        The loaded DataFrame.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file is empty or DataFrame has zero rows.
    """
    p = Path(path)
    if not p.exists():
        logger.error("File not found: %s", p)
        raise FileNotFoundError(f"File not found: {p}")

    # Sensible defaults (can be overridden)
    kwargs.setdefault("encoding", "utf-8")
    kwargs.setdefault("low_memory", False)

    try:
        logger.info("Reading CSV: %s", p)
        try:
            size_kb = p.stat().st_size / 1024
            logger.debug("File size: %.1f KB", size_kb)
        except Exception:
            pass

        df = pd.read_csv(p, **kwargs)

        logger.info("Loaded DataFrame: %s -> rows=%s, cols=%s", p.name, df.shape[0], df.shape[1])
        logger.debug("Columns: %s", list(df.columns))
        logger.debug("Dtypes:\n%s", df.dtypes)

        if df.shape[0] == 0:
            raise ValueError(f"CSV loaded but empty: {p}")

        return df

    except Exception as exc:  # re-raise with context
        logger.exception("Failed reading %s with kwargs=%s", p, kwargs)
        raise


def main() -> None:
    """
    Smoke test:
    - Find a CSV in data/raw
    - Read it into a DataFrame
    - Print a quick preview and info
    """
    logger.info("Starting data prep smoke test")

    if not RAW_DIR.exists():
        logger.error("RAW_DIR does not exist: %s", RAW_DIR)
        return

    csvs = sorted(RAW_DIR.glob("*.csv"))
    if not csvs:
        logger.warning("No CSV files found in %s", RAW_DIR)
        return

    sample = csvs[0]
    logger.info("Using sample CSV: %s", sample.name)

    df = read_csv_to_df(sample)

    # Quick on-screen confirmation for humans
    print("\n=== HEAD (5) ===")
    print(df.head(5))

    print("\n=== INFO ===")
    df.info()  # prints to stdout

    logger.info("Smoke test complete")


if __name__ == "__main__":
    main()
