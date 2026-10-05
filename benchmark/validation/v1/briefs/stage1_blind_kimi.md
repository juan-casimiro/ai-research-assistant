# Brief: answer research questions from article text

You are answering questions about biomedical research articles. Your working
directory contains:

- `articles/` — plain-text extractions of the articles you may use.
- `{batch_file}` — a JSON list of questions, each with an `id` and `question`.

The batch holds one question. Answer it using only the files in `articles/`.

## Shared guidance (read first, once)

Your working directory is a throwaway review folder, not a repository, so any
relative path to the shared development guidance (`../development-config`, "the
checkout beside this repository") does not resolve from here. The guidance is at
this absolute path and nowhere else:

`/Users/agentdev/development/development-config`

Load it with exactly these four commands, once, before anything else:

```sh
git -C /Users/agentdev/development/development-config fetch origin main
git -C /Users/agentdev/development/development-config show origin/main:INDEX.md
git -C /Users/agentdev/development/development-config show origin/main:WORKING_AGREEMENT.md
git -C /Users/agentdev/development/development-config show origin/main:environments/lnm03924-agentdev-macos.md
```

This task is inspection only: no editing, commits, issue tracker, servers or
tests. None of the procedures in the working agreement's trigger table apply, so
do not read them, and do not open any other file in that checkout. If the fetch
fails, reply with the error text only and stop.

## How to read the articles

This session holds one question. A well-founded answer matters more than a
small context, so read as much as the question needs.

1. Find the article first. List `articles/` and search it by path, for example
   `grep -n -i "term" articles/*.txt | head -40` or Grep with
   `path: "articles"`. A search that returns nothing usually means the pattern
   or path was wrong, not that the text is absent; change the terms rather than
   repeating the same search.
2. Read the whole text of each article the question depends on, including its
   tables, whenever a search excerpt does not settle the answer on its own, and
   always before you say that something is not reported or that a premise is
   wrong. Large files are expected; read them in full rather than guessing.
3. Do not read articles that are plainly about something else. For a question
   that compares or could be confused between studies, read each candidate.
4. Do not read or list the same content twice, and do not print a file to
   stdout that you have already read.
5. Keep the reply compact: quotes near the 40-character minimum that still
   supports the claim, and at most three `other_candidates`.

## Rules

- Apart from the four guidance commands above, stay inside the working
  directory. Do not read any other path, do not use the web, and do not rely on what you remember about these studies. If the articles
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
