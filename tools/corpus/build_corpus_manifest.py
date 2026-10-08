#!/usr/bin/env python3
"""Assemble a complete manifest from existing metadata records, offline."""
import argparse
import json
from pathlib import Path
from .fetch_article_metadata import validate_records


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    path = args.output or args.records_dir.parent / 'corpus_manifest.json'
    try:
        articles = validate_records([json.loads(p.read_text()) for p in sorted(args.records_dir.glob('*.json'))])
        manifest = {'articles': articles}
        save_json(path, manifest)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'ERROR: {error}')
        return 1
    print(f'Manifest saved: {path} ({len(articles)} articles)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
