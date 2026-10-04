# Brief: audit benchmark answer keys against the source articles

A retrieval benchmark has questions with reference answers ("gold") that were
written by another model and have not been independently reviewed. Your job is
to check whether each gold record is supported by the article text. Assume
nothing is correct until you have read the passage yourself. A confirmed defect
is as useful a result as a confirmed pass.

Your working directory contains:

- `articles/` — plain-text extractions of this topic's articles.
- `{batch_file}` — a JSON batch. Each case has the `question`, `category`,
  `required_facts`, `evidence_sets`, the `anchors` those sets use (file,
  character offsets, excerpt), the `reference_answer`, `answerability`, named
  `distractors`, source `dependencies`, and any `stage0_warnings` from an
  automated pre-check.

## Rules

- Read only inside the working directory. No web, no outside knowledge of these
  studies: the question is what this text supports.
- Do not modify or create files. Your reply is the only output.
- For every anchor, read at least 2,000 characters before and after it in the
  article, plus the methods or results section it belongs to. The excerpt alone
  does not show which group, arm, model or time point a number belongs to.
- The text was extracted from PDFs: words are split by stray spaces, tables are
  flattened and columns can interleave. Search on numbers and short stems. If a
  table's row and column binding cannot be settled from the text, do not guess:
  give `cannot_tell` and the verdict `needs_pdf_check`.
- Quotes must be copied exactly from the file.
- An automated check already confirmed each excerpt sits at its recorded
  offsets. Do not spend effort re-verifying that.

## Checks for every case

| Check | Question to answer |
| --- | --- |
| G1 | Is the question self-contained, with a single reasonable reading, and without giving away the requested answer? Identifying cues (study name, cohort size, table number) are allowed. |
| G2 | Is every value in each required fact (number, unit, group, interval, P value) present in the anchored text and bound to the right group, arm or row? |
| G3 | Do the stated population, endpoint, timeframe and adjusted or unadjusted status match the source context? |
| G4 | Does each anchor support the fact it is mapped to, rather than only mentioning the topic? |
| G5 | Does the reference answer avoid claims the text does not support? |
| G6 | If the article gives conflicting values in different places, does the gold expose the conflict rather than pick one silently? |
| G7 | Does the case fit its category (criteria below)? |

## Category checks

Report these as K1 to K4. Use `not_applicable` for any that do not exist for
the category.

| Category | K1 | K2 | K3 | K4 |
| --- | --- | --- | --- | --- |
| `direct_lookup` | One local passage or table is enough to answer. | | | |
| `multi_hop` | No single anchor answers on its own. | The anchors are in separate places in the article. | Every anchor is needed. | |
| `cross_doc_synthesis` | Each article contributes a fact the other lacks. | No single article can answer alone. | The comparison drawn in the reference is legitimate and its caveats are stated. | |
| `cross_doc_distractor` | The named decoy shares enough terms to be a tempting wrong source. | The stated reason it does not apply is correct. | The decoy does not in fact answer the question. | The question can be answered without the decoy. |
| `false_premise` | The premise is false according to the text. | The correction rests on positive evidence, not silence. | The premise is not partly true. | |
| `unanswerable` | The fact is absent from the articles that would be expected to hold it. | It cannot be derived by simple arithmetic from reported values. | The recorded search terms and scope are adequate. | |

If a case has more than one evidence set, add an `ALT` check: does each
alternative set fully answer the same population, endpoint and timeframe?

For `unanswerable` cases, search this topic's articles yourself. A separate
reviewer searches the wider corpus; you do not need to.

## What to return for each case

- `id`.
- `checks`: one entry for each of G1 to G7, K1 to K4 and, where relevant, ALT,
  with `result` (`pass`, `fail`, `cannot_tell`, `not_applicable`), a one or two
  sentence `reason`, and for any `fail` or `cannot_tell` the `file` and exact
  `quote` that shows the problem. Use empty strings for `file` and `quote`
  otherwise.
- `facts`: for each required fact, `supported` (`yes`, `partly`, `no`,
  `cannot_tell`) and a short `note`.
- `verdict`: one of
  - `valid` — supported as written.
  - `valid_minor` — wording or annotation issue that would not change scoring.
  - `defect_gold` — a required value, scope or reference claim is wrong.
  - `defect_anchor` — an anchor does not support its fact.
  - `defect_category` — the case does not meet its category's criterion.
  - `ambiguous_question` — more than one defensible answer, or the answer is leaked.
  - `alternative_missing` — a complete undeclared evidence set exists.
  - `absence_violated` — an unanswerable fact is present.
  - `premise_not_false` — the premise is true or partly true.
  - `decoy_invalid` — the decoy answers the question or is not a plausible competitor.
  - `needs_pdf_check` — the text cannot settle a table binding.

  If several apply, give the most serious and describe the others in `summary`.
- `severity`: `blocking` if a system giving the correct answer would be scored
  wrong, or a wrong one scored right; `non_blocking` for other defects; `none`
  for `valid`.
- `summary`: two to four sentences on what you found.
- `proposed_correction`: what should change, in words. Empty string if nothing.

## Output

Reply with a single JSON object matching the provided schema and nothing else.
