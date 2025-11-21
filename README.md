# Smart Store Analytics – Derek Wilkerson

Smart Store Analytics is a professional Python project created for the **Business Intelligence and Analytics** course at Northwest Missouri State University.
It demonstrates how to organize, document, and run analytics code using modern tools such as **uv**, **VS Code**, **Git/GitHub**, and **MkDocs**.

---

## 💡 What This Project Does

- Provides a clean Python project layout under `src/analytics_project/`.
- Includes demo modules for basics, statistics, languages, and visualization.
- Shows how to manage dependencies and environments with **uv** and a local virtual environment.
- Implements a small BI pipeline that:
  - Reads raw CSV files into pandas DataFrames.
  - Cleans and prepares data for ETL.
  - Writes cleaned versions to a prepared data folder.
- Builds project documentation automatically with **MkDocs** and GitHub Pages.

---

## 🛠 How to Set Up

### Clone the repo

From a terminal (PowerShell on Windows):

```bash
git clone https://github.com/wilkersonderek/smart-store-wilkersonderek.git
cd smart-store-wilkersonderek
```

### Create and sync the environment (one-time)

```bash
uv python pin 3.12
uv venv
uv sync --extra dev --extra docs --upgrade
uv run pre-commit install
```

### Activate the virtual environment

**Windows (PowerShell):**

```bash
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux / WSL:**

```bash
source .venv/bin/activate
```

### Verify versions

```bash
python --version
uv --version
```

---

# 🚀 P1: Machine & Project Setup

P1 focused on getting the **local machine** and **project structure** ready for BI work.

### Key Setup Tasks

- Installed and configured Python 3.12, Git, VS Code, and uv.
- Created a new GitHub repo and cloned it locally.
- Initialized a virtual environment (`uv venv`) and synced dependencies (`uv sync`).
- Confirmed all demo modules ran correctly.

---

# 📊 P2: BI Python – Reading Raw Data into pandas DataFrames

## Overview

P2 demonstrated how to use Python and pandas to load raw CSV data files into DataFrames as part of a BI workflow.

### Data Folder Structure

```
data/raw/
│
├── customers_data.csv
├── products_data.csv
└── sales_data.csv
```

### Run the Data Preparation Module

```bash
uv run python -m analytics_project.data_prep
```

This command executes the module directly from the project root.
It reads each raw CSV file found in `data/raw/`, loads it into pandas, and logs the file name and shape.

### Results Summary

| File Name            | Rows | Columns |
|----------------------|------|---------|
| customers_data.csv   | 201  | 6       |
| products_data.csv    | 100  | 4       |
| sales_data.csv       | 2001 | 8       |

---

# 🧹 P3: Prepare Data for ETL

## Objective

P3 focused on **cleaning and preparing data for Extract, Transform, and Load (ETL)**.
The goal is to ensure all datasets are consistent, accurate, and ready for business-intelligence analysis.

### Key Objectives

- Employ pandas to perform common cleaning and prep tasks.
- Wrap this functionality into a reusable `DataScrubber` class.
- Verify behavior with unit tests (optional).
- Use the `DataScrubber` class in the data prep script to process all three tables.

---

## Data Cleaning Process

All reusable cleaning logic was implemented in:

- [`src/analytics_project/data_scrubber.py`](https://github.com/wilkersonderek/smart-store-wilkersonderek/blob/main/src/analytics_project/data_scrubber.py)

The orchestration script that uses this class:

- [`src/analytics_project/data_prep.py`](https://github.com/wilkersonderek/smart-store-wilkersonderek/blob/main/src/analytics_project/data_prep.py)

### Cleaning Actions Performed

| Step | Action | Description |
|------|---------|-------------|
| 1 | **Standardized column names** | Lowercase, underscores, trimmed whitespace |
| 2 | **Trimmed whitespace** | Cleaned up string fields |
| 3 | **Dropped empty rows/columns** | Removed fully blank data |
| 4 | **Removed duplicate records** | Ensured unique entries |
| 5 | **Casted column types** | Converted numeric fields as needed |

### Input → Output Summary

| Input File                    | Clean Output File                         |
|-------------------------------|-------------------------------------------|
| `data/raw/customers_data.csv` | `data/processed/customers_data_clean.csv` |
| `data/raw/products_data.csv`  | `data/processed/products_data_clean.csv`  |
| `data/raw/sales_data.csv`     | `data/processed/sales_data_clean.csv`     |

---

## Commands Used During Cleaning

```bash
# Activate environment
.\.venv\Scripts\Activate.ps1

