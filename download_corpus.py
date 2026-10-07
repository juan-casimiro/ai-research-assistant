#!/usr/bin/env python3
"""Download manifest PDFs from PMC; guide browser downloads for exceptions."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
from urllib.error import URLError
from urllib.parse import parse_qs, urlsplit
import urllib.request
import webbrowser

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
BUCKET = "https://pmc-oa-opendata.s3.amazonaws.com"
USER_AGENT = "ai-research-assistant-corpus-downloader/1.0"


def valid_pdf(path: Path) -> bool:
    """Reject HTML responses, truncated files and PDFs without readable pages."""
    try:
        with path.open("rb") as pdf_file:
            if pdf_file.read(5) != b"%PDF-":
                return False
            pdf_file.seek(0)
            reader = PdfReader(pdf_file, strict=True)
            return bool(reader.pages) and all(page.get_contents() is not None for page in reader.pages)
    except Exception:
        # pypdf raises several parser-specific exceptions for corrupt files.
        return False


def open_url(url: str):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": USER_AGENT}), timeout=60
    )


def resolve_pdf(article: dict) -> tuple[str, str | None]:
    """Use the manifest's explicit version, rather than guessing article versions."""
    pmcid = article["pmcid"]
    version = article.get("pmc_version", 1)
    if not re.fullmatch(r"PMC[0-9]+", pmcid) or type(version) is not int or version < 1:
        raise ValueError("invalid PMCID or PMC version")
    with open_url(f"{BUCKET}/metadata/{pmcid}.{version}.json") as response:
        metadata = json.load(response)
    if metadata.get("pmcid") != pmcid or metadata.get("doi", "").lower() != article["doi"].lower():
        raise ValueError("PMC metadata does not match the manifest PMCID/DOI")
    pdf_url = metadata.get("pdf_url")
    prefix = "s3://pmc-oa-opendata/"
    if not isinstance(pdf_url, str) or not pdf_url.startswith(prefix):
        raise ValueError("PMC metadata has no supported PDF URL")
    checksum = parse_qs(urlsplit(pdf_url).query).get("md5", [None])[0]
    return BUCKET + "/" + pdf_url[len(prefix):], checksum


def download(url: str, destination: Path, checksum: str | None) -> None:
    """Validate a unique temporary file before atomically replacing the target."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".part", delete=False) as pdf_file:
            temporary = Path(pdf_file.name)
            with open_url(url) as response:
                shutil.copyfileobj(response, pdf_file)
        if checksum:
            with temporary.open("rb") as pdf_file:
                actual = hashlib.file_digest(pdf_file, "md5").hexdigest()
            if actual != checksum:
                raise ValueError("PDF checksum mismatch")
        if not valid_pdf(temporary):
            raise ValueError("download is not a readable PDF")
        temporary.replace(destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "data/corpus_manifest.json")
    parser.add_argument("--corpus-dir", type=Path, default=ROOT / "corpus")
    parser.add_argument("--filename", action="append", help="Download only this exact manifest filename (repeatable)")
    parser.add_argument("--open-manual", action="store_true", help="Open missing manual articles in your default browser")
    args = parser.parse_args(argv)
    try:
        with args.manifest.open() as manifest_file:
            articles = json.load(manifest_file)["articles"]
        filenames = [article["filename"] for article in articles]
        if len(set(filenames)) != len(filenames) or any(
            Path(name).name != name or not name.endswith(".pdf") for name in filenames
        ):
            raise ValueError("manifest filenames must be unique PDF basenames")
        if args.filename and set(args.filename) - set(filenames):
            raise ValueError("requested filename is not in the manifest")
        args.corpus_dir.mkdir(parents=True, exist_ok=True)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}")
        return 1

    incomplete = []
    for article in articles:
        filename = article["filename"]
        if args.filename and filename not in args.filename:
            continue
        destination = args.corpus_dir / filename
        if valid_pdf(destination):
            print(f"SKIP {filename} (readable PDF already present)")
            continue
        if not article.get("pmcid"):
            url = article.get("manual_url", "https://doi.org/" + article["doi"])
            print(f"MANUAL {filename}: {url}\n  {article.get('download_note', 'Download the PDF in your browser.')}\n  Save as: {destination}")
            if args.open_manual:
                try:
                    if not webbrowser.open(url):
                        print("  Browser could not be opened; use the URL above.")
                except webbrowser.Error as error:
                    print(f"  Browser could not be opened: {error}")
            incomplete.append(filename)
            continue
        try:
            url, checksum = resolve_pdf(article)
            download(url, destination, checksum)
            print(f"OK {filename} ({destination.stat().st_size} bytes)")
        except (OSError, URLError, ValueError, KeyError, TypeError) as error:
            print(f"FAILED {filename}: {error}")
            incomplete.append(filename)
    if incomplete:
        print(f"Incomplete: {len(incomplete)} PDF(s) still required. Save manual PDFs and rerun.")
        return 1
    print("All selected corpus PDFs are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
