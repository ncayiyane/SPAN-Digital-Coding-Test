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

The source data was filtered to `Season == 1974` and `division == "1"`,
which yields all 462 First Division matches of the 1974/75 season.

## What "week 10" means

The First Division did not play a perfectly synchronised set of fixtures
each week in this era. Some clubs had midweek games or rearranged fixtures,
so on a given Saturday different clubs could have played different numbers
of games.

For this project, "week 10" is interpreted as all matches played up to and
including Saturday 28 September 1974.

At that cutoff:

* 16 clubs had played 10 games
* 6 clubs had played 9 games

This cutoff is checked programmatically by `tools/verify_cutoff.py`, which
tallies games played per club after each distinct match date in the season.

Run:

```bash
python3 tools/verify_cutoff.py
```

The verification identifies 28 September 1974 as the point where 16 clubs
had played 10 matches and 6 clubs had played 9:

```text
1974-09-25: {8: 6, 9: 16}
1974-09-28: {9: 6, 10: 16}
1974-10-05: {10: 6, 11: 16}
```

This provides a reproducible check of the cutoff date using the historical
match data rather than relying only on a manually selected date.

## Verifying the result

The generated week-10 standings can be reproduced using:

```bash
python3 -m league_table.cli \
  --input data/england-1974-75-division1-week10.csv \
  --output data/england-1974-75-division1-week10-STANDINGS.csv
```

The regression tests in `tests/test_cli.py` run the real week-10 dataset
through the application and verify the expected historical result, including
Ipswich Town finishing top after 10 games.

The project also includes tests covering the historical points system,
goal-average tie-breaking, CSV validation, ranking behaviour, and CLI
integration.
