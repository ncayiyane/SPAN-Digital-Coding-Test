"""Turn a list of match results into an ordered league table."""
from __future__ import annotations

import csv
from typing import Iterable, Sequence, TextIO

from .models import MatchResult, TableRow, TeamRecord
from .rules import RuleSet

REQUIRED_INPUT_COLUMNS = ("date", "home_team", "home_goals", "away_team", "away_goals")
OUTPUT_COLUMNS = (
    "position",
    "team",
    "played",
    "won",
    "drawn",
    "lost",
    "goals_for",
    "goals_against",
    "goal_average",
    "points",
)


def read_matches(source: TextIO) -> list[MatchResult]:
    """Parse match results from an open CSV file (or any text stream).

    Expected header: date,home_team,home_goals,away_team,away_goals
    (extra columns are ignored; column order does not matter).
    """
    reader = csv.DictReader(source)
    if reader.fieldnames is None:
        raise ValueError("Input CSV is empty -- expected a header row")

    missing = [c for c in REQUIRED_INPUT_COLUMNS if c not in reader.fieldnames]
    if missing:
        raise ValueError(
            f"Input CSV is missing required column(s): {', '.join(missing)}. "
            f"Expected header: {','.join(REQUIRED_INPUT_COLUMNS)}"
        )

    matches: list[MatchResult] = []
    for line_no, row in enumerate(reader, start=2):  # header is line 1
        try:
            matches.append(
                MatchResult(
                    date=row["date"].strip(),
                    home_team=row["home_team"].strip(),
                    home_goals=int(row["home_goals"]),
                    away_team=row["away_team"].strip(),
                    away_goals=int(row["away_goals"]),
                )
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise ValueError(f"Invalid data on line {line_no} of input CSV: {exc}") from exc
    return matches


def build_records(matches: Iterable[MatchResult]) -> dict[str, TeamRecord]:
    """Fold match results into a per-team win/draw/loss/goals record."""
    records: dict[str, TeamRecord] = {}

    def record_for(team: str) -> TeamRecord:
        if team not in records:
            records[team] = TeamRecord(team=team)
        return records[team]

    for m in matches:
        home = record_for(m.home_team)
        away = record_for(m.away_team)

        home.played += 1
        away.played += 1
        home.goals_for += m.home_goals
        home.goals_against += m.away_goals
        away.goals_for += m.away_goals
        away.goals_against += m.home_goals

        if m.home_goals > m.away_goals:
            home.won += 1
            away.lost += 1
        elif m.away_goals > m.home_goals:
            away.won += 1
            home.lost += 1
        else:
            home.drawn += 1
            away.drawn += 1

    return records


def build_table(matches: Sequence[MatchResult], rules: RuleSet) -> list[TableRow]:
    """Apply `rules` to `matches` and return table rows ordered 1st to last.

    Ranking order: points (desc), then each of `rules.tie_breakers` in turn
    (desc), then team name (asc) as a final, deterministic tie-break so the
    output order never depends on input/dict ordering. Real 1974/75 football
    did sometimes leave ties genuinely unresolved in the printed table; this
    program always produces one definite order, and the alphabetical
    fallback is a documented implementation choice, not a historical rule.
    """
    records = build_records(matches)

    def sort_key(record: TeamRecord):
        points = rules.points_for(won=record.won, drawn=record.drawn, lost=record.lost)
        tie_break_values = tuple(key(record) for key in rules.tie_breakers)
        # Negate everything so a plain ascending sort gives best-first order.
        return (-points, *(-v for v in tie_break_values), record.team)

    ordered = sorted(records.values(), key=sort_key)

    rows = []
    for position, record in enumerate(ordered, start=1):
        points = rules.points_for(won=record.won, drawn=record.drawn, lost=record.lost)
        rows.append(
            TableRow(
                position=position,
                team=record.team,
                played=record.played,
                won=record.won,
                drawn=record.drawn,
                lost=record.lost,
                goals_for=record.goals_for,
                goals_against=record.goals_against,
                points=points,
                goal_average=record.goal_average,
                goal_difference=record.goal_difference,
            )
        )
    return rows


def format_goal_average(value: float) -> str:
    if value == float("inf"):
        return "inf"
    return f"{value:.3f}"


def write_table(rows: Sequence[TableRow], destination: TextIO) -> None:
    """Write table rows to `destination` as CSV in the conventional format."""
    # Use newline="" to prevent extra blank lines on Windows
    # This is the recommended approach for csv.writer
    writer = csv.writer(destination, lineterminator='\n')
    writer.writerow(OUTPUT_COLUMNS)
    for row in rows:
        writer.writerow(
            [
                row.position,
                row.team,
                row.played,
                row.won,
                row.drawn,
                row.lost,
                row.goals_for,
                row.goals_against,
                format_goal_average(row.goal_average),
                row.points,
            ]
        )
