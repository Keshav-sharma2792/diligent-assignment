"""Utility to run the consolidated e-commerce report SQL."""

from __future__ import annotations

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ecommerce.db"
QUERY_FILE = BASE_DIR / "queries.sql"


def load_query() -> str:
    if not QUERY_FILE.exists():
        raise FileNotFoundError(f"Query file not found: {QUERY_FILE}")

    query = QUERY_FILE.read_text(encoding="utf-8").strip()
    if not query:
        raise ValueError("Query file is empty.")
    return query


def fetch_report(query: str) -> list[sqlite3.Row]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(query).fetchall()


def print_report(rows: list[sqlite3.Row]) -> None:
    if not rows:
        print("Report returned no rows.")
        return

    headers = rows[0].keys()
    table = [
        ["" if row[col] is None else str(row[col]) for col in headers]
        for row in rows
    ]

    widths = [
        max(len(col), *(len(row[idx]) for row in table))
        for idx, col in enumerate(headers)
    ]

    def format_row(values: list[str]) -> str:
        return " | ".join(value.ljust(widths[idx]) for idx, value in enumerate(values))

    separator = "-+-".join("-" * w for w in widths)

    print(format_row(list(headers)))
    print(separator)
    for row in table:
        print(format_row(row))


def main() -> None:
    query = load_query()
    rows = fetch_report(query)
    print_report(rows)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Failed to run report: {exc}")

