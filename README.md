# Smart Store Analytics – Derek Wilkerson

**Smart Store Analytics** is a professional Python project created for the *Business Intelligence and Analytics* course at Northwest Missouri State University.
It demonstrates how to organize, document, and run analytics code using modern tools such as **uv**, **VS Code**, and **MkDocs**.

---

## 🧭 What This Project Does
- Provides a clean Python project layout under `src/analytics_project/`
- Includes demo modules for basics, stats, languages, and visualization
- Demonstrates how to manage dependencies and environments with `uv`
- Builds project documentation automatically with MkDocs and GitHub Pages

---

## ⚙️ How to Set Up

### Clone the repo
```powershell
git clone https://github.com/garythedog/smart-store-wilkersonderek.git
cd smart-store-wilkersonderek
---

## 🚀 Project Workflow – P2 (BI Python)

This section records the key commands and workflow used to complete Tasks 3 – 5.

### 🧰 Environment Setup (Windows 11 + PowerShell)
```powershell
# Activate local virtual environment
& .\.venv\Scripts\Activate.ps1

# Verify versions
python --version
uv --version
# Run the data preparation module
uv run python -m src.analytics_project.data_prep
# P3: Prepare Data for ETL

## Objective

This stage focuses on **cleaning and preparing data for Extract, Transform, and Load (ETL)** processes.
The goal is to ensure all datasets are consistent, accurate, and ready for analysis in a business-intelligence environment.

---

## Processing Steps

All reusable data-cleaning logic is implemented in
[`src/analytics_project/data_scrubber.py`](https://github.com/wilkersonderek/smart-store-wilkersonderek/blob/main/src/analytics_project/data_scrubber.py)
and orchestrated by
[`src/analytics_project/data_prep.py`](https://github.com/wilkersonderek/smart-store-wilkersonderek/blob/main/src/analytics_project/data_prep.py).

The process reads raw CSV files from `data/raw/`, cleans them using the `DataScrubber` class, and writes standardized versions to `data/processed/`.

### Summary of Cleaning Actions

- Standardized column names (lowercase, underscores instead of spaces).
- Trimmed whitespace from all string fields.
- Removed empty rows and columns.
- Removed duplicate records.
- (Optional) Casted numeric columns to consistent data types.
- Verified all files exported successfully to `data/processed/`.

---

### Input and Output Files

| Input File | Clean Output File |
|-------------|-------------------|
| `data/raw/customers_data.csv` | `data/processed/customers_data_clean.csv` |
| `data/raw/products_data.csv`  | `data/processed/products_data_clean.csv` |
| `data/raw/sales_data.csv`     | `data/processed/sales_data_clean.csv` |

---

## Commands Used During Cleaning

```bash
# Activate environment (Windows PowerShell example)
.\.venv\Scripts\Activate.ps1

# Verify versions
python --version
uv --version

# Run the ETL data-preparation process
uv run python -m analytics_project.data_prep
