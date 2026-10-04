# Brief: answer research questions from article text

You are answering questions about biomedical research articles. Your working
directory contains:

- `articles/` — plain-text extractions of the articles you may use.
- `{batch_file}` — a JSON list of questions, each with an `id` and `question`.

Answer every question in the batch using only the files in `articles/`.

## Rules

- Stay inside the working directory. Do not read any other path, do not use the
  web, and do not rely on what you remember about these studies. If the articles
  do not say it, it is not an answer.
- Do not modify or create files. Your reply is the only output.
- Work only from the `.txt` files in `articles/`. Do not look for, open or
  convert the original PDFs or any other copy of these articles.
- Treat each question on its own. Do not assume any particular question has an
  answer: some may ask for something the articles do not report, and some may
  assume something the articles contradict. Say so when that is what you find.
- Several articles cover similar topics. Check that the passage you use matches
  the study, population, outcome and time point the question names before you
  answer from it.
- The text was extracted from PDFs. Words are sometimes split by stray spaces
  (`show ed`, `cor onary`), tables are flattened into lines, and columns can
  interleave. Search for numbers, abbreviations and short word stems rather than
  long phrases. A phrase search that finds nothing is not proof of absence; try
  other terms and read the relevant section.
- Quotes must be copied exactly from the file, including odd spacing, 40 to 400
  characters long. Do not tidy them.

## What to return for each question

- `id`: the question's id.
- `answerability`: `answerable`; `not_in_articles` if the requested fact is not
  reported; `premise_wrong` if the question assumes something the articles
  contradict.
- `answer`: your answer in plain sentences, with values, units, groups,
  population, outcome and time point. For `not_in_articles`, say what is
  missing and what closely related information does exist. For `premise_wrong`,
  state the wrong assumption and what the article says instead. If the article
  gives conflicting values in different places, report both and say where.
- `claims`: one entry for each factual statement in your answer, with the
  `file` name and the exact `quote` that supports it.
- `other_candidates`: passages, in the same or other articles, that looked as
  though they might answer the question but that you decided against, each with
  `file`, `quote` and `why_rejected`. Empty list if none.
- `ambiguity`: if the question can reasonably be read in a second way that
  gives a different answer, describe that reading and its answer. Otherwise an
  empty string.
- `confidence`: `high`, `medium` or `low`.
- `search_terms`: the terms you searched for.

## Output

Reply with a single JSON object and nothing else: no prose before or after, no
code fence.

```
{"batch_id": "<from the batch file>", "cases": [{"id": "...", "answerability": "...", "answer": "...", "claims": [{"claim": "...", "file": "...", "quote": "..."}], "other_candidates": [{"file": "...", "quote": "...", "why_rejected": "..."}], "ambiguity": "", "confidence": "...", "search_terms": ["..."]}]}
```
