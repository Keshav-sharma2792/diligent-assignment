## Diligent Assignment – Synthetic E-Commerce Data Pipeline

### Project Overview
This assignment demonstrates a complete mini data pipeline:
- generate synthetic e-commerce CSV datasets
- ingest the data into a SQLite database
- run a consolidated SQL report via a join query
- push the entire project to GitHub for review

### Repository Layout
```
├─ data/                # synthetic CSV exports
├─ prompts.txt          # reference prompts used in Cursor
├─ ingest.py            # Python script to load CSVs into SQLite
├─ queries.sql          # join query powering the report
├─ run_sql_report.py    # helper to execute queries.sql
└─ README.md
```

### Prompt Summary
- **Prompt 1 – Generate CSVs:** create synthetic e-commerce customers, orders, order items, payments, and products CSV files.
- **Prompt 2 – Build ingestion script:** implement a Python script that loads each CSV into the SQLite `ecommerce.db` database.
- **Prompt 3 – Author SQL join report:** write the SQL query that consolidates the tables into a unified analytics view.

### Running the Project
1. **Ingest CSV data**
   ```
   python ingest.py
   ```
   Populates `ecommerce.db` using the CSVs in `data/`.

2. **Generate the consolidated report**
   ```
   python run_sql_report.py
   ```
   Executes `queries.sql` against `ecommerce.db` and prints the result set.

### Notes
- The `data/` directory may be empty until you run the CSV generation prompt, so add the files before ingesting.
- All scripts were generated with Cursor prompts and lightly edited for clarity.

### Submission
Push the project to GitHub and share the public repository link with the reviewers to complete the assignment.

