# Brief: find evidence elsewhere in the corpus that breaks a benchmark case

A retrieval benchmark has questions whose answer keys each name the articles
that answer them. The corpus has since grown to 55 articles across cardiology,
diabetes, oncology, ALS/FTD and several unrelated topics. Your job is to search
the rest of the corpus for anything that makes a case's answer key wrong or
incomplete. You are looking for counter-evidence. A case you cannot break is a
legitimate result, but only after a real search.

Your working directory contains:

- `articles/` — plain-text extractions of all 55 articles.
- `{batch_file}` — a JSON batch. Each case has the `question`, `category`,
  `required_facts`, `reference_answer`, `answerability`, `source_files` (the
  declared answer sources), and `decoys` (named wrong-answer competitors with
  the stated reason each does not apply).

## Rules

- Read only inside the working directory. No web and no outside knowledge.
- Work only from the `.txt` files in `articles/`. Do not look for, open or
  convert the original PDFs or any other copy of these articles.
- Do not modify or create files. Your reply is the only output.
- Do not report passages from a case's own `source_files`. Another reviewer
  audits those. Everything else, including the named decoys, is in scope.
- The text was extracted from PDFs: words are split by stray spaces, tables are
  flattened and columns can interleave. Search on numbers, abbreviations, drug
  and gene names, trial names and short stems, not long phrases.
- Topic overlap is real: diabetes articles discuss cardiovascular outcomes,
  oncology reviews discuss cardiovascular toxicity, cognition articles discuss
  vascular risk. Do not limit the search to the case's own topic.
- Similar wording is not enough. A finding must match the population, endpoint
  and timeframe the question asks about. State how it matches, and where it
  does not, say so and lower the `strength`.
- Quotes must be copied exactly from the file, 40 to 400 characters.

## What counts as a finding

| Type | Meaning |
| --- | --- |
| H1 | Undeclared alternative: another article fully answers the same scoped question. |
| H2 | Conflict: another article reports a different value for the same population, endpoint and timeframe. |
| H3 | Absence broken: for an `absent_fact` case, a passage that supplies the fact. |
| H4 | Premise true elsewhere: for a `false_premise` case, an article in which the premise holds for the study the question names. |
| H5 | Undeclared competitor: a passage that is not an answer but is more likely to be confused with the answer than the named decoys. Informational. |
| H6 | Decoy answers: a named decoy does in fact answer the question. |

For `absent_fact` cases there are no source files: search everything, and try
synonyms and related measures, not only the terms in the question.

## What to return for each case

- `id`.
- `findings`: each with `type`, `file`, exact `quote`, an `explanation` of how
  it matches or fails to match the question's scope, and `strength`:
  `definite` (same study or scope, clearly breaks the case), `probable`, or
  `weak`. Empty list if you found nothing.
- `search_terms`: every term you searched for. Required even with no findings.
- `files_examined`: files you opened and read beyond a search hit.
- `stable`: `true` if there is no H1, H2, H3, H4 or H6 finding of `probable`
  or `definite` strength.

## Output

Reply with a single JSON object matching the provided schema and nothing else.
