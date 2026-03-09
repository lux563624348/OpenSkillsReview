---
name: unusual-whales-api
description: Query the Unusual Whales API for unusual options flow, dark pool prints, market tide, and stock greek exposure.
---

# Unusual Whales API Skill

## When to use

Use this skill when the user asks for financial data related to:

- Unusual options activity, "whale" trades, flow alerts, or "hottest chains".
- Dark pool prints, trades, or levels.
- Market sentiment (Market Tide, Net Premium, Put/Call ratios).
- Insider trading, politician trading, or specific stock/option details (Greeks, IV).

## Instructions

You are an expert at querying the Unusual Whales API. Your primary goal is to **avoid widely common hallucinations** regarding this specific API.

### 1. Critical Rules (The "Anti-Hallucination" Protocol)

- **Base URL:** Always use `https://api.unusualwhales.com`
- **Authentication:** All requests MUST include the header: `Authorization: Bearer <API_TOKEN>`
- **Client Header:** All requests MUST include the header: `UW-CLIENT-API-ID: 100001`
- **Method:** All endpoints are `GET` requests. Never use POST, PUT, or DELETE.
- **Strict Whitelist:** You may **ONLY** use endpoints listed in the "Valid Endpoint Reference" section below. If a URL is not on that list, it does not exist.

### 2. Hallucination Blacklist (NEVER USE THESE)

These endpoints are fake but commonly hallucinated. Check your generated code against this list:

- ❌ `/api/options/flow` (Use `/api/option-trades/flow-alerts`)
- ❌ `/api/flow` or `/api/flow/live`
- ❌ `/api/stock/{ticker}/flow` (Use `/api/stock/{ticker}/flow-recent`)
- ❌ `/api/stock/{ticker}/options` (Use `/api/stock/{ticker}/option-contracts`)
- ❌ `/api/unusual-activity`
- ❌ Any URL containing `/api/v1/` or `/api/v2/`
- ❌ Query params `apiKey=` or `api_key=` (Use `Authorization` header only)

### 3. Concept Mapping

Translate user intent to the correct endpoint:

- "Live Flow" / "Whale Trades" / "Option Flow" → `/api/option-trades/flow-alerts`
- "Options Filter" / "Options Screener" / "Flow Filter" -> `/api/screener/option-contracts`
- "Market Sentiment" → `/api/market/market-tide`
- "Dark Pool" → `/api/darkpool/recent` or `/api/darkpool/{ticker}`
- "Contract Greeks" → `/api/stock/{ticker}/greeks`
- "Spot Gamma" / "Spot GEX" / "GEX" / "Gamma Exposure" -> `/api/stock/{ticker}/spot-exposures/strike`

## Valid Endpoint Reference

You must choose the endpoint from this list.

### Core Data & Flow

- **Flow Alerts (Unusual Activity):** `/api/option-trades/flow-alerts`
  - _Params:_ `limit`, `is_call`, `is_put`, `is_otm`, `min_premium`, `ticker_symbol`, `size_greater_oi`
- **Options Screener (Hottest Chains):** `/api/screener/option-contracts`
  - _Params:_ `limit`, `min_premium`, `type`, `is_otm`, `issue_types[]`, `min_volume_oi_ratio`
- **Recent Ticker Flow:** `/api/stock/{ticker}/flow-recent`
- **Dark Pool (Ticker):** `/api/darkpool/{ticker}`
- **Dark Pool (Market Wide):** `/api/darkpool/recent`
- **Market Tide:** `/api/market/market-tide`
- **Net Premium Ticks:** `/api/stock/{ticker}/net-prem-ticks`

### Options, Greeks & IV

- **Option Contracts List and Details:** `/api/stock/{ticker}/option-contracts`
- **Greeks for Each Strike & Expiry:** `/api/stock/{ticker}/greeks`
- **"Static" Gamma Exposure (GEX) by Strike:** `/api/stock/{ticker}/greek-exposure/strike`
- **Spot Gamma Exposure (GEX) by Strike:** `/api/stock/{ticker}/spot-exposures/strike`
- **Interpolated IV and Percentiles:** `/api/stock/{ticker}/interpolated-iv`
- **Options Volume/PC Ratio:** `/api/stock/{ticker}/options-volume`
- **Hottest Chains (Options Screener):** `/api/screener/option-contracts`

### Other Data

- **Insider Trading:** `/api/insider/transactions`
- **Politician Trades:** `/api/congress/recent-trades`
- **News:** `/api/news/headlines`

## Available Skills

- A skill to learn how to check the current api usage and debug rate limit errors: https://unusualwhales.com/skills/uw-api-usage-monitor-skill.md
- A skill when working with institutional data such as 13F files: https://unusualwhales.com/skills/institutional.md

## Examples

### Example 1: Getting Unusual Options Activity (Flow Alerts)

**User:** "Show me the latest unusual option trades for TSLA."
**Code:**

```python
import httpx

url = "https://api.unusualwhales.com/api/option-trades/flow-alerts"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
params = {
    "ticker_symbol": "TSLA",
    "min_premium": 50_000,
    "size_greater_oi": True,  # Opening trades where size > open_interest
    "limit": 10,
    "is_otm": True
}
response = httpx.get(url, headers=headers, params=params)
print(response.json().get("data", []))
# List of dicts with details like 'ticker', 'type', 'total_premium', 'total_size', etc.
```

### Example 2: Screening for Unusually Bullish Option Trades

**User:** "Show me unusually bullish option activity for today."

```python
import httpx

url = "https://api.unusualwhales.com/api/screener/option-contracts"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
params = {
    "limit": 150,
    "is_otm": True,
    "issue_types[]": ["Common Stock", "ADR"],
    "max_dte": 183,
    "max_multileg_volume_ratio": 0.1,
    "min_ask_perc": 0.7,
    "min_volume": 500,
    "min_premium": 250_000,
    "type": "Calls",
    "vol_greater_oi": True,
}
response = httpx.get(url, headers=headers, params=params)
print(response.json().get("data", []))
# List of dicts with details like 'ticker_symbol', 'option_symbol', 'ask_side_volume', 'avg_price', etc.
```

### Example 3: Checking Market Tide (Sentiment)

**User:** "What is the overall market sentiment right now?"
**Code:**

```python
import httpx

url = "https://api.unusualwhales.com/api/market/market-tide"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
params = {"interval_5m": False}
response = httpx.get(url, headers=headers, params=params)
print(response.json().get("data", []))
# List of dicts with details like 'timestamp', 'net_call_premium', 'net_put_premium', etc.
```

### Example 4: Dark Pool Trades

**User:** "Any big dark pool prints on NVDA?"
**Code:**

```python
import httpx

url = "https://api.unusualwhales.com/api/darkpool/NVDA"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
response = httpx.get(url, headers=headers)
print(response.json().get("data", []))
# List of dicts with details like 'ticker', 'price', 'size', 'executed_at', etc.
```

### Example 5: Gamma Exposure (GEX) by Strike

**User:** "Show me the gamma exposure for RIVN puts near current price."
**Code:**

```python
import httpx

url = "https://api.unusualwhales.com/api/stock/RIVN/spot-exposures/strike"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
response = httpx.get(url, headers=headers)
print(response.json().get("data", []))
# List of dicts with details like 'strike', 'put_gamma_oi', 'put_gamma_bid', 'put_gamma_ask', etc.
```