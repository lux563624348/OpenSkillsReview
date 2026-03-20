# Market Data (Read-Only)

Primary sources for no-auth market intelligence:
- **Gamma API** for event and market discovery
- **CLOB public endpoints** for pricing

## Rate Limits

Polymarket does not publish official rate limit thresholds. In practice:
- The Gamma API tolerates moderate polling (a few requests per second).
- The CLOB public endpoints are similarly lenient for read traffic.
- `fetch_events.py` retries automatically on HTTP 429 with exponential backoff (1 s → 2 s → 4 s, then fail).
- For large `--paginate-all` runs, add `--limit 100` to reduce per-request payload and avoid triggering server-side limits.

## Gamma API

Base URL: `https://gamma-api.polymarket.com` (no auth required).

### Bundled Scripts

Prefer the local scripts for repeatable workflows:

```bash
# Fetch every active, open event (pretty-printed by default)
python3 scripts/fetch_events.py --active true --closed false --paginate-all
```

### Events Endpoint

```bash
# All active events
GET https://gamma-api.polymarket.com/events?active=true&closed=false&limit=100

# By slug (from polymarket.com/event/{slug})
GET https://gamma-api.polymarket.com/events?slug=fed-decision-in-october

# By tag
GET https://gamma-api.polymarket.com/events?tag_id=100381&limit=10&active=true&closed=false

# By series (sports)
GET https://gamma-api.polymarket.com/events?series_id=10345&active=true&closed=false

# Sorted by 24h volume
GET https://gamma-api.polymarket.com/events?active=true&closed=false&order=volume24hr&ascending=false&limit=100
```

### Markets Endpoint

```bash
# By slug
GET https://gamma-api.polymarket.com/markets?slug=fed-decision-in-october
```

### Sort and Filter Parameters

| Parameter | Values |
|-----------|--------|
| `order` | `volume24hr`, `volume`, `liquidity`, `startDate`, `endDate`, `competitive`, `closedTime`, `createdAt`, `updatedAt` |
| `ascending` | `true` / `false` (default: `false`) |
| `active` | `true` / `false` |
| `closed` | `true` / `false` |
| `limit` | 1-500 (default: 20) |
| `offset` | Pagination offset |

### Pagination

```bash
# Page 1
GET https://gamma-api.polymarket.com/events?active=true&closed=false&limit=50&offset=0

# Page 2
GET https://gamma-api.polymarket.com/events?active=true&closed=false&limit=50&offset=50
```

In practice, the bundled `scripts/fetch_events.py --paginate-all` helper is safer than hand-rolling pagination logic. It increments `offset` by `limit` and stops on the first partial page while deduplicating event IDs across pages.

### Category Filtering

Use `--category` to filter events by named category. The script resolves the name to a `tag_id` automatically via the tags endpoint.

```bash
# List all available categories
python3 scripts/fetch_events.py --list-categories

# Fetch active events in a specific category
python3 scripts/fetch_events.py --category sports --active true --closed false
python3 scripts/fetch_events.py --category crypto --active true --closed false
python3 scripts/fetch_events.py --category politics --active true --closed false

```

Common category slugs: `sports`, `crypto`, `politics`, `science`, `technology`, `business`, `entertainment`, `world`.
`--category` matches on slug or label (case-insensitive, partial match as fallback). If the slug isn't found, the script prints all available slugs and exits with an error.

### Tags and Sports Metadata

```bash
GET https://gamma-api.polymarket.com/tags
GET https://gamma-api.polymarket.com/sports
```

## CLOB Public Read Endpoints

Base URL: `https://clob.polymarket.com` (no auth required for the endpoints below).

### Get Price

```bash
curl "https://clob.polymarket.com/price?token_id=TOKEN_ID&side=BUY"
```

```typescript
const buyPrice = await client.getPrice("TOKEN_ID", "BUY");
const sellPrice = await client.getPrice("TOKEN_ID", "SELL");
```

### Get Midpoint

```typescript
const mid = await client.getMidpoint("TOKEN_ID");
```

### Get Spread

```typescript
const spread = await client.getSpread("TOKEN_ID");
```

### Get Last Trade Price

```typescript
const last = await client.getLastTradePrice("TOKEN_ID");
```

### Get Price History

```typescript
const history = await client.getPricesHistory({
  market: "TOKEN_ID",
  interval: PriceHistoryInterval.ONE_DAY,
  fidelity: 60,
});
```

| Interval | Description |
|----------|-------------|
| `1h` | Last hour |
| `6h` | Last 6 hours |
| `1d` | Last day |
| `1w` | Last week |
| `1m` | Last month |
| `max` | All available |

Use `startTs`/`endTs` for absolute ranges (mutually exclusive with `interval`).

### Batch Read Requests

Batch reads support up to 500 tokens depending on endpoint.

| Single | Batch | REST |
|--------|-------|------|
| `getPrice()` | `getPrices()` | `POST /prices` |
| `getMidpoint()` | `getMidpoints()` | `POST /midpoints` |
| `getSpread()` | `getSpreads()` | `POST /spreads` |
| `getLastTradePrice()` | `getLastTradesPrices()` | - |

## Useful Market Fields

| Field | Description |
|-------|-------------|
| `tokenID` / `asset_id` | ERC1155 token ID for an outcome |
| `conditionID` / `market` | Condition ID identifying the market |
| `minimum_tick_size` | Minimum price increment |
| `slug` | URL-friendly identifier |
| `tokens` | Outcome token list (for example Yes/No token IDs) |
| `neg_risk` | Whether the market is in a linked multi-outcome structure |

## Fetching Strategy

1. For one market, query by slug.
2. For discovery, query by tag or series.
3. For full coverage, use `python3 scripts/fetch_events.py --paginate-all`.
4. Use `active=true&closed=false` unless historical closed markets are required.
5. Prefer events endpoint first because it contains nested market context.
