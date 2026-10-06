"""Build a frozen existing-topic query sample over core and outlier corpora."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from benchmark_scoring import canonical_hash

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "benchmark/outliers/v1/regression"
OUT.mkdir(parents=True, exist_ok=True)

RELEASES = [
    (ROOT / "benchmark/cardiology/v1", ["q058", "q129", "c001", "c003", "c006", "c016"]),
    (ROOT / "benchmark/diabetes/v1", ["d008", "d015", "d026", "d014", "q030", "q034"]),
    (ROOT / "benchmark/oncology/v1", ["q079", "q083", "o009", "o026", "q078", "o014"]),
    (ROOT / "benchmark/outliers/v1", []),
]

articles: dict[str, dict] = {}
queries: list[dict] = []
anchors: dict[str, dict] = {}
source_files: dict[str, str] = {}
for directory, ids in RELEASES:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    query_file = json.loads((directory / "queries.json").read_text(encoding="utf-8"))
    for article in manifest["articles"]:
        aid = article["article_id"]
        previous = articles.get(aid)
        if previous is not None:
            old = (previous["filename"], previous["download"]["pdf_sha256"],
                   previous["validation"]["extracted_text_sha256"])
            new = (article["filename"], article["download"]["pdf_sha256"],
                   article["validation"]["extracted_text_sha256"])
            if old != new:
                raise ValueError(f"{aid}: topic releases pin different source tuples")
        else:
            articles[aid] = article
            source_files[article["filename"]] = article["download"]["pdf_sha256"]
    if not ids:
        continue
    selected = [q for q in query_file["queries"] if q["id"] in ids]
    if {q["id"] for q in selected} != set(ids):
        missing = set(ids) - {q["id"] for q in selected}
        raise ValueError(f"{directory}: requested sample has missing IDs {sorted(missing)}")
    queries.extend(selected)
    used = {aid for q in selected for e in q["evidence_sets"] for aid in e["anchors"]}
    used.update(d["anchor_id"] for q in selected for d in q["related_distractors"])
    for anchor in query_file["anchors"]:
        if anchor["id"] in used:
            previous = anchors.get(anchor["id"])
            if previous is not None and previous != anchor:
                raise ValueError(f"duplicate anchor ID differs: {anchor['id']}")
            anchors[anchor["id"]] = anchor

if len({q["id"] for q in queries}) != len(queries):
    raise ValueError("the selected topic query IDs are not unique")

articles_list = [articles[aid] for aid in sorted(articles)]
manifest = {"schema_version": "1.0", "corpus_version": "core-topics-plus-outliers-regression-v1",
    "status": "derived frozen comparison envelope; no source or topic selection changed",
    "source_releases": [str(p.relative_to(ROOT)) for p, _ in RELEASES],
    "articles": articles_list}
manifest["fingerprint_sha256"] = canonical_hash(manifest)
benchmark = {"schema_version": "1.0", "query_version": "outlier-expansion-regression-v1",
    "status": "frozen existing-topic sample; original per-case questions and anchors copied byte-for-byte",
    "authored_for": "JUA-113 focused outlier interference check",
    "selection_sha256": manifest["fingerprint_sha256"],
    "anchors": [anchors[aid] for aid in sorted(anchors)], "queries": queries}
benchmark["query_sha256"] = canonical_hash(
    {key: value for key, value in benchmark.items() if key != "query_sha256"})

tuples = [{"article_id": a["article_id"], "pmc_version": a["pmc_version"],
    "pdf_sha256": a["download"]["pdf_sha256"],
    "text_sha256": a["validation"]["extracted_text_sha256"]} for a in articles_list]
core_ids = [a["article_id"] for a in articles_list if a["article_id"] not in
            {x["article_id"] for x in json.loads((ROOT / "benchmark/outliers/v1/manifest.json").read_text())["articles"]}]
expanded_ids = sorted(articles)
core_tuples = [t for t in tuples if t["article_id"] in core_ids]
conditions = {"schema_version": "1.0", "corpus_version": manifest["corpus_version"],
    "query_sha256": canonical_hash(benchmark), "article_tuples": tuples,
    "query_version": benchmark["query_version"],
    "conditions": {
        "C1": {"article_ids": sorted(core_ids),
            "purpose": "Frozen cardiology, diabetes and oncology releases before outlier addition.",
            "membership_sha256": canonical_hash(core_tuples)},
        "C2": {"article_ids": expanded_ids,
            "purpose": "C1 plus all five selected outlier articles.",
            "membership_sha256": canonical_hash(tuples)},
    }}

def write(path: Path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")

write(OUT / "manifest.json", manifest)
write(OUT / "queries.json", benchmark)
write(OUT / "conditions.json", conditions)
print(f"Built regression envelope: {len(core_ids)} core articles, {len(expanded_ids)} expanded articles, {len(queries)} frozen cases, {len(anchors)} anchors")
