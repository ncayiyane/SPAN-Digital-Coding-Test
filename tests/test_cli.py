import csv
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WEEK10_DATA = PROJECT_ROOT / "data" / "england-1974-75-division1-week10.csv"


def run_cli(args, input_text=None):
    return subprocess.run(
        [sys.executable, "-m", "league_table.cli", *args],
        input=input_text,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )


def test_cli_reads_stdin_and_writes_stdout():
    input_csv = (
        "date,home_team,home_goals,away_team,away_goals\n"
        "1974-08-17,Everton,0,Derby County,0\n"
        "1974-08-17,Stoke City,3,Leeds United,0\n"
    )
    result = run_cli([], input_text=input_csv)
    assert result.returncode == 0
    lines = result.stdout.strip().splitlines()
    assert lines[0].startswith("position,team")
    # Stoke City's win (2 pts) should outrank the two drawing teams (1 pt each).
    assert "Stoke City" in lines[1]


def test_cli_reports_error_on_bad_input():
    bad_csv = "date,home_team,home_goals,away_team\nfoo,bar,1,baz\n"
    result = run_cli([], input_text=bad_csv)
    assert result.returncode == 1
    assert "error:" in result.stderr


def test_cli_supports_named_input_and_output_files(tmp_path):
    input_path = tmp_path / "in.csv"
    output_path = tmp_path / "out.csv"
    input_path.write_text(
        "date,home_team,home_goals,away_team,away_goals\n"
        "1974-08-17,Everton,2,Derby County,1\n"
    )

    result = run_cli(["--input", str(input_path), "--output", str(output_path)])

    assert result.returncode == 0
    assert output_path.exists()
    rows = list(csv.DictReader(output_path.open()))
    assert rows[0]["team"] == "Everton"
    assert rows[0]["points"] == "2"


def test_week10_1974_75_first_division_standings_match_the_historical_record():
    """Regression test against the real data this exercise asks for.

    Ipswich Town were top of the First Division after 10 games in 1974/75
    (an independently checkable fact about that season's title race), and
    the fixture list of the era left six clubs with a game in hand -- i.e.
    16 clubs on 10 games played and 6 clubs on 9 -- rather than every club
    having played an identical number of matches.
    """
    assert WEEK10_DATA.exists(), "expected the bundled week-10 results CSV"

    result = run_cli(["--input", str(WEEK10_DATA)])
    assert result.returncode == 0

    rows = list(csv.DictReader(result.stdout.splitlines()))
    assert len(rows) == 22, "the First Division had 22 clubs in 1974/75"

    assert rows[0]["team"] == "Ipswich Town"
    assert rows[0]["position"] == "1"

    played_counts = sorted(int(r["played"]) for r in rows)
    assert played_counts.count(9) == 6
    assert played_counts.count(10) == 16
