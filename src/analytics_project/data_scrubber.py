from __future__ import annotations

from pathlib import Path
from typing import Optional, Iterable, Dict

import pandas as pd


class DataScrubber:
    """
    Reusable helper for standard data cleaning steps using pandas.

    Example:
        scrubber = (
            DataScrubber.from_csv("data/raw/customers_data.csv")
            .standardize_column_names()
            .strip_whitespace()
            .drop_empty_rows()
            .drop_duplicates()
        )
        clean_df = scrubber.get_df()
    """

    def __init__(self, df: pd.DataFrame) -> None:
        # Work on a copy so we don't mutate the caller's DataFrame
        self.df = df.copy()

    # ---------- Constructors ----------

    @classmethod
    def from_csv(cls, path: str | Path, **read_kwargs) -> "DataScrubber":
        """Create a DataScrubber from a CSV file."""
        path = Path(path)
        df = pd.read_csv(path, **read_kwargs)
        return cls(df)

    # ---------- Core cleaning methods ----------

    def standardize_column_names(self) -> "DataScrubber":
        """
        Standardize column names by:
        - converting to string
        - stripping whitespace
        - converting to lowercase
        - replacing spaces with underscores
        """
        self.df.columns = [str(col).strip().lower().replace(" ", "_") for col in self.df.columns]
        return self

    def strip_whitespace(self, columns: Optional[Iterable[str]] = None) -> "DataScrubber":
        """
        Strip leading and trailing whitespace from string/object columns.

        If `columns` is None, apply to all object/string columns.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=["object", "string"]).columns

        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype("string").str.strip()

        return self

    def drop_duplicates(self, subset: Optional[Iterable[str]] = None) -> "DataScrubber":
        """Drop duplicate rows, optionally based on a subset of columns."""
        self.df = self.df.drop_duplicates(subset=subset)
        return self

    def drop_empty_rows(self) -> "DataScrubber":
        """Drop rows where all values are NaN."""
        self.df = self.df.dropna(how="all")
        return self

    def drop_empty_columns(self) -> "DataScrubber":
        """Drop columns where all values are NaN."""
        self.df = self.df.dropna(axis=1, how="all")
        return self

    def drop_na_rows(self, subset: Optional[Iterable[str]] = None) -> "DataScrubber":
        """
        Drop rows that contain NaN values.

        If `subset` is provided, only consider those columns.
        """
        self.df = self.df.dropna(subset=subset)
        return self

    def fill_na(self, fill_values: Dict[str, object]) -> "DataScrubber":
        """
        Fill NaN values using a mapping of {column_name: value}.
        """
        self.df = self.df.fillna(value=fill_values)
        return self

    def cast_column_types(self, type_map: Dict[str, str]) -> "DataScrubber":
        """
        Cast columns to the specified dtypes, e.g.:

            {"customer_id": "int64", "total_spend": "float64"}

        Columns that are missing are ignored.
        """
        for col, dtype in type_map.items():
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(dtype, errors="ignore")
        return self

    # ---------- Output helpers ----------

    def get_df(self) -> pd.DataFrame:
        """Return a copy of the cleaned DataFrame."""
        return self.df.copy()

    def to_csv(self, path: str | Path, index: bool = False, **to_csv_kwargs) -> None:
        """Save the cleaned DataFrame to CSV."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(path, index=index, **to_csv_kwargs)
