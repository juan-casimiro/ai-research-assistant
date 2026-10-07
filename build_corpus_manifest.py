#!/usr/bin/env python3
"""Build a corpus manifest from explicitly selected PMC candidates."""
import argparse
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from fetch_article_metadata import fetch_metadata


def load_candidates(path: Path) -> list[dict]:
    candidates = json.loads(path.read_text(encoding="utf-8"))["articles"]
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("articles must be a nonempty list")
    seen = set()
    for article in candidates:
        pmcid = article["pmcid"]
        version = article["pmc_version"]
        if not isinstance(pmcid, str) or not re.fullmatch(r"PMC[0-9]+", pmcid):
            raise ValueError("invalid PMCID")
        if pmcid in seen:
            raise ValueError("duplicate PMCID: " + pmcid)
        seen.add(pmcid)
        if type(version) is not int or version < 1:
            raise ValueError("pmc_version must be a positive integer")
        filename = article["filename"]
        if not isinstance(filename, str) or not re.fullmatch(re.escape(pmcid) + r"-[a-z0-9]+(?:-[a-z0-9]+){0,6}\.pdf", filename):
            raise ValueError("filename must match PMCID plus 1–7 lowercase hyphen-separated words")
        for field in ["cluster", "search_query"]:
            if not isinstance(article[field], str) or not article[field].strip():
                raise ValueError(field + " must be nonempty")
    return candidates


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/corpus_manifest.json"))
    args = parser.parse_args(argv)
    try:
        if args.output.exists():
            raise ValueError("output already exists; choose a new path")
        candidates = load_candidates(args.candidates)
        records = []
        for index, article in enumerate(candidates, 1):
            print(f"Metadata {index}/{len(candidates)}: {article['pmcid']}", flush=True)
            records.append(fetch_metadata(article["pmcid"], article["pmc_version"], article["search_query"],
                                          article["filename"], article["cluster"]))
        manifest = {"articles": records}
        source = json.loads(args.candidates.read_text(encoding="utf-8")).get("source")
        if source is not None:
            manifest["candidate_source"] = source
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as output:
            output.write(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as error:
        print(f"ERROR: {error}")
        return 1
    print(f"Manifest saved: {args.output} ({len(records)} articles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
