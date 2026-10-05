# Brief: compare independent answers with benchmark answer keys

For each case in `{batch_file}` you are given a benchmark question, its answer
key (`required_facts`, `reference_answer`, `answerability`, `source_files`),
and a `blind_answer` written by a separate model that saw only the question and
the articles. Each claim in the blind answer carries `quote_verified`: whether
its quote was found in the file it names.

Read the batch file, then decide from its contents alone where the two agree.
You have no access to the articles and should not judge which side is right; a
later reviewer does that. Do not create files.

## For each case

- `answerability_agrees`: the blind `answerability` corresponds to the key's
  status: `answerable` with `answerable`, `premise_wrong` with `false_premise`.
  For an `absent_fact` key, both `not_in_articles` and `premise_wrong` agree,
  provided the blind answer does not go on to supply the requested fact: saying
  a trial never measured an outcome is the same non-answer either way.
- `facts`: for each required fact:
  - `match` — the blind answer states the same values with the same group,
    population, endpoint and timeframe. Rounding within the fact's stated
    tolerance is a match.
  - `partial` — some of the fact's values or qualifiers are present and none
    contradict it.
  - `mismatch` — the blind answer gives a different value, group, direction or
    scope for the same thing.
  - `not_addressed` — the blind answer does not speak to this fact.

  Add a short `note` naming the differing value for anything other than `match`.
- `different_source`: the blind answer rests a required fact on a verified
  quote from a file that is not in the key's `source_files`. Always `false`
  when the key has no source files. Extra context quoted from other files does
  not count if the fact itself is also supported from a source file.
- `blind_reported_ambiguity`: the blind answer's `ambiguity` field is not empty.
- `ambiguity_changes_answer`: the second reading the blind answer describes
  would give an answer that differs from the key's required facts. `false` if
  there is no reported ambiguity, or if both readings lead to the key's answer.
- `escalate`: `true` if `answerability_agrees` is false, any fact is
  `mismatch`, `different_source` is true, or `ambiguity_changes_answer` is
  true. Also `true` if more than half the facts are `not_addressed` while the
  blind confidence is `high`.
- `reasons`: one short line for each trigger. Empty list if not escalated.

Ignore blind claims whose quote is not verified when deciding `match`, and
mention them in the note.

## Output

Reply with a single JSON object matching the provided schema and nothing else.
