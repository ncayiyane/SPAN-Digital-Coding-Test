#!/usr/bin/env python3
"""Verify that 1974-09-28 is the correct "week 10" cutoff date.

Downloads the same source dataset used by extract_week10.py, tallies games
played per club after each distinct match date in the 1974/75 First
Division season, and prints the point at which a 16-clubs-on-10-games /
6-clubs-on-9-games split first appears. This is the actual evidence behind
the cutoff date hardcoded in extract_week10.py and documented in
data/SOURCE.md — run this script to reproduce that evidence yourself
rather than taking the claim on faith.

Usage:
    python3 tools/verify_cutoff.py
"""
from __future__ import annotations

import csv
import urllib.request
from collections import Counter, defaultdict

SOURCE_URL = (
    "https://raw.githubusercontent.com/jalapic/engsoccerdata/master/"
    "data-raw/england.csv"
)
SEASON = "1974"
DIVISION = "1"


def main() -> None:
    with urllib.request.urlopen(SOURCE_URL) as response:
        raw = response.read().decode("utf-8")

    reader = csv.DictReader(raw.splitlines())
    rows = [
        r for r in reader if r["Season"] == SEASON and r["division"] == DIVISION
    ]
    print(f"Total {SEASON}/{int(SEASON) + 1 - 1900:02d} Division 1 matches: {len(rows)}")

    dates = sorted(set(r["Date"] for r in rows))
    games_played: dict[str, int] = defaultdict(int)

    for d in dates:
        for r in rows:
            if r["Date"] == d:
                games_played[r["home"]] += 1
                games_played[r["visitor"]] += 1

        split = Counter(games_played.values())
        marker = ""
        if split == Counter({9: 6, 10: 16}):
            marker = "  <-- 16 clubs on 10 games, 6 clubs on 9 games"
        print(f"{d}: {dict(sorted(split.items()))}{marker}")


if __name__ == "__main__":
    main()
