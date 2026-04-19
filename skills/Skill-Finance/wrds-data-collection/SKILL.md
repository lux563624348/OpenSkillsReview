---
name: wrds-data-collection
description: Collect financial research data from WRDS using Python connections and SQL pushdown queries. Use when building reproducible extraction workflows, filtering WRDS datasets, pulling firm-level or security-level panels, validating row counts, or writing a data collection procedure for finance or economics research.
---

# WRDS Data Collection

Use this skill when the task is to pull research data from WRDS with Python, apply SQL filters at the source, and save a reproducible panel for analysis.

## Procedure

1. Connect to WRDS in Python with the project credentials.
2. Identify the exact library, table, key fields, and date range before writing code.
3. Push all row filters, joins, and column selection into SQL.
4. Fetch only the reduced result set into pandas.
5. Standardize identifiers, dates, and numeric fields after loading.
6. Save raw extracts separately from cleaned analysis files.
7. Log the query, pull date, row counts, and any exclusions.

## Working Rules

- Prefer SQL pushdown over pulling full tables into Python.
- Select only the fields needed for the analysis.
- Pull in chunks when the table is large or the date range is long.
- Validate the extract by comparing SQL counts with the loaded dataframe.
- Keep raw and processed data in separate folders.
- Write reusable code so the same query can be rerun later.

## Reusable Resources

- Use [`references/wrds_query_templates.md`](references/wrds_query_templates.md) for source-specific SQL patterns for Compustat, CRSP, and Thomson Reuters / I/B/E/S.
- Use [`scripts/wrds_extract.py`](scripts/wrds_extract.py) when you want a reproducible command-line extraction workflow with optional export to CSV or Parquet.

## Standard Extraction Pattern

```python
import wrds
import pandas as pd

conn = wrds.Connection()

sql = """
select gvkey, datadate, at, sale, emp
from comp.funda
where indfmt = 'INDL'
  and datafmt = 'STD'
  and popsrc = 'D'
  and consol = 'C'
  and fyear between 2000 and 2024
"""

df = conn.raw_sql(sql)
df["datadate"] = pd.to_datetime(df["datadate"])
```

## Output Expectations

When asked to draft the procedure, produce:

- A short description of the dataset and source table
- The Python connection code
- The SQL query with filters
- The dataframe cleaning and export steps
- A brief validation note

