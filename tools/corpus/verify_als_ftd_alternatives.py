"""Check each prepared ALS/FTD evidence alternative separately, offline.

Loads no retrieval models, opens no collection and makes no paid calls.
"""
import copy
import json
from pathlib import Path

from benchmark_scoring import canonical_hash
from eval_benchmark import read_release
from verify_benchmark_reachability import verify_reachability


def verify_alternatives(directory: Path, corpus: Path) -> dict:
    benchmark, _, _, _, _, texts = read_release(directory, corpus, "C2")
    from main import chunk_text

    count = 0
    for query in benchmark["queries"]:
        for evidence_set in query["evidence_sets"]:
            isolated = copy.deepcopy(benchmark)
            case = copy.deepcopy(query)
            case["evidence_sets"] = [evidence_set]
            isolated["queries"] = [case]
            verify_reachability(isolated, texts, chunk_text)
            count += 1
    return {"sets": count, "all_reachable_and_minimum_witnesses_pass": True,
            "query_sha256": canonical_hash(benchmark),
            "method": "Each accepted OR alternative checked separately with production chunker and scorer",
            "command": "python verify_als_ftd_alternatives.py"}


if __name__ == "__main__":
    print(json.dumps(verify_alternatives(Path("benchmark/als-ftd/v1"),
                                       Path("corpus/als-ftd-v1")), indent=2))