# Run ETL data prep
uv run python -m analytics_project.data_prep
```

This command loads all raw CSV files, cleans them using the `DataScrubber` class, and exports processed versions into `data/processed/`.

---

## Example Terminal Output

```
Running data prep...
customers_data: cleaned and saved to data/processed/customers_data_clean.csv
products_data: cleaned and saved to data/processed/products_data_clean.csv
sales_data: cleaned and saved to data/processed/sales_data_clean.csv
Data prep complete. Clean files are in data/processed
```

---

## Git Commands Used

```bash
git add README.md src\analytics_project\data_scrubber.py src\analytics_project\data_prep.py
git commit -m "Implement reusable DataScrubber and prepare data for ETL"
git push
```

---

## Notes & Lessons Learned

- Reusable cleaning logic simplifies all future BI workflows.
- Pandas is powerful for automated preprocessing of large data files.
- Documenting commands in the README improves reproducibility.
- Data cleaning can take the most time in BI, so automation is essential.

---

## Final Verification

```bash
dir data\processed
```

Expected output:

```
customers_data_clean.csv
products_data_clean.csv
sales_data_clean.csv
```

---

## Quick Links

- [Repository Home](https://github.com/wilkersonderek/smart-store-wilkersonderek)
- [README.md](https://github.com/wilkersonderek/smart-store-wilkersonderek/blob/main/README.md)
- [DataScrubber Class](https://github.com/wilkersonderek/smart-store-wilkersonderek/blob/main/src/analytics_project/data_scrubber.py)
- [Data Prep Script](https://github.com/wilkersonderek/smart-store-wilkersonderek/blob/main/src/analytics_project/data_prep.py)
- [Processed Data Folder](https://github.com/wilkersonderek/smart-store-wilkersonderek/tree/main/data/processed)

---

### ✅ Commit & Push Commands

After saving your README:

```ps
git add README.md
git commit -m "Restore full README.md with P1–P3 workflow and ETL details"
git push

