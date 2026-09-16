"""Scoring and tie-break rules for building a league table.

League standing rules are not universal across time or competition, so
rather than hard-coding "3 points for a win, sort by goal difference" (the
rule since 1981/82), this module makes the rules an explicit, swappable
value. The default here (`FIRST_DIVISION_1974_75`) matches what the
Football League actually used that season:

  * 2 points for a win, 1 for a draw, 0 for a loss.
    ("Three points for a win" was not adopted in England until 1981/82.)
  * Ties broken by goal average (goals scored / goals conceded), not goal
    difference. Goal difference was not adopted until 1976/77, and it can
    genuinely disagree with goal average -- e.g. a team on 30 for/27 against
    (average 1.111) outranks one on 40 for/37 against (average 1.081) despite
    both having a goal difference of +3.

Sources: the 1974-75 Football League First Division was classified by
"1) Points; 2) Goal average; 3) Goals scored" (per contemporary Football
League tables reproduced on Wikipedia club-season pages for that season).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .models import TeamRecord

# A tie-break key extracts a sortable value from a TeamRecord. Higher is
# always better -- callers that want an ascending sort must negate.
TieBreakKey = Callable[[TeamRecord], float]

GOAL_AVERAGE: TieBreakKey = lambda r: r.goal_average
GOAL_DIFFERENCE: TieBreakKey = lambda r: r.goal_difference
GOALS_FOR: TieBreakKey = lambda r: r.goals_for
WINS: TieBreakKey = lambda r: r.won


@dataclass(frozen=True)
class RuleSet:
    """A named, complete set of rules for turning results into a table."""

    name: str
    points_win: int
    points_draw: int
    points_loss: int
    # Applied in order, most significant first, after points.
    tie_breakers: tuple[TieBreakKey, ...] = field(default_factory=tuple)

    def points_for(self, *, won: int, drawn: int, lost: int) -> int:
        return won * self.points_win + drawn * self.points_draw + lost * self.points_loss


# The rules actually in force for the season named in this exercise.
FIRST_DIVISION_1974_75 = RuleSet(
    name="First Division 1974/75",
    points_win=2,
    points_draw=1,
    points_loss=0,
    tie_breakers=(GOAL_AVERAGE, GOALS_FOR),
)

# Provided for comparison/testing -- the rules used in England today.
MODERN_ENGLISH_LEAGUE = RuleSet(
    name="modern English league",
    points_win=3,
    points_draw=1,
    points_loss=0,
    tie_breakers=(GOAL_DIFFERENCE, GOALS_FOR),
)

RULESETS_BY_NAME: dict[str, RuleSet] = {
    "1974-75": FIRST_DIVISION_1974_75,
    "modern": MODERN_ENGLISH_LEAGUE,
}
