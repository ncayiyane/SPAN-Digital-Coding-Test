# Football League Standings

A command-line tool that calculates a football (soccer) league standings
table from a CSV file of match results, and uses it to reproduce the
English First Division table after week 10 of the 1974/75 season.

## Requirements

- Python 3.10+ (uses `X | Y` type hints and `match`-free but modern syntax)
- No third-party runtime dependencies — the tool itself only uses the
  standard library (`csv`, `argparse`, `dataclasses`).
- `pytest` for running the test suite (dev-only, not required to run the
  tool itself).

## Setup

```bash
# from the project root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt   # only needed to run the tests
```

## Running it

The tool reads match results as CSV and writes a standings table as CSV.
It supports both file arguments and stdin/stdout, per the exercise brief.

```bash
# Named files:
python3 -m league_table.cli --input data/matches.csv --output table.csv

# stdin / stdout:
python3 -m league_table.cli < data/matches.csv > table.csv

# Piped:
cat data/matches.csv | python3 -m league_table.cli
```

### Input format

A CSV with a header row and (at least) these five columns, in any order:

```
date,home_team,home_goals,away_team,away_goals
1974-08-17,Everton,0,Derby County,0
1974-08-17,Stoke City,3,Leeds United,0
```

### Output format

A CSV standings table, ranked best (row 1) to worst:

```
position,team,played,won,drawn,lost,goals_for,goals_against,goal_average,points
1,Ipswich Town,10,8,0,2,18,6,3.000,16
...
```

### Rules

By default the tool applies the rules **actually used by the English First
Division in 1974/75**, not modern English football rules — the two
genuinely disagree, and getting this right was the point of the exercise:

| | 1974/75 (default, `--rules 1974-75`) | Modern (`--rules modern`) |
|---|---|---|
| Win | 2 points | 3 points |
| Draw | 1 point | 1 point |
| Loss | 0 points | 0 points |
| Tie-break | Goal **average** (F ÷ A), then goals scored | Goal **difference** (F − A), then goals scored |

Goal difference wasn't adopted by the Football League until 1976/77, and
three points for a win not until 1981/82 — using either for the 1974/75
table would be an anachronism. See `league_table/rules.py` for the rationale
and a worked example of goal average and goal difference disagreeing on
who ranks higher.

`--rules` lets you compare both on the same data; `--rules modern` is
provided for that comparison, not because it's the "right" answer for
1974/75.

## Reproducing the week-10 1974/75 table

```bash
python3 -m league_table.cli \
  --input data/england-1974-75-division1-week10.csv \
  --output data/england-1974-75-division1-week10-STANDINGS.csv
```

`data/england-1974-75-division1-week10.csv` is the actual set of First
Division results played up to and including Saturday 28 September 1974 —
see `data/SOURCE.md` for where that data came from and why that date is
"week 10". It's 107 matches; at that point 16 of the 22 clubs had played
10 games and 6 clubs had a game in hand on 9 — English fixture lists of
this era were not perfectly synchronised across clubs, which the tool
handles the same way a real table does (it just tallies whatever each
club actually played).

## Running the tests

```bash
pytest
```

The suite covers: points/tie-break rule math, CSV parsing and its error
cases, the ranking algorithm (including a test that goal average and goal
difference can produce *opposite* orderings for two teams with identical
points and goal difference), the CLI end-to-end via subprocess, and a
regression test that runs the real week-10 data through the CLI and checks
it reproduces the historically correct result (Ipswich Town top, and the
9-games/10-games split described above).

## Project layout

```
league_table/
  models.py   # MatchResult, TeamRecord, TableRow dataclasses
  rules.py    # RuleSet: points + tie-break configuration (1974/75 & modern)
  table.py    # CSV I/O + the ranking algorithm
  cli.py      # argparse entry point
tests/        # pytest suite (unit + CLI integration + historical regression)
data/         # the actual 1974/75 week-10 input, its output, and SOURCE.md
```

## AI collaboration artifacts

As required by the exercise, this repository also includes `CLAUDE.md`
(project instructions given to the AI assistant) and `AI_REFLECTION.md`
(a reflection on the collaboration). See those files, and their headers,
for a note on the `.claude/` and `ai/` folders.
