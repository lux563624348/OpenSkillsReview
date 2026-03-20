#!/usr/bin/env python3
"""Fetch Polymarket Gamma events with pagination and category filtering."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_BASE_URL = "https://gamma-api.polymarket.com/events"
TAGS_URL = "https://gamma-api.polymarket.com/tags"
DEFAULT_USER_AGENT = "Mozilla/5.0 (compatible; Codex Polymarket Skill/1.0)"

_RETRY_DELAYS = (1, 2, 4)  # seconds between retries on 429 / transient errors
ORDER_ALIASES = {
    # Legacy names kept for backwards-compatible CLI usage.
    "volume_24hr": "volume24hr",
    "start_date": "startDate",
    "end_date": "endDate",
    "closed_time": "closedTime",
}
ORDER_CHOICES = (
    "volume24hr",
    "volume",
    "liquidity",
    "startDate",
    "endDate",
    "competitive",
    "closedTime",
    "createdAt",
    "updatedAt",
    # Legacy aliases (mapped before request).
    "volume_24hr",
    "start_date",
    "end_date",
    "closed_time",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Polymarket Gamma events and optionally paginate all results."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--slug")
    parser.add_argument("--tag-id", dest="tag_id")
    parser.add_argument(
        "--category",
        help=(
            "Filter by category name (e.g. sports, crypto, politics, science, tech, "
            "business, entertainment). Resolved to a tag_id via the tags endpoint. "
            "Ignored if --tag-id is also provided."
        ),
    )
    parser.add_argument("--series-id")
    parser.add_argument(
        "--active",
        nargs="?",
        const="true",
        default="true",
        choices=("true", "false"),
        help="Filter active events. Use --active or --active true/false (default: true).",
    )
    parser.add_argument(
        "--closed",
        nargs="?",
        const="true",
        default="false",
        choices=("true", "false"),
        help="Filter closed events. Use --closed or --closed true/false (default: false).",
    )
    parser.add_argument(
        "--archived",
        nargs="?",
        const="true",
        choices=("true", "false"),
        help="Filter archived events. Use --archived or --archived true/false.",
    )
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument(
        "--order",
        choices=ORDER_CHOICES,
        help="Sort field for results.",
    )
    parser.add_argument("--ascending", choices=("true", "false"))
    parser.add_argument(
        "--paginate-all",
        action="store_true",
        help="Fetch all pages until the final partial page.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=True,
        help="Pretty-print JSON output (default: on; use --no-pretty to disable).",
    )
    parser.add_argument(
        "--no-pretty",
        dest="pretty",
        action="store_false",
        help="Output compact JSON.",
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="Print all available category slugs and exit.",
    )
    return parser.parse_args()


def build_query(args: argparse.Namespace, offset: int) -> str:
    order = ORDER_ALIASES.get(args.order, args.order)
    params = {
        "slug": args.slug,
        "tag_id": args.tag_id,
        "series_id": args.series_id,
        "active": args.active,
        "closed": args.closed,
        "archived": args.archived,
        "limit": args.limit,
        "offset": offset,
        "order": order,
        "ascending": args.ascending,
    }
    filtered = {k: v for k, v in params.items() if v is not None}
    return urllib.parse.urlencode(filtered)


def fetch_json(url: str) -> Any:
    for attempt, delay in enumerate((*_RETRY_DELAYS, None), start=1):
        request = urllib.request.Request(url, headers={"User-Agent": DEFAULT_USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and delay is not None:
                print(
                    f"Rate limited (429). Retrying in {delay}s (attempt {attempt})...",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue
            raise
        except urllib.error.URLError as exc:
            if delay is not None:
                print(
                    f"Network error: {exc}. Retrying in {delay}s (attempt {attempt})...",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue
            raise
    raise RuntimeError(f"Failed to fetch {url} after {len(_RETRY_DELAYS) + 1} attempts")


def resolve_category(category: str) -> str:
    """Return a tag_id string matching the given category name/slug (case-insensitive)."""
    tags = fetch_json(TAGS_URL)
    if not isinstance(tags, list):
        raise RuntimeError("Unexpected response from tags endpoint")
    needle = category.strip().lower()
    for tag in tags:
        slug = str(tag.get("slug") or "").lower()
        label = str(tag.get("label") or tag.get("name") or "").lower()
        if needle in (slug, label):
            return str(tag["id"])
    # Partial match fallback
    for tag in tags:
        slug = str(tag.get("slug") or "").lower()
        label = str(tag.get("label") or tag.get("name") or "").lower()
        if needle in slug or needle in label:
            return str(tag["id"])
    available = sorted({
        str(tag.get("slug") or tag.get("label") or "").lower()
        for tag in tags
        if tag.get("slug") or tag.get("label")
    })
    raise RuntimeError(
        f"Category '{category}' not found. Available slugs:\n  "
        + "\n  ".join(available)
    )


def list_categories() -> None:
    tags = fetch_json(TAGS_URL)
    if not isinstance(tags, list):
        raise RuntimeError("Unexpected response from tags endpoint")
    rows = sorted(
        [
            (str(tag.get("slug") or ""), str(tag.get("label") or tag.get("name") or ""), str(tag.get("id", "")))
            for tag in tags
        ],
        key=lambda r: r[0],
    )
    print(f"{'slug':<30} {'label':<30} id")
    print("-" * 70)
    for slug, label, tag_id in rows:
        print(f"{slug:<30} {label:<30} {tag_id}")


def fetch_events(args: argparse.Namespace) -> list[dict[str, Any]]:
    if not args.paginate_all:
        url = f"{args.base_url}?{build_query(args, args.offset)}"
        data = fetch_json(url)
        if not isinstance(data, list):
            raise RuntimeError(f"Expected list payload, got {type(data).__name__}")
        return data

    all_events: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    offset = args.offset

    while True:
        url = f"{args.base_url}?{build_query(args, offset)}"
        data = fetch_json(url)
        if not isinstance(data, list):
            raise RuntimeError(f"Expected list payload, got {type(data).__name__}")

        for event in data:
            event_id = str(event.get("id", ""))
            if event_id and event_id not in seen_ids:
                seen_ids.add(event_id)
                all_events.append(event)

        if len(data) < args.limit:
            break
        offset += args.limit

    return all_events


def main() -> int:
    args = parse_args()
    try:
        if args.list_categories:
            list_categories()
            return 0

        # Resolve --category to a tag_id if --tag-id was not explicitly provided
        if args.category and not args.tag_id:
            args.tag_id = resolve_category(args.category)

        events = fetch_events(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    indent = 2 if args.pretty else None
    json.dump(events, sys.stdout, indent=indent)
    if indent is not None:
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
