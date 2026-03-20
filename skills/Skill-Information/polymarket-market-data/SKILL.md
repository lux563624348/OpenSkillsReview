---
name: polymarket-market-data
description: Download live Polymarket events from Gamma API and summarize/filter them in a compact table format. Read-only, no authentication required.
compatibility: Requires network access to gamma-api.polymarket.com
version: 03/20/2026
Author: Xiang OpenSkillsReview
---

# Polymarket Live Events Summary Skill

## When to use this skill

Use this skill when the user asks to:
- Pull live Polymarket events from Gamma API
- Filter events by keyword, tag/category, or 24h volume
- Summarize events into a compact table view
- Get top active events ranked by 24h volume

Do not use this skill for:
- Placing or managing orders
- Wallet/account authentication flows
- Onchain execution or transaction automation

## Live API Source

Use this endpoint for live active events sorted by 24h volume:

```text
https://gamma-api.polymarket.com/events?active=true&closed=false&order=volume24hr&ascending=false
```

## Script

Use:

- `scripts/live_events_summary.py`

This script:
- Downloads live events directly from the URL above (or reads from a local JSON file)
- Applies filters (`--contains`, `--tag`, `--min-volume24h`, `--top`)
- Outputs rows in this strict format:

```text
<Question Title> | <Strike Label>: Yes: <Yes%> No: <No%> | 24h: <$Volume>
What price will Bitcoin hit in 2026? | $100K: Yes: 40.5% No: 59.5% | 24h: $1.06M
```

If the user asks about any specific Polymarket event, this next flow is mandatory before answering.

## Mandatory: Download JSON First, Then Process (Specific Event Queries)

Use this base URL:

```text
https://gamma-api.polymarket.com/events?active=true&closed=false
```

Routing logic:
- If the user asks a general topic query, you must choose exactly one Tag from `skills/Skill-Information/polymarket-market-data/slug.md` (for example: Crypto, Politics, Finance, Geopolitics, Tech, Economy, Weather), then use that Tag to set `tagSlug`.
- General-topic request format: `base_url&tagSlug=<tag-from-slug.md>`
- If the user asks a specific event query, call: `base_url&slug=<event-slug>`
- Always download JSON first, then run local processing on the downloaded file.

Example mapping for Bitcoin queries:

```text
User intent: bitcoin
Specific event slug: what-price-will-bitcoin-hit-before-2027
Use in request: base_url&slug=what-price-will-bitcoin-hit-before-2027

Output example:
bitcoin reach 100,000 by 12-31-2026, Yes: 40.5%, No: 59.5%
```

```bash
# Specific event query
curl -s "https://gamma-api.polymarket.com/events?active=true&closed=false&slug=what-price-will-bitcoin-hit-before-2027" > /tmp/live_events_<slug>.json


# General topic query (must use one Tag from slug.md)
curl -s "https://gamma-api.polymarket.com/events?active=true&closed=false&tagSlug=crypto" > /tmp/live_events_<tagSlug>.json

# Process downloaded JSON
python3 scripts/live_events_summary.py --input-file /tmp/live_events.json --top 10
```

## Recommended Workflow for general search

```bash
# 1) Quick live summary (top 20 by volume24h)
python3 scripts/live_events_summary.py

# 2) Filter by keyword
python3 scripts/live_events_summary.py --contains bitcoin --top 10

# 3) Filter by tag/category
python3 scripts/live_events_summary.py --tag politics --top 15

# 4) Filter by minimum 24h volume (USD)
python3 scripts/live_events_summary.py --min-volume24h 1000000 --top 25
```

## Output Contract

Always keep this output structure:

```text
<Question Title> | <Strike Label>: Yes: <Yes%> No: <No%> | 24h: <$Volume>
```

## Reference Files

Load only as needed:
- [market-data.md](market-data.md)
- [README.md](README.md)