```

🏛️ P4: Data Warehouse Design and ETL to DW
Overview

P4 extends the Smart Store BI pipeline by creating and populating a small data warehouse (DW) in SQLite.
The goal is to move from cleaned CSV files to a dimensional model (star schema) that supports fast, flexible business-intelligence queries.

In this phase, I:

Designed a star schema with one fact table and two dimension tables.

Created the schema in a local SQLite database.

Wrote a Python ETL script to load the warehouse from the processed CSV files.

Verified that all three tables were populated correctly.

Data Warehouse Files

SQLite database: data/dw/smart_sales.db

ETL script: src/analytics_project/etl_to_dw.py

Source (cleaned) data:

data/processed/customers_data_clean.csv

data/processed/products_data_clean.csv

data/processed/sales_data_clean.csv

Star Schema Design

The data warehouse uses a star schema with one central fact table and two dimensions:

dim_customer ← fact_sales → dim_product

Key ideas:

dim_customer contains descriptive attributes about each customer.

dim_product contains descriptive attributes about each product.

fact_sales stores the numeric measures (such as quantity and sales amount) and foreign keys to each dimension.

This structure supports OLAP-style queries such as “total sales by product category,” “sales by customer segment,” and other slice-and-dice analysis.

ETL to the Data Warehouse

The ETL script performs the following steps:

Reads the cleaned CSV files from data/processed.

Creates the SQLite database file (if it does not exist).

Creates the dimension and fact tables for the star schema.

Loads customers into dim_customer, products into dim_product, and sales records into fact_sales.

Logs row counts so I can verify that all rows were loaded correctly.

After running the ETL, I confirmed that:

dim_customer contains the expected number of customer rows.

dim_product contains the expected number of product rows.

fact_sales contains the expected number of sales transactions.

This completed the move from prepared flat files into a true analytical data warehouse.

P5 – Cross-Platform Reporting with Power BI and Spark
Overview

P5 connects the SQLite data warehouse created in P4 to Power BI using an ODBC DSN, performs OLAP-style analysis, and prepares for future cross-platform reporting with tools like Spark.
The goal is to show that the star schema in data/dw/smart_sales.db can support flexible, repeatable analysis outside of SQLite.

Task 1 – Install and Configure Power BI + SQLite ODBC

Steps completed:

Installed Power BI Desktop.

Installed the SQLite ODBC driver.

Created an ODBC DSN named SmartSalesDSN.

Linked the DSN to the SQLite data warehouse file data/dw/smart_sales.db.

This allowed Power BI to treat the SQLite data warehouse as a standard relational data source.

Task 2 – Load Data Warehouse Tables into Power BI

Steps completed:

In Power BI, used Home → Get Data → ODBC and selected SmartSalesDSN.

Loaded the tables dim_customer, dim_product, and fact_sales.

Opened Model view and verified the relationships:

dim_customer.CustomerID → fact_sales.CustomerID

dim_product.ProductID → fact_sales.ProductID

This recreated the star schema visually inside Power BI.

Task 3 – Measures and Visuals for Analysis

To support OLAP-style analysis, I defined DAX measures and used them in visuals.

Examples of measures:

Total Sales Amount – sums the extended sales amount across all rows in fact_sales.

Total Quantity Sold – sums the units sold.

Average Order Value – divides total sales amount by the number of distinct orders or customers (depending on the definition used).

How they were used:

A bar chart showing Total Sales Amount by product category.

A table showing the Top 10 Customers by Total Sales.

Slicers for date, product category, and (if available) customer segment.

These visuals demonstrate that the data warehouse can answer common business questions quickly.

Task 4 – Example Insights

From the Power BI report, I observed that:

A few product categories contribute a large portion of total revenue.

A relatively small set of customers drives a significant share of total sales.

Slicers make it easy to compare different time periods or filter to specific categories or customer groups.

These are classic OLAP-style insights that depend on having a clean star schema and a well-designed BI model.

Future Cross-Platform Use (Spark and Others)

Because the data warehouse is stored in a standard SQLite file and follows a star schema, it can be reused by many tools:

Spark DataFrames by connecting to the database or importing exported tables.

Other BI tools such as Tableau or Excel.

Python or R notebooks for more advanced analytics or machine learning.

The key idea is that P4 built the warehouse, and P5 demonstrates how that warehouse supports tool-agnostic reporting across platforms.

Reflection

This phase helped me connect a real data warehouse to a professional BI tool.

I practiced setting up ODBC connections and validating relationships between fact and dimension tables.

I gained experience defining measures and building visuals that answer real BI questions.

I saw how a well-designed star schema makes it easy to reuse the same data across multiple tools (SQLite, Power BI, and potentially Spark) without rebuilding the pipeline from scratch.

Step 2 – Save, commit, push

After you paste the new section:

Save the file in VS Code.

In the terminal (at the project root), run:

git add README.md

git commit -m "Rewrite P4 and P5 section without markdown code fences"

git push

Then refresh the README on GitHub – everything from P4 down should render as normal headings, paragraphs, and bullet lists, with no giant grey code box.

Why this suddenly became a problem

You asked a fair question: why did everything work fine earlier?

Earlier sections (P1–P3) had balanced fences and we weren’t trying to surgically edit inside them.

The moment we mixed a partial code block (```text) and then nested more fences inside P5, one missing closing fence caused GitHub to treat everything below as “still inside the code block.”

The chat UI always turns ``` into a grey box, which makes “before” and “after” look identical when I’m trying to show fixes.
