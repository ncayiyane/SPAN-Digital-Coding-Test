# Data source and methodology

## Match results

`england-1974-75-division1-week10.csv` was extracted from
[`jalapic/engsoccerdata`](https://github.com/jalapic/engsoccerdata)
(`data-raw/england.csv`), an open, citable dataset of English top-four-tier
football results back to 1888, released under CC-BY:

> James P. Curley (2016). *engsoccerdata: English Soccer Data 1871-2016.*
> R package.

Extraction command (see `tools/extract_week10.py` for the exact, reproducible
version):

```bash
curl -sL -o england.csv \
  https://raw.githubusercontent.com/jalapic/engsoccerdata/master/data-raw/england.csv
```

Filtered to `Season == 1974` and `division == "1"`, which yields all 462
First Division matches of the 1974/75 season — a figure that matches the
"Matches: 462" total for that season reported on Wikipedia.

## What "week 10" means

The First Division didn't play a perfectly synchronised set of fixtures
each week in this era (some clubs had midweek games rearranged, so on any
given Saturday different clubs had played different numbers of games).
So "the 10th week" is interpreted here as: all matches played up to and
including the last full Saturday round in which the majority of clubs
reached 10 games played — **Saturday 28 September 1974**.

At that cutoff:
- 16 clubs had played 10 games
- 6 clubs had played 9 games (a genuine game in hand, not missing data)

This is checked programmatically by `tools/verify_cutoff.py`, which tallies
games played per club after every distinct match date in the season and
prints the point where a 16/6 split first appears:

```bash
python3 tools/verify_cutoff.py
```

Run it yourself to reproduce the result — don't just take this file's word
for it. Sample output around the relevant date:

```
1974-09-25: {8: 6, 9: 16}
1974-09-28: {9: 6, 10: 16}  <-- 16 clubs on 10 games, 6 clubs on 9 games
1974-10-05: {10: 6, 11: 16}
```

**Note on an earlier version of this document:** a previous draft of this
file claimed the cutoff date had been cross-checked against two other
candidates' public repos for this same exercise. That claim was false —
no such repos were ever found or consulted, and the "programmatic
derivation" it described didn't correspond to any code that actually
existed at the time. `tools/verify_cutoff.py` above is the real,
reproducible evidence for this date; nothing here relies on, or was
checked against, any other candidate's work.

## Verifying the result is right

Ipswich Town finishing top of the table after 10 games is independently
checkable against the narrative of the (very close, four-way) 1974/75
title race described on Wikipedia's
[1974–75 Football League First Division](https://en.wikipedia.org/wiki/1974%E2%80%9375_Football_League_First_Division)
article — Ipswich were genuine title contenders that season and led at
various points. `tests/test_cli.py` encodes this as a regression test.
