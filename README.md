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

# 📈 P5 – Cross-Platform Reporting with Power BI & Spark

P5 extends the BI pipeline by connecting the P4 data warehouse to reporting tools and performing OLAP analysis (slice, dice, drilldown). Windows users complete reporting using **Power BI**, while Mac/Linux users complete the same steps using **Spark SQL**. This ensures cross-platform skill development for modern BI environments.

---

# 🔌 Task 1 – Install & Configure Power BI + SQLite ODBC (Windows)

### Completed Steps

- Installed **Power BI Desktop**
- Installed SQLite ODBC driver for Windows
- Created DSN: `SmartSalesDSN`
- Mapped DSN to:

---

# 📈 P5 – Cross-Platform Reporting with Power BI & Spark

P5 extends the BI pipeline by connecting the P4 data warehouse to reporting tools and performing OLAP analysis (slice, dice, drilldown). Windows users complete reporting using Power BI, while Mac/Linux users complete the same steps using Spark SQL. This ensures cross-platform skill development for modern BI environments.

---

# 🔌 Task 1 – Install & Configure Power BI + SQLite ODBC (Windows)

Completed Steps:

- Installed Power BI Desktop
- Installed SQLite ODBC driver for Windows
- Created DSN: SmartSalesDSN
- Mapped DSN to the DW file:

\`\`\`
data/dw/smart_sales.db
\`\`\`

Power BI now connects directly to the Smart Store data warehouse.

---

# 📥 Task 2 – Load Data Warehouse Tables into Power BI

Tables loaded from the DSN connection:

- dim_customer
- dim_product
- fact_sales

Relationships were verified in Model View.

---

# 🧮 Task 3 – SQL Querying in Power Query (Advanced Editor)

Power Query was used to build a custom SQL query titled “Top Customers.”

Steps completed:

1. Open Transform Data
2. Create Blank Query
3. Open Advanced Editor
4. Insert SQL using DSN SmartSalesDSN
5. Join fact and dimension tables
6. Group and sort by total spending
7. Close & Apply

M Code used:

\`\`\`
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
\`\`\`

---

# 🧊 Task 4 – OLAP: Slice, Dice & Drilldown

## Slicing (Date Range Filters)

- Extracted Year, Quarter, and Month fields in Power Query
- Added a date slicer configured with the “Between” option

## Dicing (Two Dimensions)

Created a Matrix visual to break down data across two dimensions:

- Rows: Product Category
- Columns: Region (or another categorical field)
- Values: Total Sales

## Drilldown (Year → Quarter → Month)

Configured a hierarchy and enabled drilldown on a line or column chart:

- Year
- Quarter
- Month

Drill functionality was tested and confirmed.

---

# 📊 Task 5 – Visualizations Created

Visuals completed:

- Top Customers bar chart
- Sales Trends line chart (with Year → Quarter → Month drilldown)
- Product Category slicer
- Matrix visual for multi-dimensional dicing

All visuals support interactive filtering and drilldown.

---

# 🔗 Quick Links for P5

- Power BI Desktop (Windows Store)
- SQLite ODBC Driver – Christian Werner (x64)
- DSN Name: SmartSalesDSN
- Data Warehouse File: data/dw/smart_sales.db

---

# 🗂 Git Commands for P5

\`\`\`
git add README.md
git commit -m "Add complete P5 reporting workflow with SQL and OLAP"
git push
\`\`\`

---
