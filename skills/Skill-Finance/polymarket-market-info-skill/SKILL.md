---
name: polymarket-market-data
description: Polymarket read-only integration focused on information collection with no authentication required. Covers market discovery (Gamma API), read-only pricing data (CLOB public endpoints), and real-time public streams (market and sports WebSocket channels). Use when building dashboards, analytics agents, scanners, alerts, and research tools that do not place orders or execute transactions.
compatibility: Requires network access to Polymarket public APIs (gamma-api.polymarket.com, clob.polymarket.com, ws-subscriptions-clob.polymarket.com, sports-api.polymarket.com)
version: 03/20/2026
Author: Xiang
---

# Polymarket Market Data Skill

## When to use this skill

Use this skill when the user asks about or needs to build:
- Market data fetching from Polymarket APIs
- Event and market discovery by slug, tag, series, or pagination
- Trending or top Polymarket event discovery
- Read-only pricing queries
- Real-time market feed subscriptions over public WebSocket channels
- Sports feed consumption from Polymarket sports WebSocket

Do not use this skill for:
- Authentication flows or API key management
- Order placement, order cancellation, or account-level trading workflows
- Bridge, relayer, gasless, or onchain transaction execution

## API Configuration

| API | Base URL | Auth | Purpose |
|-----|----------|------|---------|
| Gamma API | `https://gamma-api.polymarket.com` | None | Events, markets, tags, sports metadata |
| CLOB (read endpoints) | `https://clob.polymarket.com` | None | Public price, midpoint, spread, history |
| WebSocket (Market) | `wss://ws-subscriptions-clob.polymarket.com/ws/market` | None | Real-time market updates |
| WebSocket (Sports) | `wss://sports-api.polymarket.com/ws` | None | Live sports updates |

## Recommended Workflow

Use the bundled script for repeatable event discovery:

```bash
# Fetch all active events
python3 scripts/fetch_events.py --active true --closed false --paginate-all --no-pretty 

# Fetch trending events (top open events by 24h volume)
python3 scripts/fetch_events.py --active true --closed false --order volume24hr --ascending false --limit 20 --no-pretty
```

Output format (strict):

```text
<Question Title> | Predicted: <Yes/No> (<Probability%>) | 24h: <$Volume>
Will Bitcoin reach $150,000 in March? | Predicted: No (99.8%) | 24h: $732.93K
Will ETH outperform BTC this week? | Predicted: Yes (62.4%) | 24h: $1.00M
```

## Core Pattern: Fetch Active Events

```bash
python3 scripts/fetch_events.py --active true --closed false --limit 100
```

## Core Pattern: Fetch Trending Events

Treat "trending events" as the highest-volume currently active events unless the user specifies a different definition.

```bash
# Top trending events across Polymarket
python3 scripts/fetch_events.py --active true --closed false --order volume24hr --ascending false --limit 20

# Trending events within a category
python3 scripts/fetch_events.py --category sports --active true --closed false --order volume24hr --ascending false --limit 20
python3 scripts/fetch_events.py --category crypto --active true --closed false --order volume24hr --ascending false --limit 20
```

## Core Pattern: Fetch Events by Category

```bash
# List available categories
python3 scripts/fetch_events.py --list-categories

# Filter by category name
python3 scripts/fetch_events.py --category sports --active true --closed false
python3 scripts/fetch_events.py --category crypto --active true --closed false
python3 scripts/fetch_events.py --category politics --active true --closed false
```

## Core Pattern: Read Price

```bash
curl "https://clob.polymarket.com/price?token_id=TOKEN_ID&side=BUY"
```

## Core Pattern: Public WebSocket Subscribe

```json
{
  "type": "market",
  "assets_ids": ["TOKEN_ID"],
  "custom_feature_enabled": true
}
```

Send `PING` every 10 seconds; ignore `PONG`.

## Reference files (load on demand)

Only read these when the task requires deeper detail:

- **Market data** (Gamma API + CLOB read endpoints): [market-data.md](market-data.md)
- **WebSocket** (public market + sports channels): [websocket.md](websocket.md)
- **Scripts** (fetch/paginate active events): `scripts/fetch_events.py`
