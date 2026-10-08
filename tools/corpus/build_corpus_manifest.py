#!/usr/bin/env python3
"""Assemble or validate a PMC corpus manifest from existing metadata records."""
import argparse
import json
import os
from pathlib import Path
import re
import tempfile

from .fetch_article_metadata import validate_metadata
from .download_corpus import BUCKET

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
    mode.add_argument('--records-dir', type=Path, help='Directory of per-article metadata JSON records')
    mode.add_argument('--finalize', type=Path, help='Validate this existing manifest in place, offline')
    parser.add_argument('--output', type=Path, help='Preparation output; defaults to corpus_manifest.json beside the records directory')
    args = parser.parse_args(argv)
    if args.finalize and args.output:
        parser.error('--output cannot be used with --finalize')
    path = args.finalize or args.output or (args.records_dir.parent / 'corpus_manifest.json')
    try:
        original = path.read_bytes() if args.finalize else None
        if not args.finalize and path.exists():
            raise ValueError('output already exists; use --finalize')
        envelope = json.loads(original) if args.finalize else {'articles': [json.loads(p.read_text()) for p in sorted(args.records_dir.glob('*.json'))]}
        selected = validate_selection(envelope['articles'])
        records, excluded = [], []
        for article in selected:
            try:
                record = article
                validate_metadata(record)
                record.get('metadata_sources', {}).pop('extracted_text', None)
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
