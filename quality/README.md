# Diagnostic quality checks

These are opt-in measurements, not build gates. The default test suite remains
`python -m unittest discover`. Optional pinned `coverage==7.16.0` and
`radon==6.0.1` live in `requirements-quality.txt`; runtime requirements and the
Docker image are untouched.

The committed `evidence/mutations.json` is the [JUA-80 audit](JUA-80-audit.md)'s
mutation-run snapshot. It is not automatically refreshed; record any rerun
explicitly if you regenerate it.

## Coverage and complexity hotspots

```sh
AUDIT_DIR="$(mktemp -d)"
python -m coverage run --data-file="$AUDIT_DIR/final.coverage" -m unittest discover
python -m coverage report --data-file="$AUDIT_DIR/final.coverage"
python -m coverage json --data-file="$AUDIT_DIR/final.coverage" -o "$AUDIT_DIR/final.json"
python quality/quality_hotspots.py "$AUDIT_DIR/final.json" > "$AUDIT_DIR/final-hotspots.json"
python -m radon cc main.py eval_golden.py eval_context_sufficient.py ingest_corpus.py compare_evals.py -s -a
```

`quality_hotspots.py` joins Radon cyclomatic complexity to `coverage.py`'s
executed/missing statement lines and reports a CRAP-style score
(`CC² × (1 − line coverage)³ + CC`) plus a structural decision-nesting count. It
covers `main.py`, `eval_golden.py`, `eval_context_sufficient.py`,
`ingest_corpus.py`, `compare_evals.py`, `reset_collection.py`, `debug_bm25.py`,
and `show_failures.py`. Tests, `.venv`, and `quality/` itself are excluded via
`.coveragerc`.

## Curated mutation analysis

```sh
python quality/verify_test_strength.py --output-dir "$AUDIT_DIR/mutations"
```

`verify_test_strength.py` copies production source and tests into an isolated
temporary directory per mutation, runs the target test green, applies one
hand-picked production change, requires the expected assertion failure,
restores the original bytes, and reruns green. It writes per-mutation logs and
a `mutations.json` summary to `--output-dir`; only the portable
`mutations.json` is committed, under `evidence/`. See the
[audit's mutation section](JUA-80-audit.md) for the full curated list and
results.
