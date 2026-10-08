#!/usr/bin/env python3
"""Publish a fully validated local corpus, aborting on destination conflicts."""
import argparse
import json
import os
import hashlib
from urllib.parse import parse_qs, urlsplit
from pathlib import Path
import shutil
import tempfile
from .build_corpus_manifest import atomic_write, validate_selection
from .fetch_article_metadata import validate_metadata
from .download_corpus import BUCKET
from .extract_corpus_text import main as extract, digest, save_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--manifest-destination', type=Path, default=Path('data/corpus_manifest.json'))
    parser.add_argument('--pdf-destination', type=Path, default=Path('corpus/mvp'))
    parser.add_argument('--check', action='store_true', help='Validate and report without moving final artifacts')
    args = parser.parse_args(argv)
    run = args.run_dir
    source = run / 'corpus_manifest.json'
    pdfs = run / 'pdfs'
    failures = []
    published = False
    try:
        if args.pdf_destination.resolve().is_relative_to(run.resolve()) or args.manifest_destination.resolve().is_relative_to(run.resolve()):
            raise ValueError('final destinations must be outside the preparation run')
        original = source.read_bytes()
        manifest = json.loads(original)
        articles = validate_selection(manifest['articles'])
        selection = validate_selection(json.loads((run / 'candidates.json').read_text())['articles'])
        identities = lambda records: {(a['pmcid'], a['pmc_version'], a['filename']) for a in records}
        if identities(articles) != identities(selection):
            failures.append({'reason': 'prepared manifest does not match the complete selected PMCID/version/filename list'})
        for article in articles:
            try:
                validate_metadata(article)
                pdf = article.get('metadata_sources', {}).get('pdf', {})
                url = pdf.get('url', '')
                prefix = f"{BUCKET}/{article['pmcid']}.{article['pmc_version']}/"
                if not isinstance(url, str) or not url.startswith(prefix) or not urlsplit(url).path.endswith('.pdf'):
                    raise ValueError('missing or invalid pinned PDF source URL')
                raw = (pdfs / article['filename']).read_bytes()
                for checksum in [pdf.get('md5'), parse_qs(urlsplit(url).query).get('md5', [None])[0]]:
                    if checksum is not None and hashlib.md5(raw).hexdigest() != checksum:
                        raise ValueError('PDF provider MD5 mismatch')
                if 'extracted_text' in article.get('metadata_sources', {}):
                    raise ValueError('extraction provenance belongs in the local cache, not the manifest')
            except (OSError, ValueError, KeyError, TypeError) as error:
                failures.append({'pmcid': article['pmcid'], 'reason': str(error)})
        if failures:
            raise ValueError('metadata/selection validation failed')
        if extract(['--manifest', str(source), '--corpus-dir', str(pdfs), '--cache-dir', str(run / 'extracted_text')]):
            report = json.loads((run / 'extracted_text/extraction_report.json').read_text())
            failures.extend({'pmcid': a['pmcid'], 'reason': a['reason']} for a in report['articles'] if a['status'] != 'ok')
            raise ValueError('extraction validation failed')
        entries = {e['source_id']: e for e in json.loads((run / 'extracted_text/index.json').read_text())['articles']}
        for article in articles:
            article.setdefault('metadata_sources', {}).setdefault('pdf', {})['sha256'] = entries[article['id']]['pdf_sha256']
        expected = {a['filename']: entries[a['id']]['pdf_sha256'] for a in articles}
        if args.pdf_destination.exists():
            actual_names = {p.name for p in args.pdf_destination.iterdir()}
            if actual_names != set(expected):
                failures.append({'reason': 'PDF destination membership conflicts with prepared selection'})
            for name, checksum in expected.items():
                target = args.pdf_destination / name
                if not target.is_file() or digest(target.read_bytes()) != checksum:
                    failures.append({'reason': 'destination PDF is missing or has different bytes', 'file': str(target)})
        if args.manifest_destination.exists() and json.loads(args.manifest_destination.read_text()) != manifest:
            failures.append({'reason': 'destination manifest differs from prepared manifest', 'file': str(args.manifest_destination)})
        if failures:
            raise ValueError('destination conflicts')
        if not args.check:
            if source.read_bytes() != original:
                raise ValueError('prepared manifest changed during validation')
            staged = None
            created_pdfs = False
            try:
                if not args.pdf_destination.exists():
                    args.pdf_destination.parent.mkdir(parents=True, exist_ok=True)
                    staged = Path(tempfile.mkdtemp(dir=args.pdf_destination.parent, prefix='.corpus-'))
                    for name, checksum in expected.items():
                        shutil.copyfile(pdfs / name, staged / name)
                        if digest((staged / name).read_bytes()) != checksum:
                            raise ValueError('PDF changed during publication: ' + name)
                    if source.read_bytes() != original:
                        raise ValueError('prepared manifest changed during publication')
                    if args.pdf_destination.exists():
                        raise ValueError('PDF destination appeared during publication; resolve conflict')
                    os.rename(staged, args.pdf_destination)
                    staged = None
                    created_pdfs = True
                if args.manifest_destination.exists() and json.loads(args.manifest_destination.read_text()) != manifest:
                    raise ValueError('manifest destination changed during publication; resolve conflict')
                if not args.manifest_destination.exists():
                    atomic_write(args.manifest_destination, manifest)
                published = True
            except Exception:
                if created_pdfs:
                    shutil.rmtree(args.pdf_destination)
                raise
            finally:
                if staged is not None:
                    shutil.rmtree(staged)
            # Remove preparation originals only after both destinations succeeded.
            for name in expected:
                (pdfs / name).unlink()
            if not any(pdfs.iterdir()):
                pdfs.rmdir()
            source.unlink()
        save_json(run / 'publication_report.json', {'published': published, 'validated': True, 'failures': []})
        print('Publication validated.' if args.check else 'Corpus published; preparation originals removed.')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        if not failures:
            failures.append({'reason': str(error)})
        save_json(run / 'publication_report.json', {'published': published, 'validated': False, 'failures': failures})
        print('PUBLICATION COMPLETED; resolve preparation cleanup errors:' if published else
              'PUBLICATION ABORTED. Resolve these conflicts with the user before changing selection or destinations:')
        for failure in failures:
            print(f"  {failure.get('pmcid', failure.get('file', 'corpus'))}: {failure['reason']}")
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
