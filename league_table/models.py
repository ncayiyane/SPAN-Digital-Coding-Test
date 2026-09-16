"""Core data structures for the league table calculator."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MatchResult:
    """A single played fixture between two teams.

    ``date`` is kept as the raw string from the input file (not parsed into a
    ``date`` object) because the calculator never needs to do date arithmetic
    with it -- it only needs to preserve and echo it back. Keeping it as a
    plain string also means the CLI tolerates whatever date format the input
    CSV happens to use.
    """

    date: str
    home_team: str
    home_goals: int
    away_team: str
    away_goals: int

    def __post_init__(self) -> None:
        if self.home_goals < 0 or self.away_goals < 0:
            raise ValueError(
                f"Goals cannot be negative: {self.home_team} {self.home_goals}-"
                f"{self.away_goals} {self.away_team}"
            )
        if not self.home_team.strip() or not self.away_team.strip():
            raise ValueError("Team names cannot be blank")
        if self.home_team == self.away_team:
            raise ValueError(f"A team cannot play itself: {self.home_team!r}")

    @property
    def winner(self) -> str | None:
        """Return the winning team's name, or None for a draw."""
        if self.home_goals > self.away_goals:
            return self.home_team
        if self.away_goals > self.home_goals:
            return self.away_team
        return None


@dataclass
class TeamRecord:
    """The accumulated record for one team, before points/ordering are applied."""

    team: str
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    @property
    def goal_average(self) -> float:
        """Goals scored divided by goals conceded.

        This is the tie-breaker the Football League actually used before
        goal difference was adopted in 1976/77 (see rules.py). A team that
        has conceded zero goals has an undefined ratio; by convention we
        treat that as infinitely good rather than raising, so a hypothetical
        "10 for, 0 against" record sorts above "10 for, 1 against" instead of
        crashing the program.
        """
        if self.goals_against == 0:
            return float("inf") if self.goals_for > 0 else 0.0
        return self.goals_for / self.goals_against


@dataclass
class TableRow:
    """One ranked row of the final standings output."""

    position: int
    team: str
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    points: int
    goal_average: float = field(default=0.0)
    goal_difference: int = field(default=0)
