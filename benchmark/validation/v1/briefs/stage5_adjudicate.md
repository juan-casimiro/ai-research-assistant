# Brief: adjudicate a disputed benchmark case

One benchmark case has been reviewed by several independent reviewers who do
not all agree with its answer key. Decide, from the article text, whether the
key stands.

Your working directory contains:

- `articles/` — plain-text extractions of all 55 corpus articles.
- `{case_file}` — the case: the full answer key with its anchors, and the
  reviewer records:
  - `stage0` — automated structural warnings.
  - `blind_answer` — an answer written from the question and articles alone.
  - `audit` — a checklist review of the key against its source articles.
  - `hunt` — a search of the rest of the corpus for counter-evidence, each
    finding tagged with the corpus condition (`C1`, `C2`, `C3`, `als_ftd_only`)
    in which that article first appears for this case.
  - `compare` — where the blind answer and the key differ.
  - `escalation_reasons` — why the case reached you.

## Rules

- Read only inside the working directory. No web and no outside knowledge of
  these studies. Do not modify or create files.
- Any reviewer can be wrong, and so can the key. Read every disputed passage
  yourself, with its surrounding section, before deciding. Do not count votes.
- A blind answer that failed to find the answer shows the question is hard, not
  that the key is wrong. A hunt finding with similar wording but a different
  population, endpoint or timeframe does not break the case.
- The text was extracted from PDFs: tables are flattened and columns can
  interleave. If the dispute turns on a table binding the text cannot settle,
  the verdict is `needs_pdf_check`; say exactly which page, table and cells
  need to be looked at.
- Quotes must be copied exactly from the file.

## What to return

- `id`.
- `verdict`: `valid`, `valid_minor`, `defect_gold`, `defect_anchor`,
  `defect_category`, `ambiguous_question`, `alternative_missing`,
  `absence_violated`, `premise_not_false`, `decoy_invalid` or
  `needs_pdf_check`. If several apply, give the most serious and cover the rest
  in `rationale`.
- `severity`: `blocking` if a system giving the correct answer would be scored
  wrong, or a wrong one scored right; `non_blocking` for other defects; `none`
  if valid.
- `condition_first_affected`: for a defect caused by evidence outside the
  case's own sources, the smallest condition containing that evidence.
  `none` if the defect is in the key itself or there is no defect.
- `gold_stands`: `true` if the key can be used for scoring unchanged.
- `evidence`: the passages your decision rests on, each with `file`, exact
  `quote` and the `point` it establishes.
- `rationale`: how you resolved each escalation reason.
- `proposed_correction`: what should change in the key, in words. Do not write
  replacement JSON. Empty string if nothing.
- `blind_answer_assessment` and `hunter_assessment`: one or two sentences each
  on whether that reviewer was right, and why.

## Output

Reply with a single JSON object matching the provided schema and nothing else.
