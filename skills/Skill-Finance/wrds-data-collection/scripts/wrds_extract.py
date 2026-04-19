#!/usr/bin/env python3
"""Run a WRDS SQL query and export the result.

Examples:
    python wrds_extract.py --sql-file query.sql --output data/raw/compustat.csv
    python wrds_extract.py --query "select * from comp.funda limit 10" --output sample.parquet
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import pandas as pd


def connect():
    import wrds

    return wrds.Connection()


def load_sql(args: argparse.Namespace) -> str:
    if args.sql_file:
        return Path(args.sql_file).read_text()
    if args.query:
        return args.query
    raise ValueError("Provide either --sql-file or --query.")


def execute_query(conn, sql: str) -> pd.DataFrame:
    if getattr(conn, "raw_sql", None) is None:
        raise AttributeError("WRDS connection does not expose raw_sql().")
    return conn.raw_sql(sql)


def export_frame(df: pd.DataFrame, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() == ".parquet":
        df.to_parquet(output, index=False)
    else:
        df.to_csv(output, index=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a WRDS query and export the results.")
    parser.add_argument("--sql-file", type=Path, help="Path to a file containing SQL.")
    parser.add_argument("--query", help="SQL query string.")
    parser.add_argument("--output", type=Path, required=True, help="Output path (.csv or .parquet).")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    sql = load_sql(args)

    conn = connect()
    try:
        df = execute_query(conn, sql)
    finally:
        try:
            conn.close()
        except Exception:
            pass

    export_frame(df, args.output)
    print(f"saved {len(df):,} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

