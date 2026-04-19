# WRDS Query Templates

Use these as starting points. Adjust table names and fields to match the WRDS package available in the account.

## 1. Compustat: firm fundamentals

Use this for firm-year panels with accounting variables.

```sql
select
    gvkey,
    datadate,
    fyear,
    at,
    sale,
    emp,
    revt,
    ni
from comp.funda
where indfmt = 'INDL'
  and datafmt = 'STD'
  and popsrc = 'D'
  and consol = 'C'
  and fyear between 2000 and 2024
  and at is not null
```

Common refinements:

- Restrict to a fiscal year window.
- Add industry filters if needed.
- Join on `gvkey` to other Compustat tables such as segment or annual stock data.

## 2. CRSP: monthly stock file

Use this for security-level returns, prices, and market capitalization.

```sql
select
    permno,
    date,
    ret,
    prc,
    shrout,
    vol,
    cfacpr,
    cfacshr
from crsp.msf
where date between '2000-01-01' and '2024-12-31'
  and permno is not null
```

Common refinements:

- Filter out non-common share codes if the study requires common equity only.
- Merge with `crsp.msenames` for share codes and name history.
- Compute market cap after loading as `abs(prc) * shrout / 1000`.

## 3. Thomson Reuters / I/B/E/S: analyst estimates

WRDS subscriptions differ, so confirm the exact table names before running. A common pattern is to pull EPS estimates or summary data.

```sql
select
    ticker,
    cusip,
    statpers,
    fpedats,
    measure,
    value,
    numest
from ibes.statsum_epsus
where statpers between '2000-01-01' and '2024-12-31'
```

Alternative detail-style pull:

```sql
select
    ticker,
    cusip,
    statpers,
    fpedats,
    value,
    analyst,
    estimator
from ibes.det_epsus
where statpers between '2000-01-01' and '2024-12-31'
```

Common refinements:

- Filter by `measure`, `fpi`, or forecast horizon.
- Deduplicate by company, fiscal period, and forecast date.
- Join to Compustat or CRSP after standardizing identifiers.

## Extraction Checklist

Before running any query:

1. Confirm the WRDS library and table exist.
2. Check the key fields and date field names.
3. Apply the narrowest possible `where` clause.
4. Select only the columns needed downstream.
5. Count rows in SQL if the result is large.

