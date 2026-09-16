# Project instructions for AI assistants

## What this is

A CLI that calculates a football league standings table from CSV match
results, built for the SPAN Digital backend coding test. It's exercised
against the English First Division's actual results through week 10 of the
1974/75 season.

## Hard requirements (don't compromise on these)

- Language: Python 3.10+, standard library only for the runtime tool
  (`pytest` is fine as a dev/test dependency).
- Input and output are CSV, via stdin/stdout **or** `--input`/`--output`
  file paths.
- Use the **1974/75 rules**, not modern football rules, by default:
  2 points for a win (not 3), ties broken by goal average (not goal
  difference). This is the crux of the exercise — don't silently default
  to today's rules.
- Automated tests are mandatory and must actually run (`pytest`).
- The week-10 data must be real historical results, not invented, and its
  provenance must be documented (`data/SOURCE.md`).

## Design conventions to follow

- Rules (points-per-result, tie-break order) live in `rules.py` as a
  `RuleSet` value, not hard-coded into the ranking function — the exercise
  is explicitly about a season with non-default rules, so the ranking
  logic must not assume "current" football rules anywhere.
- Keep `models.py` (data), `table.py` (logic + CSV I/O), and `cli.py`
  (argument parsing) separated; don't fold argument parsing into the
  ranking logic or vice versa.
- Every public function gets at least one direct unit test; the CLI gets
  subprocess-level integration tests; the bundled real 1974/75 data gets a
  regression test that checks the actual historical result (Ipswich Town
  top after 10 games), not just "it runs without crashing."
- Prefer raising `ValueError` with a specific, actionable message over
  crashing on invalid input (bad CSV headers, non-numeric goals, negative
  goals, a team playing itself).

## Things to avoid

- Don't reach for third-party CSV/data libraries (pandas etc.) — this is a
  small, well-bounded problem and the standard library is enough; adding a
  dependency here would be over-engineering.
- Don't assume goal difference is "close enough" to goal average — they
  can and do disagree, and a test should demonstrate that on this exact
  codebase rather than just asserting it in a comment.
- Don't fabricate or guess historical match data — if a fact about the
  season is needed (the cutoff date for "week 10", the points/tie-break
  rules), look it up and cite the source in `data/SOURCE.md` or in a code
  comment.

## Running things

```bash
pytest                                                   # tests
python3 -m league_table.cli --input path --output path   # the tool itself
python3 tools/extract_week10.py                          # regenerate data/*.csv from source
```
