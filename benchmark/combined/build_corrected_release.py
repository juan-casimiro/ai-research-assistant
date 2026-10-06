"""Freeze the corrected five-topic selection without altering historical v1."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchmark_scoring import canonical_hash, validate_benchmark
from benchmark.combined.build_release import load, write

TOPICS = ("cardiology", "diabetes", "oncology", "outliers", "als-ftd")


def build(destination):
    articles, origins, snapshots = {}, {}, {}
    for topic in TOPICS:
        release = ROOT / "benchmark" / topic / "v1"
        benchmark = load(release / "queries.json")
        manifest = load(release / "manifest.json")
        validate_benchmark(benchmark)
        if benchmark["selection_sha256"] != manifest["fingerprint_sha256"]:
            raise ValueError(f"{topic}: selection/query linkage changed")
        snapshots[topic] = benchmark
        origins[topic] = {"queries": str((release / "queries.json").relative_to(ROOT)),
                         "query_sha256": canonical_hash(benchmark),
                         "manifest": str((release / "manifest.json").relative_to(ROOT)),
                         "manifest_sha256": canonical_hash(manifest)}
        for article in manifest["articles"]:
            aid = article["article_id"]
            identity = lambda a: (a["filename"], a["pmc_version"],
                a["download"]["pdf_sha256"], a["validation"]["extracted_text_sha256"])
            if aid in articles and identity(articles[aid]) != identity(article):
                raise ValueError(f"conflicting shared article: {aid}")
            articles.setdefault(aid, article)
    ordered = [articles[aid] for aid in sorted(articles)]
    if len(ordered) != 55 or len({a["filename"] for a in ordered}) != 55:
        raise ValueError("expected exactly 55 unique articles/filenames")
    all_ids = [q["id"] for b in snapshots.values() for q in b["queries"]]
    if len(all_ids) != 158 or len(set(all_ids)) != 158:
        raise ValueError("expected exactly 158 unique query IDs")
    manifest = {"schema_version": "1.0", "corpus_version": "combined-selection-v2",
                "status": "corrected-gold evaluation snapshot; model-reviewed, not expert-certified",
                "source_releases": origins, "articles": ordered}
    manifest["fingerprint_sha256"] = canonical_hash(manifest)
    # One shared inventory; topic-local relative links keep read_release's
    # existing interface without committing five identical 55-article copies.
    write(destination / "manifest.json", manifest)
    tuples = [{"article_id": a["article_id"], "pmc_version": a["pmc_version"],
               "pdf_sha256": a["download"]["pdf_sha256"],
               "text_sha256": a["validation"]["extracted_text_sha256"]} for a in ordered]
    dependencies = {"schema_version": "1.0", "selection_sha256": manifest["fingerprint_sha256"],
                    "source_releases": origins, "cases": [],
                    "scope_rationale": "All 158 IDs: corpus expansion and final whole-benchmark claims. All earlier nested conditions use the same current gold/scorer. No configuration sweep."}
    for topic, original in snapshots.items():
        benchmark = {"schema_version": original["schema_version"],
                     "query_version": original["query_version"] + "-combined-envelope-v2",
                     "status": manifest["status"], "selection_sha256": manifest["fingerprint_sha256"],
                     "parent": origins[topic], "queries": original["queries"], "anchors": original["anchors"]}
        validate_benchmark(benchmark)
        parent = load(ROOT / "benchmark" / topic / "v1/conditions.json")
        members = {name: sorted(value["article_ids"]) for name, value in parent["conditions"].items()
                   if name in ("C1", "C2")}
        members["C3"] = sorted(articles)
        conditions = {"schema_version": "1.0", "corpus_version": manifest["corpus_version"],
                      "query_version": benchmark["query_version"], "query_sha256": canonical_hash(benchmark),
                      "article_tuples": tuples, "conditions": {}}
        for name, ids in members.items():
            if len(set(ids)) != len(ids) or not set(ids) <= articles.keys():
                raise ValueError(f"invalid members for {topic}/{name}")
            conditions["conditions"][name] = {"article_ids": ids,
                "membership_sha256": canonical_hash([t for t in tuples if t["article_id"] in ids])}
        anchors = {a["id"]: a for a in benchmark["anchors"]}
        for query in benchmark["queries"]:
            used = {aid for e in query["evidence_sets"] for aid in e["anchors"]}
            accepted = sorted({anchors[aid]["article_id"] for aid in used})
            dependencies["cases"].append({"topic": topic, "query_id": query["id"],
                "revision": query["revision"], "category": query["category"],
                "case_sha256": canonical_hash(query), "query_sha256": canonical_hash(benchmark),
                "accepted_articles": accepted, "evidence_sets": query["evidence_sets"],
                "related_distractors": query["related_distractors"],
                "negative_evidence_scope": query["answerability"],
                "overlap_review_articles": sorted(set(articles) - set(accepted))})
        for name, value in [("queries.json", benchmark), ("conditions.json", conditions)]:
            write(destination / topic / name, value)
        local_manifest = destination / topic / "manifest.json"
        if local_manifest.is_symlink():
            if local_manifest.readlink() != Path("../manifest.json"):
                raise ValueError("unexpected topic manifest link")
        elif local_manifest.exists():
            if load(local_manifest) != manifest:
                raise ValueError("refusing to replace changed topic manifest")
            local_manifest.unlink()
        if not local_manifest.is_symlink():
            local_manifest.symlink_to("../manifest.json")
    dependencies["fingerprint_sha256"] = canonical_hash(dependencies)
    write(destination / "case_dependencies.json", dependencies)
    print("Built 55 unique articles / 158 unchanged current-gold queries in five envelopes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    build(parser.parse_args().output)
