# Polymarket Market Data Skill

Agent skill for Polymarket information collection with no authentication required.

Scope is intentionally read-only:
- Discover markets and events
- Fetch public pricing data
- Stream real-time public market and sports updates

No trading or transaction workflows are included.

## What's Included

```
polymarket-market-data/
├── SKILL.md          # Entry point — read-only scope and quick patterns
├── README.md         # This file
├── market-data.md    # Gamma API + CLOB read-only market data
├── scripts/
│   └── fetch_events.py           # Fetch/paginate events; category filter; 429 retry
└── websocket.md      # Public market and sports WebSocket channels
```

## API Endpoints (No Auth)

| API | Base URL | Auth Required |
|-----|----------|---------------|
| Gamma API | `https://gamma-api.polymarket.com` | No |
| CLOB (read) | `https://clob.polymarket.com` | No |
| WS Market | `wss://ws-subscriptions-clob.polymarket.com/ws/market` | No |
| WS Sports | `wss://sports-api.polymarket.com/ws` | No |

## Use Cases

- Market monitoring dashboards
- Trend scanners and watchlists
- Alerting systems for price changes
- Research agents that summarize active markets
- Sports market feed consumers

## File Guide

| File | Read when you need to... |
|------|--------------------------|
| [SKILL.md](SKILL.md) | Start quickly with read-only patterns |
| [market-data.md](market-data.md) | Fetch events/markets, prices, spreads, and history |
| [websocket.md](websocket.md) | Subscribe to public market/sports streams and handle heartbeats |
| `scripts/fetch_events.py` | Pull one page or the full active event set from Gamma; filter by `--category`; 429 retry |
