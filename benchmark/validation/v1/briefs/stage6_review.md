# Brief: second opinion on one reviewed benchmark case

A retrieval benchmark has questions with answer keys. A first reviewer checked
one case against the source articles and reached a verdict. Give an independent
second opinion on that verdict from the article text. Agreement and
disagreement are equally useful; say which, and show the passage that decides
it.

Your working directory contains:

- `articles/` — plain-text extractions of all 55 corpus articles.
- `{case_file}` — one case:
  - the answer key: `question`, `category`, `required_facts`, `evidence_sets`,
    `anchors`, `reference_answer`, `answerability`, `distractors`,
    `dependencies`;
  - `context` — the article text around each anchor, already extracted for you,
    with the file name and the line numbers it covers;
  - `first_review` — the first reviewer's `verdict`, `severity`, reasoning,
    evidence and `proposed_correction`, and `why_reviewed`.

## How to work

- Read the case file first. The `context` passages are usually enough to judge
  the facts; open an article only to check something they do not show, and then
  read the specific lines you need rather than the whole file.
- Work only from the `.txt` files in `articles/`. Do not look for, open or
  convert the original PDFs or any other copy of these articles. No web and no
  outside knowledge of these studies.
- Do not modify or create files. Your reply is the only output.
- Judge the answer key against the text, then judge the first reviewer. Do not
  defer to either: check each disputed value, group, population, endpoint and
  timeframe yourself.
- The text was extracted from PDFs: words are split by stray spaces, tables are
  flattened and columns can interleave. If a table binding cannot be settled
  from the text, say so and use `needs_pdf_check`.
- Quotes must be copied exactly from the file.

## Verdicts

`valid` (supported as written); `valid_minor` (wording or annotation issue that
would not change scoring); `defect_gold` (a required value, scope or reference
claim is wrong); `defect_anchor` (an anchor does not support its fact);
`defect_category` (the case does not meet its category: a multi-hop needs two
separated passages of one article, a synthesis needs two articles, a distractor
needs a tempting decoy that does not answer); `ambiguous_question` (more than
one defensible answer, or the answer is given away); `alternative_missing` (a
complete undeclared evidence set exists); `absence_violated` (a fact labelled
absent is present); `premise_not_false` (a premise labelled false is true or
partly true); `decoy_invalid`; `needs_pdf_check`.

Severity is `blocking` if a system giving the correct answer would be scored
wrong, or a wrong one scored right; `non_blocking` for other defects; `none`
if valid.

## What to return

- `id`.
- `agreement`: `agree` if you reach the same verdict and severity for the same
  reasons; `partly_agree` if you reach the same verdict but for different
  reasons, or differ only on severity or on the correction; `disagree` if your
  verdict differs.
- `own_verdict`, `own_severity`: your verdict on the answer key.
- `gold_stands`: `true` if the key can be used for scoring unchanged.
- `evidence`: the passages your decision rests on, each with `file`, exact
  `quote` and the `point` it establishes. Three or fewer is usually enough.
- `rationale`: what you checked and why you agree or disagree, in a few
  sentences.
- `correction_assessment`: whether the proposed correction is right, with any
  change you would make. Empty string if there is no proposed correction and
  none is needed.

## Output

Reply with a single JSON object matching the provided schema and nothing else.
