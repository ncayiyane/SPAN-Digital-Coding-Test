# AI-Assisted Development Summary

## 1. Project scope

This project was completed as part of the SPAN Digital backend coding
assessment.

The application calculates football league standings from CSV match results.
The required historical dataset is the English First Division after week 10
of the 1974/75 season.

I chose Python for the implementation. AI was used throughout the development
process to help understand the requirements, discuss design decisions,
develop code, create and review tests, and improve documentation.

I reviewed the suggestions and made the final decisions about what was
included in the project.

## 2. Historical football rules

Before implementing the league-ranking logic, I verified the rules that
applied during the 1974/75 season.

The application uses:

* 2 points for a win
* 1 point for a draw
* 0 points for a loss
* goal average as the relevant tie-break rather than modern goal difference

This was important because applying modern football rules without checking
the historical rules would produce an incorrect implementation for this
assessment.

## 3. Historical data and the cutoff-date correction

The project uses historical English football results from the
`jalapic/engsoccerdata` dataset. The 1974/75 First Division data was filtered
to produce the required week-10 dataset.

During development, an AI-generated explanation stated that the
28 September 1974 cutoff date had been established through a specific
programmatic verification process and that other candidates' public
repositories had also been checked.

When I reviewed that explanation, I discovered that the described process
had not actually happened. The date had been presented as if it had been
verified when the claimed verification work had not been performed.

I did not keep that claim simply because it sounded plausible. I required
the cutoff date to be checked against the actual historical match data.

A verification script was then created to examine candidate dates and count
the matches played by each club. The verification confirmed the selected
cutoff date of 28 September 1974: 16 clubs had played 10 matches and 6 clubs
had played 9 matches at that point.

The important lesson was not only that the final date was correct, but that
the original explanation of how the date had been established was not
correct. I learned that AI-generated descriptions of work must be checked
against the actual evidence and code.

## 4. Implementation

The application was organised into separate responsibilities for:

* data models
* football rules
* league-table calculations
* CSV processing
* command-line argument handling

The historical 1974/75 rules are represented separately from the ranking
logic so that the implementation does not silently assume modern football
rules.

The project also includes validation for invalid input and automated tests.

During development I encountered an issue with using `argparse.FileType`
together with the newline handling required for CSV output. I changed the
implementation to open the output file manually so that CSV output could be
handled correctly across platforms.

## 5. Testing

The project includes unit tests and command-line integration tests.

The tests cover normal league calculations as well as cases involving
historical goal-average rules and invalid input.

A regression test also runs the real week-10 dataset through the application
and checks the resulting historical table.

The final test run contained 26 passing tests.

## 6. What I learned

This assessment improved my understanding of:

* historical football rules and how they affect software requirements
* CSV processing and validation
* software design and separation of responsibilities
* automated testing
* using AI as a development assistant
* reviewing AI-generated code and factual information
* writing and reviewing technical documentation

The most important lesson was that AI output must be treated as something
to review rather than something to accept automatically.

## 7. AI review and ownership

I reviewed AI-generated code, documentation, and factual claims during the
development process.

The cutoff-date incident was particularly important because it showed me
that a detailed and confident explanation can still describe work that was
never actually performed.

For future assessments, I would review every AI-generated document before
putting it into the repository. I would specifically check claims about
sources, verification steps, tests, and work supposedly performed.

The final repository should reflect what I actually did, what I verified,
and the decisions I made rather than simply preserving AI-generated draft
content.
