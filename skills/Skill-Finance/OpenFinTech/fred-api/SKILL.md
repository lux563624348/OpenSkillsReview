---
name: fred-api
description: Retrieve macroeconomic time series from the Federal Reserve Economic Data (FRED) API.
---

# FRED API Skill

## When to use

Use this skill when the user asks for:
- US macro time series (GDP, CPI, unemployment, yields, etc.).
- Reproducible macro data pulls with explicit series IDs.

## Key rules

- Use an API key stored in `FRED_API_KEY`.
- Always cite the series ID and frequency.
- Avoid mixing real and nominal series without explicit conversion.

## Quick start (fredapi)

```python
from fredapi import Fred
import os

fred = Fred(api_key=os.environ["FRED_API_KEY"])

# Example: CPI for All Urban Consumers (CPIAUCSL)
cpi = fred.get_series("CPIAUCSL")

# Example: 10-Year Treasury Constant Maturity Rate (DGS10)
dgs10 = fred.get_series("DGS10")
```

## Quick start (raw requests)

```python
import os
import requests

api_key = os.environ["FRED_API_KEY"]
url = "https://api.stlouisfed.org/fred/series/observations"
params = {"series_id": "CPIAUCSL", "api_key": api_key, "file_type": "json"}
response = requests.get(url, params=params)
response.raise_for_status()
obs = response.json()["observations"]
```

## Common series examples

- `GDP` (Gross Domestic Product, quarterly)
- `CPIAUCSL` (CPI, monthly)
- `UNRATE` (Unemployment rate, monthly)
- `DGS10` (10Y Treasury yield, daily)

## Pitfalls

- Daily series have gaps for holidays and weekends.
- Some series are seasonally adjusted; label this clearly.
