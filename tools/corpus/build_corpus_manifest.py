#!/usr/bin/env python3
"""Create or finalize a complete PMC corpus manifest using local PDFs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import parse_qs, urlsplit

import pypdf
from pypdf import PdfReader
from .fetch_article_metadata import fetch_metadata, licence_eligibility, cloud_url
from .download_corpus import BUCKET

# Revisit at the next expansion: resolve extraction or replace/exclude the article.
READABILITY_EXCEPTION = (
    "PMC12003177", 1,
    "d977b0dc0b6e1642cdf840e3980a7049b2705efea8c3673b1966228426b00747",
)
EXCEPTION_NOTE = "User-approved readability exception for PMC12003177 v1: pages 22–24 are reporting-summary forms with no extracted text; pages 1–21 yield text. Appended forms are not searchable."
EXTRACTION_METHOD = 'ingest_corpus.ingest_file: pypdf.PdfReader; newline-joined page.extract_text() or empty string'


def validate_selection(articles):
    if not isinstance(articles, list) or not articles:
        raise ValueError("articles must be a nonempty list")
    seen = set()
    for article in articles:
        pmcid, version = article['pmcid'], article['pmc_version']
        if not isinstance(pmcid, str) or not re.fullmatch(r'PMC[0-9]+', pmcid):
            raise ValueError('invalid PMCID')
        if pmcid in seen:
            raise ValueError('duplicate PMCID: ' + pmcid)
        seen.add(pmcid)
        if type(version) is not int or version < 1:
            raise ValueError('pmc_version must be a positive integer')
        filename = article['filename']
        if not isinstance(filename, str) or not re.fullmatch(re.escape(pmcid) + r'-[a-z0-9]+(?:-[a-z0-9]+){0,6}\.pdf', filename):
            raise ValueError('filename must match PMCID plus 1–7 lowercase hyphen-separated words')
        for field in ['cluster', 'search_query']:
            if not isinstance(article.get(field), str) or not article[field].strip():
                raise ValueError(field + ' must be nonempty')
    return articles


def validate_metadata(record):
    for field in ['pmid', 'doi', 'title', 'journal', 'publication_date', 'pubmed_url', 'abstract']:
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError('missing mandatory field: ' + field)
    if not re.fullmatch(r'[0-9]+', record['pmid']):
        raise ValueError('invalid PMID')
    if record['pubmed_url'] != f"https://pubmed.ncbi.nlm.nih.gov/{record['pmid']}/":
        raise ValueError('PubMed identity URL mismatch')
    if record.get('abstract_absence_reason'):
        raise ValueError('PubMed abstract is marked absent')
    if not isinstance(record.get('authors'), list) or not record['authors'] or any(
        not isinstance(name, str) or not name.strip() for name in record['authors']
    ):
        raise ValueError('missing bibliography authors')
    if type(record.get('year')) is not int or record['year'] < 1:
        raise ValueError('missing bibliography year')
    for field in ['id', 'article_id']:
        if record.get(field) != record['filename'][:-4]:
            raise ValueError('filename/ID mismatch: ' + field)
    if licence_eligibility(record.get('license'), record.get('licence_urls', [])) != 'eligible':
        raise ValueError('unsupported or missing licence evidence')


def complete_provenance(record, corpus_dir, provenance_dir=None):
    validate_metadata(record)
    path = corpus_dir / record['filename']
    raw = path.read_bytes()
    pdf_hash = hashlib.sha256(raw).hexdigest()
    sources = record.setdefault('metadata_sources', {})
    pdf = sources.setdefault('pdf', {})
    if not pdf.get('url') and provenance_dir is not None:
        source = provenance_dir / f"{record['pmcid']}.{record['pmc_version']}.cloud.json"
        source_bytes = source.read_bytes()
        expected = sources.get('cloud.json', {}).get('sha256') or record.get('metadata_sha256')
        if expected and hashlib.sha256(source_bytes).hexdigest() != expected:
            raise ValueError('PMC Cloud source SHA-256 mismatch')
        cloud = json.loads(source_bytes)
        if (cloud.get('pmcid'), cloud.get('version'), str(cloud.get('pmid')), cloud.get('doi', '').lower()) != (
            record['pmcid'], record['pmc_version'], record['pmid'], record['doi'].lower()
        ):
            raise ValueError('PMC Cloud source identity mismatch')
        pdf['url'] = cloud_url(cloud['pdf_url'])
    url = pdf.get('url', '')
    prefix = f"{BUCKET}/{record['pmcid']}.{record['pmc_version']}/"
    if not isinstance(url, str) or not url.startswith(prefix) or not urlsplit(url).path.endswith('.pdf') or urlsplit(url).fragment:
        raise ValueError('missing or invalid pinned PMC PDF source URL')
    if pdf.get('sha256') is not None and pdf['sha256'] != pdf_hash:
        raise ValueError('PDF SHA-256 mismatch')
    md5 = hashlib.md5(raw).hexdigest()
    provider_md5 = parse_qs(urlsplit(url).query).get('md5', [None])[0]
    for expected in [pdf.get('md5'), provider_md5]:
        if expected is not None and expected != md5:
            raise ValueError('PDF MD5 mismatch')
    # Exactly production ingestion: default PdfReader, newline join, UTF-8 bytes.
    reader = PdfReader(str(path))
    texts = [page.extract_text() or '' for page in reader.pages]
    if not texts:
        raise ValueError('PDF has no pages')
    missing = [i for i, text in enumerate(texts, 1) if not text.strip()]
    exception = (record['pmcid'], record['pmc_version'], pdf_hash) == READABILITY_EXCEPTION and missing == [22, 23, 24]
    if missing and not exception:
        raise ValueError(f'no extracted text on pages {missing}')
    text_hash = hashlib.sha256('\n'.join(texts).encode('utf-8')).hexdigest()
    extraction = sources.setdefault('extracted_text', {})
    if extraction.get('sha256') is not None and extraction['sha256'] != text_hash:
        raise ValueError('extracted-text SHA-256 mismatch')
    if record.get('page_count') is not None and record['page_count'] != len(texts):
        raise ValueError('page count mismatch')
    pdf.update(sha256=pdf_hash, md5=md5)
    extraction.update(sha256=text_hash, method=EXTRACTION_METHOD, pypdf_version=pypdf.__version__,
                      encoding='UTF-8', pages_without_text=missing)
    record['page_count'] = len(texts)
    record['eligibility'] = 'eligible'
    if exception and EXCEPTION_NOTE not in record.get('notes', ''):
        record['notes'] = (record.get('notes', '') + ' ' + EXCEPTION_NOTE).strip()


def atomic_write(path, manifest, original=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False, mode='w', encoding='utf-8') as output:
            temporary = Path(output.name)
            output.write(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
            output.flush()
            os.fsync(output.fileno())
        if original is None:
            os.link(temporary, path)  # Refuse an existing output, even if created concurrently.
        else:
            if path.read_bytes() != original:
                raise ValueError('manifest changed during finalization')
            temporary.chmod(path.stat().st_mode & 0o777)
            os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--candidates', type=Path)
    mode.add_argument('--finalize', type=Path, help='Validate and complete this existing manifest in place, offline')
    parser.add_argument('--corpus-dir', type=Path, required=True)
    parser.add_argument('--provenance-dir', type=Path, help='Retained PMC Cloud responses, for missing pinned PDF URLs')
    parser.add_argument('--output', type=Path, help='Creation output; defaults to data/corpus_manifest.json')
    args = parser.parse_args(argv)
    if args.finalize and args.output:
        parser.error('--output cannot be used with --finalize')
    path = args.finalize or args.output or Path('data/corpus_manifest.json')
    try:
        original = path.read_bytes() if args.finalize else None
        if not args.finalize and path.exists():
            raise ValueError('output already exists; use --finalize')
        envelope = json.loads(original if args.finalize else args.candidates.read_bytes())
        selected = validate_selection(envelope['articles'])
        records, excluded = [], []
        for article in selected:
            try:
                record = article if args.finalize else fetch_metadata(
                    article['pmcid'], article['pmc_version'], article['search_query'], article['filename'], article['cluster'])
                complete_provenance(record, args.corpus_dir, args.provenance_dir)
                records.append(record)
            except Exception as error:
                excluded.append((article['pmcid'], str(error)))
                print(f"EXCLUDED {article['pmcid']}: {error}")
        print(f'Selected: {len(selected)}; included: {len(records)}; excluded: {len(excluded)}')
        if excluded:
            raise ValueError('incomplete selection; no manifest written')
        if args.finalize:
            manifest = envelope
        else:
            manifest = {'articles': records}
            if 'source' in envelope:
                manifest['candidate_source'] = envelope['source']
        atomic_write(path, manifest, original)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'ERROR: {error}')
        return 1
    print(f'Manifest saved: {path} ({len(records)} articles)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
