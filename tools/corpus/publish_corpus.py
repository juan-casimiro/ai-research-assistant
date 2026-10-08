#!/usr/bin/env python3
"""Validate the entire selection, check conflicts, then move PDFs and text."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from urllib.parse import parse_qs, urlsplit
from .build_corpus_manifest import save_json
from .download_corpus import BUCKET
from .fetch_article_metadata import validate_record, validate_selection
from .extract_corpus_text import digest, extract_article


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--manifest-destination', type=Path, default=Path('data/corpus_manifest.json'))
    parser.add_argument('--pdf-destination', type=Path, default=Path('corpus/mvp'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    if not args.run_dir.is_dir():
        print(f'ERROR: run directory does not exist or is not a directory: {args.run_dir}')
        return 1
    failures, files = [], []
    try:
        if any(p.resolve().is_relative_to(args.run_dir.resolve()) for p in [args.pdf_destination, args.manifest_destination]):
            raise ValueError('final destinations must be outside the preparation run')
        source = args.run_dir / 'corpus_manifest.json'
        manifest = json.loads(source.read_text())
        articles = manifest['articles']
        selection = validate_selection(json.loads((args.run_dir / 'candidates.json').read_text())['articles'])
        requested, prepared = {a['pmcid'] for a in selection}, {a['pmcid'] for a in articles}
        for pmcid in sorted(requested - prepared):
            failures.append({'pmcid': pmcid, 'reason': 'selected PMCID missing from prepared manifest'})
        for pmcid in sorted(prepared - requested):
            failures.append({'pmcid': pmcid, 'reason': 'prepared PMCID not in supplied selection'})
        if len(prepared) != len(articles):
            raise ValueError('duplicate PMCID in prepared manifest')
        if not articles:
            raise ValueError('articles must be a nonempty list')
        for article in articles:
            try:
                validate_record(article)
                pdf_source = article.get('metadata_sources', {}).get('pdf', {})
                url = pdf_source.get('url', '')
                prefix = f"{BUCKET}/{article['pmcid']}.{article['pmc_version']}/"
                if not isinstance(url, str) or not url.startswith(prefix) or not urlsplit(url).path.endswith('.pdf'):
                    raise ValueError('missing or invalid pinned PDF source URL')
                target = args.pdf_destination / article['filename']
                pdf = args.run_dir / 'pdfs' / article['filename']
                if not pdf.exists() and target.exists():
                    pdf = target  # Rerun after a successful or partial move.
                raw = pdf.read_bytes()
                checksums = [pdf_source.get('md5'), parse_qs(urlsplit(url).query).get('md5', [None])[0]]
                if not any(checksums):
                    raise ValueError('missing PDF provider MD5 checksum')
                for checksum in checksums:
                    if checksum is not None and hashlib.md5(raw).hexdigest() != checksum:
                        raise ValueError('PDF provider MD5 mismatch')
                text = extract_article(article, pdf).encode('utf-8')
                pdf_source['sha256'] = digest(raw)
                text_source = (args.run_dir / 'pdfs' / article['filename']).with_suffix('.txt')
                files.extend([(pdf, target, raw), (text_source, target.with_suffix('.txt'), text)])
            except Exception as error:
                failures.append({'pmcid': article['pmcid'], 'reason': str(error)})
        for _, target, expected in files:
            if (target.exists() or target.is_symlink()) and (not target.is_file() or target.read_bytes() != expected):
                failures.append({'file': str(target), 'reason': 'destination has different content'})
        if args.manifest_destination.exists() or args.manifest_destination.is_symlink():
            try:
                matching = json.loads(args.manifest_destination.read_text()) == manifest
            except (OSError, ValueError):
                matching = False
            if not matching:
                failures.append({'file': str(args.manifest_destination), 'reason': 'destination manifest differs'})
        if failures:
            raise ValueError('validation or destination conflicts')
        if not args.check:
            args.pdf_destination.mkdir(parents=True, exist_ok=True)
            for prepared_file, target, expected in files:
                if target.exists():
                    if prepared_file != target:
                        prepared_file.unlink(missing_ok=True)
                    continue
                if prepared_file.suffix == '.txt':
                    prepared_file.write_bytes(expected)
                if prepared_file == target:
                    continue
                shutil.move(str(prepared_file), str(target))
            if not args.manifest_destination.exists():
                save_json(args.manifest_destination, manifest)
        save_json(args.run_dir / 'publication_report.json', {'published': not args.check, 'validated': True, 'failures': []})
        print('Publication validated.' if args.check else 'Corpus published.')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        if not failures:
            failures.append({'reason': str(error)})
        save_json(args.run_dir / 'publication_report.json', {'published': False, 'validated': False, 'failures': failures})
        for failure in failures:
            print(f"FAILED {failure.get('pmcid', failure.get('file', 'corpus'))}: {failure['reason']}")
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
