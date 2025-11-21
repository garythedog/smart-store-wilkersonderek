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

## 🏛️ P4: Data Warehouse Design and ETL to DW

### Overview

P4 extends the Smart Store BI pipeline by creating and populating a small **data warehouse (DW)** in SQLite.
The goal is to move from cleaned CSV files to a **dimensional model (star schema)** that supports fast, flexible business intelligence queries.

In this phase, I:

- Designed a star schema with one fact table and two dimension tables.
- Created the schema in a local SQLite database.
- Wrote a Python ETL script to load the warehouse from the processed CSV files.
- Verified that all three tables were populated correctly.

---

### Data Warehouse Files

- **SQLite database:** `data/dw/smart_sales.db`
- **ETL script:** `src/analytics_project/etl_to_dw.py`
- **Source (cleaned) data:**
  - `data/processed/customers_data_clean.csv`
  - `data/processed/products_data_clean.csv`
  - `data/processed/sales_data_clean.csv`

---

### Star Schema Design

The data warehouse uses a **star schema**:

```text
dim_customer   ←   fact_sales   →   dim_product

## P5 – Cross-Platform Reporting with Power BI & Spark

### Overview
This project connects the data warehouse created in P4 to Power BI using an ODBC DSN, performs OLAP operations (slice, dice, drilldown), executes SQL queries in Power Query, and creates interactive BI visuals.

### Task 1 – Install & Configure Power BI + SQLite ODBC
**Steps completed:**
- Installed Power BI Desktop.
- Installed the SQLite3 ODBC Driver.
- Created DSN: `SmartSalesDSN`.
- Linked the DSN to the SQLite data warehouse: `data/dw/smart_sales.db`.

### Task 2 – Load Data Warehouse Tables
**Steps completed:**
- Connected via **Home → Get Data → ODBC → SmartSalesDSN**.
- Loaded the following tables into Power BI:
  - `dim_customer`
  - `dim_product`
  - `fact_sales`
- Verified the relationships in **Model View**.

### Task 3 – Query & Aggregate Data Using SQL in Power BI
To generate a list of top-spending customers, I created a custom SQL query directly in Power Query’s Advanced Editor.

**Steps completed:**
1. Opened **Power Query Editor** (Home → Transform data).
2. Created a **Blank Query**.
3. Opened **Advanced Editor**.
4. Inserted a custom SQL query using the DSN (`SmartSalesDSN`).
5. Joined the warehouse tables `fact_sales` and `dim_customer`.
6. Calculated `SUM(SaleAmount)` grouped by customer.
7. Renamed the query to **Top Customers**.
8. Clicked **Close & Apply** to load the results back into Power BI.

**M code used:**

```m
let
    Source = Odbc.Query("dsn=SmartSalesDSN",
        "SELECT c.Name AS customer_name,
                SUM(f.SaleAmount) AS total_spent
         FROM fact_sales f
         JOIN dim_customer c
           ON f.CustomerID = c.CustomerID
         GROUP BY c.Name
         ORDER BY total_spent DESC;")
in
    Source

---

## P5 - Cross-Platform Reporting with Power BI & Spark

### Overview
This project connects the data warehouse created in P4 to Power BI using an ODBC DSN, performs OLAP operations, and prepares for future cross-platform reporting with Spark or other tools. The goal is to show that the star schema in `data/dw/smart_sales.db` can support flexible, repeatable analysis outside of SQLite.

### Task 1 – Install & Configure Power BI + SQLite ODBC

**Steps completed:**

- Installed Power BI Desktop.
- Installed the SQLite3 ODBC Driver.
- Created a DSN named `SmartSalesDSN`.
- Linked the DSN to the SQLite data warehouse file: `data/dw/smart_sales.db`.

### Task 2 – Load Data Warehouse Tables

**Steps completed:**

- Connected to **Home → Get Data → ODBC → SmartSalesDSN**.
- Loaded the following tables into Power BI:
  - `dim_customer`
  - `dim_product`
  - `fact_sales`
- Verified relationships in **Model view**, using:
  - `dim_customer.CustomerID` → `fact_sales.CustomerID`
  - `dim_product.ProductID` → `fact_sales.ProductID`.

### Task 3 – Create & Use Measures for Analysis

To support OLAP-style analysis, I defined DAX measures for sales and quantity.

**Measures created:**

- **Total Sales Amount**
  Calculates the total extended sales amount.

- **Total Quantity Sold**
  Sums the units sold across all transactions.

- **Average Order Value**
  Divides total sales by the number of distinct orders.

**How I used them:**

- Built a bar chart showing **Total Sales Amount by Product Category**.
- Built a table showing **Top 10 Customers by Total Sales**.
- Used slicers for:
  - Date (by year or month)
  - Product category
  - Customer segment (if available).

### Task 4 – Example Insights from the Report

From the Power BI report, I observed:

- Certain product categories contribute a large share of total revenue.
- A small number of customers drive a significant portion of total sales.
- Filters make it easy to answer ad hoc questions, such as:
  - “Which customers bought the most in a specific category?”
  - “How did sales change between two time periods?”

### Future Cross-Platform Use (Spark, etc.)

Because the data warehouse is in a standard SQLite database with a star schema, the same data can be used by:

- Spark DataFrames (via JDBC or by exporting tables).
- Other BI tools such as Tableau or Excel.
- Python or R notebooks for advanced analytics.

The key idea is that **P4 built the warehouse, and P5 demonstrates how that warehouse supports flexible, tool-agnostic reporting**.

### Reflection

- This task helped me connect a real data warehouse to a professional BI tool.
- I practiced setting up DSNs and verifying relationships across fact and dimension tables.
- I gained experience defining measures in DAX and using them in multiple visuals.
- I also saw how a well-designed star schema makes it easy to move between tools (SQLite, Power BI, and potentially Spark) without rebuilding the data from scratch.
