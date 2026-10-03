"""Build immutable comparison envelopes from reviewed topic release snapshots.

No gold, source bytes, or historical run is edited. Corpus paths are supplied
separately to the existing production-path ingestion/evaluation tools.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchmark_scoring import canonical_hash, validate_benchmark

TOPICS = ("cardiology", "diabetes", "oncology", "outliers")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") != text:
        raise ValueError(f"refusing to change frozen envelope: {path}")
    path.write_text(text, encoding="utf-8")


def build(destination):
    articles, snapshots, origins = {}, {}, {}
    for topic in TOPICS:
        release = ROOT / "benchmark" / topic / "v1"
        # This is the final evaluated diabetes snapshot, before descriptive
        # annotations were corrected. Its questions/anchors remain unchanged.
        query_path = (release / "runs/evaluated-release/queries.json"
                      if topic == "diabetes" else release / "queries.json")
        snapshots[topic] = load(query_path)
        origins[topic] = {"queries": str(query_path.relative_to(ROOT)),
                          "query_sha256": canonical_hash(snapshots[topic]),
                          "manifest": str((release / "manifest.json").relative_to(ROOT))}
        manifest = load(release / "manifest.json")
        origins[topic]["manifest_sha256"] = canonical_hash(manifest)
        for article in manifest["articles"]:
            aid = article["article_id"]
            previous = articles.get(aid)
            if previous is not None:
                identity = lambda a: (a["filename"], a["pmc_version"],
                    a["download"]["pdf_sha256"], a["validation"]["extracted_text_sha256"])
                if identity(previous) != identity(article):
                    raise ValueError(f"conflicting shared article: {aid}")
            else:
                articles[aid] = article
    ordered = [articles[aid] for aid in sorted(articles)]
    if len({a["filename"] for a in ordered}) != len(ordered):
        raise ValueError("article filenames are not unique")
    manifest = {"schema_version": "1.0", "corpus_version": "combined-selection-v1",
                "status": "derived union; original article records preserved",
                "source_releases": origins, "articles": ordered}
    manifest["fingerprint_sha256"] = canonical_hash(manifest)
    tuples = [{"article_id": a["article_id"], "pmc_version": a["pmc_version"],
               "pdf_sha256": a["download"]["pdf_sha256"],
               "text_sha256": a["validation"]["extracted_text_sha256"]} for a in ordered]
    for topic in TOPICS:
        original = snapshots[topic]
        # Preserve the complete evaluated query objects and all original anchors.
        benchmark = {"schema_version": original["schema_version"],
                     "query_version": original["query_version"] + "-combined-envelope-v1",
                     "status": "frozen comparison envelope; original gold unchanged",
                     "selection_sha256": manifest["fingerprint_sha256"],
                     "parent": origins[topic],
                     "queries": original["queries"], "anchors": original["anchors"]}
        validate_benchmark(benchmark)
        parent_conditions = load(ROOT / "benchmark" / topic / "v1/conditions.json")
        membership = {name: value["article_ids"]
                      for name, value in parent_conditions["conditions"].items()
                      if name in ("C1", "C2")}
        membership["C3"] = sorted(articles)
        conditions = {"schema_version": "1.0", "corpus_version": manifest["corpus_version"],
                      "query_version": benchmark["query_version"],
                      "query_sha256": canonical_hash(benchmark), "article_tuples": tuples,
                      "conditions": {name: {"article_ids": sorted(ids),
                          "membership_sha256": canonical_hash([t for t in tuples if t["article_id"] in ids])}
                          for name, ids in membership.items()}}
        for name, ids in membership.items():
            if not set(ids) <= articles.keys():
                raise ValueError(f"unknown members for {topic}/{name}")
        for name, value in [("manifest.json", manifest), ("queries.json", benchmark),
                            ("conditions.json", conditions)]:
            write(destination / topic / name, value)
    print(f"Built {len(articles)} unique articles and four topic comparison envelopes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.output)
