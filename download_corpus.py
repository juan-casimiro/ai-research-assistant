#!/usr/bin/env python3
"""Download the corpus PDFs listed in corpus_manifest.json.

One route covers every article with a `pmcid`: the PMC AWS open-data bucket
(see corpus_info.download_notes in the manifest). Articles without a `pmcid`
(the two Singapore Medical Journal papers) have no curl-reachable source and
are reported for manual browser download via Ovid instead.

Idempotent: files already present with a %PDF header are skipped.
"""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "corpus_manifest.json"
OUT_DIR = ROOT / "corpus"
BUCKET = "https://pmc-oa-opendata.s3.amazonaws.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def download(url: str, dest: Path) -> bool:
    tmp = dest.with_suffix(".part")
    rc = subprocess.run(
        ["curl", "-sSL", "--fail", "--max-time", "180", "-A", UA, "-o", str(tmp), url],
        check=False,
    ).returncode
    if rc != 0 or not tmp.exists() or tmp.open("rb").read(5) != b"%PDF-":
        tmp.unlink(missing_ok=True)
        return False
    tmp.rename(dest)
    return True


def main() -> int:
    manifest = json.load(open(MANIFEST))
    OUT_DIR.mkdir(exist_ok=True)
    failures = []
    manual = []
    for article in manifest["articles"]:
        fname = article["filename"]
        dest = OUT_DIR / fname
        if dest.exists() and dest.open("rb").read(5) == b"%PDF-":
            print(f"SKIP {fname} (already present)")
            continue
        pmcid = article.get("pmcid")
        if not pmcid:
            manual.append((fname, article["doi"]))
            print(f"MANUAL {fname}: no pmcid — {article.get('download_note', 'see manifest')}")
            continue
        print(f"GET  {fname}  {pmcid}")
        ok = False
        for version in ("1", "2", "3"):
            try:
                meta = get_json(f"{BUCKET}/metadata/{pmcid}.{version}.json")
            except Exception:
                continue
            pdf_url = meta.get("pdf_url")
            if not pdf_url:
                continue
            pdf_url = re.sub(r"^s3://pmc-oa-opendata/", f"{BUCKET}/", pdf_url)
            if download(pdf_url, dest):
                print(f"  OK ({dest.stat().st_size} bytes)")
                ok = True
                break
        if not ok:
            failures.append((fname, pmcid))
            print(f"  FAILED {fname}")
    print()
    if manual:
        print(f"{len(manual)} need manual browser download:")
        for fname, doi in manual:
            print(f"  {fname}  https://doi.org/{doi}")
    if failures:
        print(f"{len(failures)} FAILED:")
        for fname, pmcid in failures:
            print(f"  {fname}  {pmcid}")
        return 1
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
