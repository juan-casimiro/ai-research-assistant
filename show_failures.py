#!/usr/bin/env python3
"""Print every query that did not pass at n=3, with full context."""
import json
from pathlib import Path

RESULTS = Path("./eval_results.json")

data = json.loads(RESULTS.read_text())
for r in data["results"]:
    if r["n3"]["verdict"] != "pass":
        print(f"\n{'='*60}")
        print(f"FAIL @ n=3 | {r['id']} | {r['category']}")
        print(f"Q: {r['question']}")
        print(f"Expected: {r.get('expected_doc') or r.get('expected_docs')}")
        print(f"Distractor: {r.get('distractor_doc')}")
        print(f"Retrieved (n=3): {r['n3']['retrieved_sources']}")
        print(f"Retrieved (n=8): {r['n8']['retrieved_sources']}")