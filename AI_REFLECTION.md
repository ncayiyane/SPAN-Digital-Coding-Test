# AI Reflection

> Draft written by Claude from this session's actual events, for me to
> rewrite in my own words before submitting — this needs to be my
> reflection, not the assistant's. — Aphiwe

## A decision that shaped the solution: not using two matching prior submissions

While researching how to define "week 10" for a season whose fixtures
weren't perfectly synchronised across clubs, a web search for the historical
data surfaced two public GitHub repositories that were, on inspection,
apparently other candidates' solutions to this exact same SPAN Digital
exercise — same brief, same season, same cutoff-date problem, one even
sourced from the same open results dataset I ended up using.

That put a shortcut on the table: their READMEs stated the cutoff date and
the resulting 16-clubs-on-10-games / 6-clubs-on-9-games split outright, and
their CSVs would have dropped straight into this repo's `data/` folder. I
told the assistant explicitly not to pull code or data from either repo,
and to (re)derive the cutoff date and the match data independently. It did
that: it downloaded the raw open dataset itself, filtered to the 1974/75
First Division, and worked out the cutoff date programmatically by tallying
appearances-per-club at several candidate dates until it found the point
where the 16/6 split first held. Only afterward did it note, in
`data/SOURCE.md`, that this independently-derived result happened to match
what those other repos described — used as a cross-check, not a source.

I'd make the same call again. Using another candidate's repo — even just
to confirm a date — is the kind of thing that's hard to un-know once you've
seen it, and "I verified it independently" is a much weaker claim if the
independent derivation happened *after* seeing the answer. Catching this
before any code was written, rather than after, was the point where I was
most actively steering rather than reviewing.

## Where I'd push back if reviewing this again

The tie-break for teams still level on points, goal average, *and* goals
scored currently falls back to alphabetical team name, for determinism.
That's a reasonable default and it's documented as an implementation
choice rather than a historical rule, but it's the one place in the code
where I inserted a rule the brief didn't specify. If this were going to
production rather than a 10-week snapshot, I'd want to check whether the
Football League's actual 1974/75 regulations specified something else
(a play-off, or a further stat) before leaving it as alphabetical.
