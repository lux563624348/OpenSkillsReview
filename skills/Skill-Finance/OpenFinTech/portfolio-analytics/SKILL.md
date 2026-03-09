---
name: portfolio-analytics
description: Compute portfolio performance, risk metrics, and attribution from return series using pandas and numpy.
---

# Portfolio Analytics Skill

## When to use

Use this skill when the user asks for:
- Portfolio returns, cumulative performance, or risk metrics.
- Sharpe/Sortino, drawdowns, or beta vs a benchmark.
- Simple allocation backtests from weight series.

## Key rules

- Always state the return frequency (daily, monthly) and annualization factor.
- Use log or simple returns consistently; do not mix.
- If using risk-free rate, specify the source and frequency.

## Quick start

```python
import numpy as np
import pandas as pd

# returns: pd.Series of daily simple returns
ann_factor = 252

cagr = (1 + returns).prod() ** (ann_factor / len(returns)) - 1
vol = returns.std() * np.sqrt(ann_factor)
sharpe = (returns.mean() * ann_factor) / vol

# Max drawdown
cum = (1 + returns).cumprod()
peak = cum.cummax()
drawdown = (cum / peak) - 1
max_dd = drawdown.min()
```

## Benchmark beta

```python
# r_p, r_b are aligned return series
cov = np.cov(r_p, r_b)[0, 1]
beta = cov / np.var(r_b)
```

## Pitfalls

- Ensure timestamps align and missing data is handled explicitly.
- Annualization assumes independent, identically distributed returns; note limitations.
