"""Command-line interface: read match results, print a league table.

Usage:
    python -m league_table.cli --input matches.csv --output table.csv
    python -m league_table.cli < matches.csv > table.csv
    cat matches.csv | python -m league_table.cli --rules modern
"""
from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .rules import RULESETS_BY_NAME
from .table import build_table, read_matches, write_table


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="league-table",
        description="Calculate a football league standings table from a CSV of match results.",
    )
    parser.add_argument(
        "--input",
        "-i",
        default=None,
        help="Path to the input results CSV (default: read from stdin).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Path to write the output table CSV (default: write to stdout).",
    )
    parser.add_argument(
        "--rules",
        choices=sorted(RULESETS_BY_NAME),
        default="1974-75",
        help=(
            "Which scoring/tie-break rules to apply. '1974-75' (the default) "
            "is what the English First Division actually used that season: "
            "2 points for a win, ties broken by goal average. 'modern' uses "
            "3 points for a win and goal difference, for comparison."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    # Opened manually (rather than via argparse.FileType) so we can pass
    # newline="" on the output side -- required by the csv module to avoid
    # extra blank lines, and not something FileType supports directly.
    input_stream = open(args.input, "r", encoding="utf-8") if args.input else sys.stdin
    output_stream = (
        open(args.output, "w", encoding="utf-8", newline="") if args.output else sys.stdout
    )

    try:
        matches = read_matches(input_stream)
        rules = RULESETS_BY_NAME[args.rules]
        rows = build_table(matches, rules)
        write_table(rows, output_stream)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        if input_stream is not sys.stdin:
            input_stream.close()
        if output_stream is not sys.stdout:
            output_stream.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
