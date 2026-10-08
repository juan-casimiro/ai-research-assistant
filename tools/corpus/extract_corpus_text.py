#!/usr/bin/env python3
"""Extract local PDFs into a verified reusable text cache; no OCR or downloads."""
import argparse
import hashlib
import json
from pathlib import Path
import pypdf
from .build_corpus_manifest import atomic_write, validate_records
from .pdf_text import extract_pdf, METHOD

# Revisit at the next corpus expansion; no recovery workaround is applied.
EXCEPTION = ('PMC12003177', 1, 'd977b0dc0b6e1642cdf840e3980a7049b2705efea8c3673b1966228426b00747')
LIMITATION = 'Reporting-summary pages yield no text and are not searchable; pypdf output accepted as-is.'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save_json(path, data):
    atomic_write(path, data, path.read_bytes() if path.exists() else None)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=Path('data/corpus_manifest.json'))
    parser.add_argument('--corpus-dir', type=Path, required=True)
    parser.add_argument('--cache-dir', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        articles = validate_records(json.loads(args.manifest.read_text())['articles'])
        args.cache_dir.mkdir(parents=True, exist_ok=True)
        index_path = args.cache_dir / 'index.json'
        previous = json.loads(index_path.read_text()) if index_path.exists() else {}
        old = {e['source_id']: e for e in previous.get('articles', [])} if previous.get('schema_version') == 1 else {}
        extractor = {'tool': 'pypdf', 'version': pypdf.__version__, 'method': METHOD}
        entries, reports = [], []
        # Diagnostics are required for reuse, particularly the approved exception.
        report_path = args.cache_dir / 'extraction_report.json'
        old_reports = json.loads(report_path.read_text()).get('articles', []) if report_path.exists() else []
        diagnostics = {r['source_id']: r for r in old_reports}
        for article in articles:
            source_id = article['filename'][:-4]
            text_path = args.cache_dir / (source_id + '.txt')
            try:
                if article.get('id') != source_id:
                    raise ValueError('filename/ID mismatch')
                pdf_path = args.corpus_dir / article['filename']
                pdf_hash = digest(pdf_path.read_bytes())
                expected = article.get('metadata_sources', {}).get('pdf', {}).get('sha256')
                if expected is not None and expected != pdf_hash:
                    raise ValueError('PDF SHA-256 mismatch')
                diagnostic = diagnostics.get(source_id, {})
                entry = old.get(source_id, {})
                identity = (article['pmcid'], article['pmc_version'], pdf_hash)
                accepted_exception = identity == EXCEPTION
                reusable = (entry.get('pdf_sha256') == pdf_hash and entry.get('extractor') == extractor
                            and entry.get('text_file') == text_path.name and text_path.is_file()
                            and entry.get('text_sha256') == digest(text_path.read_bytes())
                            and text_path.read_text(encoding='utf-8').strip()
                            and diagnostic.get('pmcid') == article['pmcid']
                            and diagnostic.get('pmc_version') == article['pmc_version']
                            and diagnostic.get('status') == 'ok'
                            and diagnostic.get('accepted_exception') == accepted_exception
                            and (not diagnostic.get('pages_without_text') or accepted_exception))
                if reusable:
                    entries.append(entry)
                    reports.append(dict(diagnostic, reused=True))
                    continue
                text, missing = extract_pdf(pdf_path)
                if not text.strip():
                    raise ValueError('empty document text')
                if missing and not accepted_exception:
                    raise ValueError(f'pages without text: {missing}')
                raw = text.encode('utf-8')
                # Publish text only after all admission checks pass.
                temporary = text_path.with_suffix('.txt.part')
                try:
                    temporary.write_bytes(raw)
                    temporary.replace(text_path)
                finally:
                    temporary.unlink(missing_ok=True)
                entries.append({'source_id': source_id, 'pdf_sha256': pdf_hash,
                                'text_file': text_path.name, 'text_sha256': digest(raw), 'extractor': extractor})
                reports.append({'source_id': source_id, 'pmcid': article['pmcid'], 'pmc_version': article['pmc_version'],
                                'status': 'ok', 'reused': False, 'pages_without_text': missing,
                                'accepted_exception': accepted_exception, 'limitation': LIMITATION if accepted_exception else None})
            except Exception as error:
                text_path.unlink(missing_ok=True)
                reports.append({'source_id': source_id, 'pmcid': article['pmcid'], 'pmc_version': article['pmc_version'],
                                'status': 'requires_replacement', 'reason': str(error)})
                print(f"REQUIRES REPLACEMENT {article['pmcid']}: {error}")
        # Drop stale files from previous selections as well as failed entries.
        active = {e['text_file'] for e in entries}
        for entry in old.values():
            name = entry.get('text_file', '')
            if name and Path(name).name == name and name not in active:
                (args.cache_dir / name).unlink(missing_ok=True)
        save_json(index_path, {'schema_version': 1, 'articles': entries})
        failures = len(articles) - len(entries)
        save_json(report_path, {'schema_version': 1, 'selected': len(articles), 'included': len(entries),
                                'failed': failures, 'complete': failures == 0, 'articles': reports})
        print(f'Selected: {len(articles)}; included: {len(entries)}; requiring replacement: {failures}')
        return 1 if failures else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
