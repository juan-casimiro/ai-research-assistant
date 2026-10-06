#!/usr/bin/env python3
"""Verify the pinned cardiology selection locally without ingestion or API calls."""
import argparse
import hashlib
import json
from pathlib import Path
from tools.layout import recorded_path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SELECTION = ROOT / "data/benchmark/sources/cardiology/v1"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(data) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def verify(selection_dir: Path, corpus_dir: Path) -> int:
    manifest = json.loads((selection_dir / "manifest.json").read_text())
    fingerprint = manifest.pop("fingerprint_sha256")
    if digest(canonical(manifest)) != fingerprint:
        raise ValueError("manifest fingerprint mismatch")
    articles = manifest["articles"]
    if not articles:
        raise ValueError("selected corpus is empty")
    for key in ["article_id", "filename", "pmcid", "doi"]:
        if len({a[key] for a in articles}) != len(articles):
            raise ValueError(f"duplicate {key}")
    core_fields = ["filename", "cluster", "search_query", "doi", "pmcid", "pmc_version", "pmid", "title", "authors", "journal", "abstract", "abstract_summary", "year", "license", "page_count", "has_structured_sections", "notes", "license_notes"]
    evidence = json.loads((selection_dir / "evidence_map.json").read_text())["articles"]
    if {e["article_id"] for e in evidence} != {a["article_id"] for a in articles}:
        raise ValueError("evidence-map membership differs from selected corpus")
    inventory = (selection_dir / "ATTRIBUTION.md").read_text()
    for article in articles:
        article_id = article["article_id"]
        if any(field not in article for field in core_fields):
            raise ValueError(f"{article_id}: missing legacy/core metadata")
        if not article["search_query"] or not article["abstract"] or not article["authors"]:
            raise ValueError(f"{article_id}: incomplete search/abstract/author metadata")
        if article["eligibility"] != "eligible" or article["licence"]["id"] not in {"CC-BY-4.0", "CC0-1.0"} or article["third_party_review"]["status"] != "clear":
            raise ValueError(f"{article_id}: eligibility gate failure")
        if "manual_url" in article or article["download"]["route"] != "pmc_cloud":
            raise ValueError(f"{article_id}: unsupported download route")
        name = article["filename"]
        if Path(name).name != name or not name.endswith(".pdf"):
            raise ValueError(f"{article_id}: invalid PDF basename")
        pdf = corpus_dir / name
        if digest(pdf.read_bytes()) != article["download"]["pdf_sha256"]:
            raise ValueError(f"{article_id}: PDF hash mismatch")
        try:
            reader = PdfReader(pdf, strict=True)
            pages = [page.extract_text() or "" for page in reader.pages]
        except Exception as error:
            # Corrupt content can raise parser-specific and built-in exceptions.
            # Keep this boundary limited to PDF parsing and text extraction.
            raise ValueError(f"{article_id}: unreadable PDF") from error
        if not pages or len(pages) != article["page_count"] or not any(p.strip() for p in pages):
            raise ValueError(f"{article_id}: unreadable PDF or changed page count")
        extracted = "\n".join(pages)
        if digest(extracted.encode()) != article["validation"]["extracted_text_sha256"]:
            raise ValueError(f"{article_id}: PDF extraction changed; check parser version")
        if digest(pdf.with_suffix(".txt").read_bytes()) != article["validation"]["extracted_text_sha256"]:
            raise ValueError(f"{article_id}: saved text hash mismatch")
        source = article["metadata_sources"]["pmc_cloud"]
        archived = (selection_dir / source["archive"]).read_bytes()
        if digest(archived) != article["metadata_sha256"]:
            raise ValueError(f"{article_id}: metadata hash mismatch")
        metadata = json.loads(archived)
        if (metadata["pmcid"], metadata["version"], metadata["doi"], str(metadata["pmid"])) != (article["pmcid"], article["pmc_version"], article["doi"], article["pmid"]):
            raise ValueError(f"{article_id}: archived identifiers differ")
        for source_key in ["pubmed", "pmcid_converter"]:
            source = article["metadata_sources"][source_key]
            if digest((selection_dir / source["archive"]).read_bytes()) != source["sha256"]:
                raise ValueError(f"{article_id}: {source_key} archive hash mismatch")
        source = article["metadata_sources"]["pmc_article_xml"]
        xml = corpus_dir / f"{article['pmcid']}.{article['pmc_version']}.xml"
        try:
            xml_bytes = xml.read_bytes()
        except OSError as error:
            raise ValueError(f"{article_id}: missing or unreadable article XML") from error
        if digest(xml_bytes) != source["sha256"]:
            raise ValueError(f"{article_id}: article XML hash mismatch")
        entry = next(e for e in evidence if e["article_id"] == article_id)
        if entry["pdf_sha256"] != article["download"]["pdf_sha256"] or entry["text_sha256"] != article["validation"]["extracted_text_sha256"] or not entry["selection_locations"]:
            raise ValueError(f"{article_id}: evidence is missing or names different bytes")
        for location in entry["selection_locations"]:
            raw = extracted[location["text_start"]:location["text_end"]]
            if raw != location["excerpt"] or digest(raw.encode()) != location["excerpt_sha256"]:
                raise ValueError(f"{article_id}: evidence offset/hash mismatch")
        if f"## {article_id}\n" not in inventory or article["download"]["pdf_sha256"] not in inventory:
            raise ValueError(f"{article_id}: missing attribution entry/hash")
    conditions = json.loads((selection_dir / "conditions.json").read_text())
    by_id = {a["article_id"]: a for a in articles}
    expected_tuples = [{"article_id": a["article_id"], "pmc_version": a["pmc_version"], "pdf_sha256": a["download"]["pdf_sha256"], "text_sha256": a["validation"]["extracted_text_sha256"]} for a in articles]
    if conditions["article_tuples"] != expected_tuples:
        raise ValueError("condition versions/hashes differ from manifest")
    sets = []
    for name in ["C1", "C2", "C3"]:
        condition = conditions["conditions"][name]
        ids = condition["article_ids"]
        if ids != sorted(set(ids)) or not set(ids) <= set(by_id):
            raise ValueError(f"{name}: invalid membership")
        tuples = [t for t in expected_tuples if t["article_id"] in ids]
        if digest(canonical(tuples)) != condition["membership_sha256"]:
            raise ValueError(f"{name}: membership fingerprint mismatch")
        sets.append(set(ids))
    if not sets[0] <= sets[1] <= sets[2] or sets[2] != set(by_id):
        raise ValueError("conditions are not nested or do not cover selection")
    migration = json.loads((selection_dir / "migration.json").read_text())
    for path, expected in migration["baseline"]["files"].items():
        if digest(recorded_path(path, ROOT).read_bytes()) != expected:
            raise ValueError(f"preserved baseline changed: {path}")
    return len(articles)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection-dir", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument("--corpus-dir", type=Path, default=ROOT / "corpus/cardiology-v1")
    args = parser.parse_args(argv)
    try:
        count = verify(args.selection_dir, args.corpus_dir)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}")
        return 1
    print(f"Verified {count} articles: metadata/XML, PDF/text hashes, evidence offsets, attribution, nested conditions and preserved baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
