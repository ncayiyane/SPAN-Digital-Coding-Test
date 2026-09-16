import io

import pytest

from league_table.models import MatchResult
from league_table.rules import FIRST_DIVISION_1974_75, MODERN_ENGLISH_LEAGUE
from league_table.table import (
    build_records,
    build_table,
    read_matches,
    write_table,
)


def test_build_records_counts_wins_draws_losses_and_goals():
    matches = [
        MatchResult("d1", "A", 2, "B", 1),
        MatchResult("d2", "A", 0, "B", 0),
        MatchResult("d3", "B", 3, "A", 3),
    ]
    records = build_records(matches)

    assert records["A"].played == 3
    assert records["A"].won == 1
    assert records["A"].drawn == 2
    assert records["A"].lost == 0
    assert records["A"].goals_for == 5
    assert records["A"].goals_against == 4

    assert records["B"].played == 3
    assert records["B"].won == 0
    assert records["B"].drawn == 2
    assert records["B"].lost == 1


def test_build_table_orders_by_points_descending():
    matches = [
        MatchResult("d1", "A", 3, "B", 0),  # A win
        MatchResult("d2", "C", 1, "D", 1),  # draw
    ]
    rows = build_table(matches, FIRST_DIVISION_1974_75)
    points_by_team = {r.team: r.points for r in rows}
    assert points_by_team["A"] == 2
    assert points_by_team["B"] == 0
    assert points_by_team["C"] == 1
    assert points_by_team["D"] == 1
    # A (2 pts) must rank above the three teams on fewer points.
    assert rows[0].team == "A"


def test_goal_average_and_goal_difference_can_disagree_on_ranking():
    """The central historical wrinkle this exercise is testing for.

    Team X: 3 wins, goals 6-3 (goal average 2.000, goal difference +3).
    Team Y: 3 wins, goals 9-6 (goal average 1.500, goal difference +3).

    Both finish on identical points and identical goal difference, but
    1974/75 First Division rules (goal average) and modern rules (goal
    difference, then goals scored) must rank them in opposite order.
    """
    matches = [
        MatchResult("d1", "X", 2, "P1", 1),
        MatchResult("d2", "X", 2, "P2", 1),
        MatchResult("d3", "X", 2, "P3", 1),
        MatchResult("d4", "Y", 3, "P4", 2),
        MatchResult("d5", "Y", 3, "P5", 2),
        MatchResult("d6", "Y", 3, "P6", 2),
    ]

    rows_1974 = build_table(matches, FIRST_DIVISION_1974_75)
    positions_1974 = {r.team: r.position for r in rows_1974}
    assert positions_1974["X"] < positions_1974["Y"], "goal average should favour X"

    rows_modern = build_table(matches, MODERN_ENGLISH_LEAGUE)
    positions_modern = {r.team: r.position for r in rows_modern}
    assert positions_modern["Y"] < positions_modern["X"], (
        "equal goal difference should fall through to goals scored, favouring Y"
    )


def test_ties_fall_back_to_team_name_for_determinism():
    matches = [
        MatchResult("d1", "Zeta", 1, "Opp1", 0),
        MatchResult("d2", "Alpha", 1, "Opp2", 0),
    ]
    rows = build_table(matches, FIRST_DIVISION_1974_75)
    zeta_row = next(r for r in rows if r.team == "Zeta")
    alpha_row = next(r for r in rows if r.team == "Alpha")
    # Identical points, goal average, and goals for -- alphabetical breaks the tie.
    assert alpha_row.position < zeta_row.position


def test_read_matches_parses_valid_csv():
    csv_text = (
        "date,home_team,home_goals,away_team,away_goals\n"
        "1974-08-17,Everton,0,Derby County,0\n"
        "1974-08-17,Stoke City,3,Leeds United,0\n"
    )
    matches = read_matches(io.StringIO(csv_text))
    assert len(matches) == 2
    assert matches[0].home_team == "Everton"
    assert matches[1].away_goals == 0


def test_read_matches_rejects_missing_column():
    csv_text = "date,home_team,home_goals,away_team\n1974-08-17,Everton,0,Derby County\n"
    with pytest.raises(ValueError, match="missing required column"):
        read_matches(io.StringIO(csv_text))


def test_read_matches_rejects_non_integer_goals():
    csv_text = (
        "date,home_team,home_goals,away_team,away_goals\n"
        "1974-08-17,Everton,many,Derby County,0\n"
    )
    with pytest.raises(ValueError, match="line 2"):
        read_matches(io.StringIO(csv_text))


def test_write_table_round_trips_through_csv():
    matches = [MatchResult("d1", "A", 2, "B", 1)]
    rows = build_table(matches, FIRST_DIVISION_1974_75)
    buf = io.StringIO()
    write_table(rows, buf)
    output = buf.getvalue()
    assert "position,team,played,won,drawn,lost,goals_for,goals_against,goal_average,points" in output
    assert "1,A,1,1,0,0,2,1,2.000,2" in output
