---
name: yfinance
description: Download equity, ETF, and crypto price history and basic fundamentals using the yfinance Python library.
---

# yfinance Skill

## When to use

Use this skill when the user asks for:
- Historical prices, returns, or volatility for stocks/ETFs/indices.
- Corporate actions like dividends or splits.
- Basic company info (sector, market cap, financial statements) when yfinance is acceptable.

## Key rules

- Prefer `yfinance` for quick, non-critical data pulls. For regulated filings or official figures, use SEC or company reports.
- Always be explicit about adjustments: `auto_adjust=True` for total-return style prices, or keep `auto_adjust=False` and adjust manually.
- Use timezone-aware date handling and state the time zone if returning timestamps.

## Quick start

```python
import yfinance as yf

# Single ticker
spy = yf.Ticker("SPY")
prices = spy.history(period="5y", interval="1d", auto_adjust=True)

# Multiple tickers
data = yf.download(["AAPL", "MSFT"], period="3y", auto_adjust=True)

# Corporate actions
dividends = spy.dividends
splits = spy.splits

# Basic fundamentals
info = spy.info  # may be partial
```

## Common patterns

- Total return series:
```python
prices = yf.download("SPY", start="2015-01-01", auto_adjust=True)["Close"]
```

- Daily returns:
```python
returns = prices.pct_change().dropna()
```

- Volatility (annualized):
```python
vol = returns.std() * (252 ** 0.5)
```

## Pitfalls

- `info` is not always complete or current.
- Intraday data often has gaps and limited history.
- Crypto tickers follow `BTC-USD` style symbols.
