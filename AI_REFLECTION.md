# AI Reflection

## How I used AI

I used AI throughout this coding assessment as a development assistant. I used it to help me understand the requirements, think through the software design, work with CSV data, develop parts of the solution, create and review tests, and improve the documentation.

I did not treat the AI output as automatically correct. I reviewed the code and information it provided, ran the application and tests, and made decisions about what to accept, change, or reject.

AI was particularly useful when I was thinking about how to structure the application. We discussed separating the data models, football rules, league-table calculations, and CLI functionality instead of putting everything into one file. I reviewed that approach and used the parts that made sense for the assessment.

## A situation where I caught an AI-generated problem

The most important example of reviewing AI output happened when I was working with the historical football data.

AI-generated documentation stated that the week-10 cutoff date of 28 September 1974 had been established through a specific programmatic verification process. It also described other checks that supposedly took place.

When I reviewed this more carefully, I realised that the described verification had not actually happened. The explanation sounded convincing, but the evidence and code did not support what the documentation claimed.

I questioned the claim instead of leaving it in the repository. I checked what had actually been done and found that the date had been asserted without the verification process described in the documentation.

I then required the cutoff date to be properly checked against the historical match data. A verification script was used to examine candidate dates and count the matches played by each club. The check confirmed 28 September 1974 as the appropriate cutoff: 16 clubs had played 10 matches and 6 clubs had played 9 matches.

This was an important lesson for me because the final date was correct, but the original explanation of how it had been established was not. It showed me that an AI response can be detailed and confident while still describing work that was never actually performed.

## How I reviewed the code

I reviewed the generated code against the actual requirements of the assessment rather than assuming that code produced by AI was correct.

I ran the application and tests, checked the league calculations, considered invalid-input and edge cases, and reviewed whether the implementation followed the historical football rules.

The historical rules were particularly important. The 1974/75 season used 2 points for a win and goal average as the relevant tie-break, rather than simply applying modern football rules. I therefore checked that these rules were represented correctly in the implementation.

I also reviewed the tests and documentation. I did not consider the project complete simply because AI had generated tests or documentation for it.

## What I learned

This assessment taught me more about historical football rules, CSV processing, data validation, software design, testing, and technical documentation.

I learned that historical requirements need to be checked carefully because assumptions based on current rules can lead to an incorrect implementation.

I also learned more about separating responsibilities in a software project. Keeping the data models, rules, calculations, and CLI responsibilities separate made the project easier to understand and test.

The biggest lesson for me was about using AI responsibly. AI can speed up development and help with problem-solving, but its output still needs to be reviewed.

The cutoff-date issue showed me that this applies to documentation and factual claims just as much as it applies to source code. A document can sound professional and contain specific details while still being inaccurate.

## What I would do differently next time

If I completed another coding assessment where AI was allowed, I would review every AI-generated document before putting it into the repository.

I would specifically check claims about:

* work that was supposedly performed
* sources that were supposedly checked
* tests that were supposedly run
* verification steps that were supposedly completed

I would also keep a clearer record of my own decisions during development. That would make it easier to ensure that the final documentation reflects what actually happened rather than relying on an AI-generated summary.

My main takeaway is that AI is a development tool, not an authority. I am responsible for reviewing its suggestions, testing the resulting code, verifying factual claims, and making sure that the final repository represents my own work and decisions.
