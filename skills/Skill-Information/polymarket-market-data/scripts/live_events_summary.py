#!/usr/bin/env python3
"""Download live Polymarket events and print a compact summary table."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from typing import Any


DEFAULT_URL = (
    "https://gamma-api.polymarket.com/events"
    "?active=true&closed=false&order=volume24hr&ascending=false"
)
DEFAULT_USER_AGENT = "Mozilla/5.0 (compatible; PolymarketMarketDataSkill/1.0)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download live events from Gamma API and summarize from live_events_<slug>.json."
    )
    parser.add_argument("--url", default=DEFAULT_URL, help="Gamma events endpoint URL.")
    parser.add_argument("--input-file", help="Optional local JSON file. Skips network when set.")
    parser.add_argument(
        "--contains",
        help="Case-insensitive keyword filter against title/question text.",
    )
    parser.add_argument(
        "--tag",
        help="Case-insensitive tag/category filter (e.g. politics, finance, weather).",
    )
    parser.add_argument("--min-volume24h", type=float, default=0.0)
    parser.add_argument("--top", type=int, default=20)
    return parser.parse_args()


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": DEFAULT_USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def load_events(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = fetch_json(args.url)

    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [e for e in data if isinstance(e, dict)]
    raise ValueError(f"Expected list/dict payload, got {type(data).__name__}")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def parse_list_field(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("[") and text.endswith("]"):
            try:
                loaded = json.loads(text)
                if isinstance(loaded, list):
                    return loaded
            except json.JSONDecodeError:
                return []
    return []


def extract_yes_no_probs(record: dict[str, Any]) -> tuple[float | None, float | None]:
    outcomes = [normalize_text(x) for x in parse_list_field(record.get("outcomes"))]
    prices = [as_float(x, 0.0) for x in parse_list_field(record.get("outcomePrices"))]
    if len(outcomes) == len(prices) and outcomes:
        idx_yes = next((i for i, o in enumerate(outcomes) if o.lower() == "yes"), -1)
        idx_no = next((i for i, o in enumerate(outcomes) if o.lower() == "no"), -1)
        if idx_yes >= 0 and idx_no >= 0:
            return (prices[idx_yes] * 100.0, prices[idx_no] * 100.0)

    return (None, None)


def event_title(event: dict[str, Any]) -> str:
    for key in ("question", "title", "slug"):
        text = normalize_text(event.get(key))
        if text:
            return text
    return "Untitled Event"


def slug_to_readable(slug: str) -> str:
    text = normalize_text(slug).lower()
    if not text:
        return "untitled event"

    # Remove trailing numeric suffixes often appended for uniqueness
    # while keeping date fragments like day/year (e.g. 31-2026).
    tokens = text.split("-")
    while tokens and tokens[-1].isdigit() and len(tokens[-1]) <= 3:
        tokens.pop()
    text = " ".join(tokens)
    if text.startswith("will "):
        text = text[5:]

    month_map = {
        "january": "01",
        "february": "02",
        "march": "03",
        "april": "04",
        "may": "05",
        "june": "06",
        "july": "07",
        "august": "08",
        "september": "09",
        "october": "10",
        "november": "11",
        "december": "12",
    }
    parts = text.split()
    for i in range(len(parts) - 2):
        month = month_map.get(parts[i], "")
        day = parts[i + 1]
        year = parts[i + 2]
        if month and day.isdigit() and year.isdigit() and len(year) == 4:
            parts[i : i + 3] = [f"{month}-{int(day):02d}-{year}"]
            break

    for i, token in enumerate(parts):
        if token.isdigit() and len(token) >= 5:
            parts[i] = f"{int(token):,}"
    return " ".join(parts)


def market_label(market: dict[str, Any], idx: int) -> str:
    # Prefer explicit strike labels in question/title/slug like "$100k strike".
    text = " ".join(
        normalize_text(market.get(k))
        for k in ("question", "title", "slug")
        if normalize_text(market.get(k))
    )
    token_match = re.search(r"\$?\s*(\d[\d,]*(?:\.\d+)?)\s*([kKmMbB])\b", text)
    if token_match:
        num = token_match.group(1).replace(",", "")
        suffix = token_match.group(2).upper()
        return f"${num}{suffix}"

    raw_num_match = re.search(r"\$?\s*(\d{4,})\b", text)
    if raw_num_match:
        value = int(raw_num_match.group(1))
        if value % 1_000_000 == 0:
            return f"${value // 1_000_000}M"
        if value % 1_000 == 0:
            return f"${value // 1_000}K"
        return f"${value:,}"

    return f"Market {idx}"


def event_tags(event: dict[str, Any]) -> list[str]:
    raw_tags = event.get("tags")
    if not isinstance(raw_tags, list):
        return []
    collected: list[str] = []
    for t in raw_tags:
        if isinstance(t, dict):
            for key in ("slug", "label", "name"):
                val = normalize_text(t.get(key))
                if val:
                    collected.append(val.lower())
                    break
        else:
            val = normalize_text(t)
            if val:
                collected.append(val.lower())
    return collected


def match_filters(event: dict[str, Any], contains: str | None, tag: str | None) -> bool:
    if contains:
        title = event_title(event).lower()
        if contains.lower() not in title:
            return False
    if tag:
        tag_needle = tag.lower()
        if tag_needle not in event_tags(event):
            return False
    return True


def format_usd_compact(value: float) -> str:
    amount = max(value, 0.0)
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f}B"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.2f}M"
    if amount >= 1_000:
        return f"${amount / 1_000:.2f}K"
    return f"${amount:,.2f}"


def summarize(events: list[dict[str, Any]], args: argparse.Namespace) -> list[str]:
    filtered = []
    for event in events:
        volume24h = as_float(event.get("volume24hr"), as_float(event.get("volume"), 0.0))
        if volume24h < args.min_volume24h:
            continue
        if not match_filters(event, args.contains, args.tag):
            continue
        filtered.append(event)

    filtered.sort(
        key=lambda e: as_float(e.get("volume24hr"), as_float(e.get("volume"), 0.0)),
        reverse=True,
    )
    if args.top > 0:
        filtered = filtered[: args.top]

    lines = []
    for event in filtered:
        title = event_title(event)
        markets = event.get("markets")
        market_rows = [m for m in markets if isinstance(m, dict)] if isinstance(markets, list) else []

        if market_rows:
            for idx, market in enumerate(market_rows, start=1):
                yes_prob, no_prob = extract_yes_no_probs(market)
                if yes_prob is None or no_prob is None:
                    continue
                label = market_label(market, idx)
                volume24h = as_float(
                    market.get("volume24hr"),
                    as_float(market.get("volume"), as_float(event.get("volume24hr"), as_float(event.get("volume"), 0.0))),
                )
                lines.append(
                    f"{title} | {label}: Yes: {yes_prob:.1f}% No: {no_prob:.1f}% | 24h: {format_usd_compact(volume24h)}"
                )
            continue

        # Fallback for payloads that only provide event-level outcomes.
        slug = normalize_text(event.get("slug"))
        fallback_title = title if title and title != "Untitled Event" else (slug_to_readable(slug) if slug else "Untitled Event")
        yes_prob, no_prob = extract_yes_no_probs(event)
        if yes_prob is None or no_prob is None:
            lines.append(f"{fallback_title}, Yes/No prices unavailable")
            continue
        volume24h = as_float(event.get("volume24hr"), as_float(event.get("volume"), 0.0))
        lines.append(
            f"{fallback_title} | Event: Yes: {yes_prob:.1f}% No: {no_prob:.1f}% | 24h: {format_usd_compact(volume24h)}"
        )
    return lines


def main() -> int:
    args = parse_args()
    try:
        events = load_events(args)
        lines = summarize(events, args)
    except urllib.error.URLError as exc:
        print(f"error: network fetch failed: {exc}", file=sys.stderr)
        print(
            "hint: run with --input-file after downloading JSON, e.g. "
            "curl -s \"https://gamma-api.polymarket.com/events?active=true&closed=false&slug=what-price-will-bitcoin-hit-before-2027\" "
            "> /tmp/live_events_what-price-will-bitcoin-hit-before-2027.json",
            file=sys.stderr,
        )
        print(
            "hint: python3 scripts/live_events_summary.py --input-file /tmp/live_events_what-price-will-bitcoin-hit-before-2027.json --top 10",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
