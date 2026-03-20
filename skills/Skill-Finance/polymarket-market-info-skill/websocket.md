# WebSocket (Public Channels Only)

This skill only uses no-auth WebSocket channels.

## Channels

| Channel | Endpoint | Auth |
|---------|----------|------|
| Market | `wss://ws-subscriptions-clob.polymarket.com/ws/market` | No |
| Sports | `wss://sports-api.polymarket.com/ws` | No |

## Market Channel

Public. Subscribes by **asset IDs** (token IDs).

### Subscribe

```json
{
  "assets_ids": ["TOKEN_ID_1", "TOKEN_ID_2"],
  "type": "market",
  "custom_feature_enabled": true
}
```

Set `custom_feature_enabled: true` to enable `new_market` and `market_resolved` events.

### Event Types

| Event | Trigger | Key Fields |
|-------|---------|------------|
| `price_change` | Order placed or cancelled | `price_changes[]` with `price`, `size`, `side` |
| `last_trade_price` | Trade executed | `price`, `side`, `size`, `fee_rate_bps` |
| `tick_size_change` | Price hits >0.96 or <0.04 | `old_tick_size`, `new_tick_size` |
| `new_market` | Market created | `question`, `assets_ids`, `outcomes` |
| `market_resolved` | Market resolved | `winning_asset_id`, `winning_outcome` |

Events requiring `custom_feature_enabled: true`: `new_market`, `market_resolved`.

### Example Messages

```json
// price_change
{
  "event_type": "price_change",
  "market": "0xCONDITION_ID",
  "price_changes": [{
    "asset_id": "TOKEN_ID",
    "price": "0.5",
    "size": "200",
    "side": "BUY",
    "hash": "..."
  }],
  "timestamp": "..."
}
```

## Sports Channel

No subscription message needed. Connect and receive all active sports data.

### Example Messages

```json
// Live game update
{
  "type": "sport_result",
  "game_id": "nba-2025-lakers-vs-celtics",
  "sport": "basketball",
  "league": "NBA",
  "status": "in_progress",
  "home_team": "Los Angeles Lakers",
  "away_team": "Boston Celtics",
  "home_score": 87,
  "away_score": 91,
  "clock": "4:32",
  "period": 4,
  "updated_at": "1742478000000"
}
```

```json
// Game finished
{
  "type": "sport_result",
  "game_id": "nba-2025-lakers-vs-celtics",
  "sport": "basketball",
  "league": "NBA",
  "status": "final",
  "home_team": "Los Angeles Lakers",
  "away_team": "Boston Celtics",
  "home_score": 104,
  "away_score": 109,
  "period": 4,
  "updated_at": "1742480400000"
}
```

Key fields:

| Field | Description |
|-------|-------------|
| `game_id` | Unique game identifier |
| `sport` | Sport type (basketball, football, soccer, baseball, etc.) |
| `league` | League name (NBA, NFL, EPL, etc.) |
| `status` | `scheduled`, `in_progress`, `final`, `postponed` |
| `home_score` / `away_score` | Current score |
| `clock` | Time remaining in current period (where applicable) |
| `period` | Current period / quarter / half |
| `updated_at` | Unix timestamp in milliseconds |

> **Note:** The exact field set varies by sport. Always handle missing fields gracefully. The `status: "final"` value is what Polymarket uses to resolve related markets.

## Dynamic Subscribe / Unsubscribe (Market Channel)

```json
// Subscribe to additional assets
{ "assets_ids": ["NEW_TOKEN_ID"], "operation": "subscribe", "custom_feature_enabled": true }

// Unsubscribe from assets
{ "assets_ids": ["OLD_TOKEN_ID"], "operation": "unsubscribe" }
```

## Heartbeat

### Market Channel

Send `PING` every **10 seconds**. Server responds with `PONG`.

```typescript
const ws = new WebSocket("wss://ws-subscriptions-clob.polymarket.com/ws/market");

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: "market",
    assets_ids: ["TOKEN_ID"],
    custom_feature_enabled: true,
  }));
  setInterval(() => ws.send("PING"), 10_000);
};

ws.onmessage = (event) => {
  if (event.data === "PONG") return;
  const msg = JSON.parse(event.data);
  // handle msg.event_type
};
```

### Sports Channel

Server sends `ping` every 5 seconds. Respond with `pong` within 10 seconds or connection closes.

## Troubleshooting

- **Connection closes immediately**: send subscription message right after open
- **Drops after ~10s**: you're not sending PING heartbeats on market channel
- **No messages**: verify asset IDs are correct and markets are active
