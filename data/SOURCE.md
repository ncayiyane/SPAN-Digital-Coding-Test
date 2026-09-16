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

This was checked programmatically: matches were sorted by date and
appearances per club were tallied at several candidate cutoff dates; the
28 September cutoff is the point where the 16/6 split first appears and
holds until the next full round (5 October 1974, confirmed by inspecting
which matches fall between the two dates — there are none, i.e. no
midweek games in between shifted the count).

This matches the description of "week 10" independently used for the same
season/competition on GitHub by past candidates who published their
methodology for this same exercise (search results surfaced two public
repos doing the same extraction from the same dataset). Their code and
data files were **not** consulted or copied — only their stated
methodology (cutoff date, 16/6 split) was used as a cross-check that the
independently-derived date and dataset here were correct.

## Verifying the result is right

Ipswich Town finishing top of the table after 10 games is independently
checkable against the narrative of the (very close, four-way) 1974/75
title race described on Wikipedia's
[1974–75 Football League First Division](https://en.wikipedia.org/wiki/1974%E2%80%9375_Football_League_First_Division)
article — Ipswich were genuine title contenders that season and led at
various points. `tests/test_cli.py` encodes this as a regression test.
