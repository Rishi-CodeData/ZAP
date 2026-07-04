Common Credit Profile from Multiple Bureau Sources

The Scenario
A fintech company receives credit bureau reports on loan applicants from three different credit bureaus. Each bureau delivers data in its own format, with its own field names, scoring range, and quirks. The risk and product teams need a single, clean applicant profile they can query consistently - regardless of which bureau(s) the data came from.

Your task is to build the normalisation layer that produces this common profile.

What to submit
- Three synthetic bureau files in different formats (you define the formats - make them realistically different)
- A parser for each format
- A final unified applicant dataset - you define the schema, justify your choices
- A reconciliation summary: what came in, what matched, what was incomplete

A short section in the README explaining: your schema decisions, how you would extend this for a new bureau, and one thing you are not happy with in your own solution.
