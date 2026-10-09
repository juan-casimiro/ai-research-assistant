#!/usr/bin/env python3
"""Extract every PDF with the production extractor into adjacent text files."""
import argparse
import hashlib
import json
from pathlib import Path
from .build_corpus_manifest import save_json, validate_records
from .download_corpus import named_corpus_dir
from .pdf_text import extract_pdf

# Revisit at the next corpus expansion; no recovery workaround is applied.
EXCEPTION = ('PMC12003177', 1, 'd977b0dc0b6e1642cdf840e3980a7049b2705efea8c3673b1966228426b00747')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def extract_article(article, pdf_path):
    checksum = digest(pdf_path.read_bytes())
    expected = article.get('metadata_sources', {}).get('pdf', {}).get('sha256')
    if expected is not None and expected != checksum:
        raise ValueError('PDF SHA-256 mismatch')
    text, missing = extract_pdf(pdf_path)
    accepted = (article['pmcid'], article['pmc_version'], checksum) == EXCEPTION
    if not text.strip():
        raise ValueError('empty document text')
    if missing and not accepted:
        raise ValueError(f'pages without text: {missing}')
    return text


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=Path('data/corpus_manifest.json'))
    parser.add_argument('--corpus-dir', type=Path, help='Defaults to corpus/<corpus_name>/ from the manifest')
    args = parser.parse_args(argv)
    failures = []
    try:
        manifest = json.loads(args.manifest.read_text())
        articles = validate_records(manifest['articles'])
        if args.corpus_dir is None:
            args.corpus_dir = named_corpus_dir(manifest)
        for article in articles:
            pdf = args.corpus_dir / article['filename']
            try:
                pdf.with_suffix('.txt').write_text(extract_article(article, pdf), encoding='utf-8')
            except Exception as error:
                pdf.with_suffix('.txt').unlink(missing_ok=True)
                failures.append({'pmcid': article['pmcid'], 'reason': str(error)})
                print(f"FAILED {article['pmcid']}: {error}")
        save_json(args.corpus_dir / 'extraction_report.json', {'complete': not failures, 'failures': failures})
        return int(bool(failures))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
