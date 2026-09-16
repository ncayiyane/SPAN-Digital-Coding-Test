import pytest

from league_table.models import MatchResult, TeamRecord


def test_match_result_winner_home():
    m = MatchResult("2024-01-01", "Derby County", 2, "Everton", 1)
    assert m.winner == "Derby County"


def test_match_result_winner_away():
    m = MatchResult("2024-01-01", "Derby County", 0, "Everton", 1)
    assert m.winner == "Everton"


def test_match_result_draw_has_no_winner():
    m = MatchResult("2024-01-01", "Derby County", 1, "Everton", 1)
    assert m.winner is None


def test_negative_goals_rejected():
    with pytest.raises(ValueError):
        MatchResult("2024-01-01", "Derby County", -1, "Everton", 1)


def test_blank_team_name_rejected():
    with pytest.raises(ValueError):
        MatchResult("2024-01-01", "", 1, "Everton", 1)


def test_team_cannot_play_itself():
    with pytest.raises(ValueError):
        MatchResult("2024-01-01", "Derby County", 1, "Derby County", 1)


def test_goal_average_normal_case():
    r = TeamRecord(team="Ipswich Town", goals_for=18, goals_against=6)
    assert r.goal_average == pytest.approx(3.0)


def test_goal_average_zero_conceded_and_zero_scored_is_zero():
    r = TeamRecord(team="No Goals FC", goals_for=0, goals_against=0)
    assert r.goal_average == 0.0


def test_goal_average_zero_conceded_with_goals_scored_is_infinite():
    r = TeamRecord(team="Watertight FC", goals_for=5, goals_against=0)
    assert r.goal_average == float("inf")


def test_goal_difference():
    r = TeamRecord(team="Derby County", goals_for=10, goals_against=7)
    assert r.goal_difference == 3
