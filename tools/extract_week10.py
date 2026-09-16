#!/usr/bin/env python3
"""Regenerate data/england-1974-75-division1-week10.csv from source.

This script is committed so the provenance of the bundled test-fixture data
is transparent and reproducible, rather than the CSV just appearing with no
paper trail. See data/SOURCE.md for the reasoning behind the cutoff date.

Usage:
    python3 tools/extract_week10.py
"""
from __future__ import annotations

import csv
import pathlib
import urllib.request

SOURCE_URL = (
    "https://raw.githubusercontent.com/jalapic/engsoccerdata/master/"
    "data-raw/england.csv"
)
SEASON = "1974"
DIVISION = "1"
CUTOFF_DATE = "1974-09-28"  # see data/SOURCE.md for why this date

HERE = pathlib.Path(__file__).resolve().parent
OUTPUT_PATH = HERE.parent / "data" / "england-1974-75-division1-week10.csv"


def main() -> None:
    with urllib.request.urlopen(SOURCE_URL) as response:
        raw = response.read().decode("utf-8")

    reader = csv.DictReader(raw.splitlines())
    rows = [
        r
        for r in reader
        if r["Season"] == SEASON and r["division"] == DIVISION and r["Date"] <= CUTOFF_DATE
    ]
    rows.sort(key=lambda r: (r["Date"], r["home"]))

    with OUTPUT_PATH.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "home_team", "home_goals", "away_team", "away_goals"])
        for r in rows:
            writer.writerow([r["Date"], r["home"], r["hgoal"], r["visitor"], r["vgoal"]])

    print(f"Wrote {len(rows)} matches to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
