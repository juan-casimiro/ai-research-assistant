"""Re-score saved local contexts after source-based annotation-only corrections.

Requires byte-equivalent questions, anchors, sources, and evidence-set bindings.
Preserves the parent retrieval output; records both envelopes and parent hashes.
This does not run models, retrieve, generate, judge, or ingest.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from benchmark_scoring import (canonical_hash, compile_anchor_spans,
                               compile_query_feasibility, score_evidence,
                               validate_benchmark)
from eval_benchmark import read_release, summarize
from main import chunk_text


def annotation_invariant(query):
    result = copy.deepcopy(query)
    for key in ['revision', 'category', 'reasoning', 'reference_answer']:
        result.pop(key, None)
    for fact in result['required_facts']:
        fact.pop('expected_text', None)
    return result


def verify_parent(parent, initial, initial_conditions, current, conditions):
    validate_benchmark(initial)
    validate_benchmark(current)
    if parent['run_status'] != 'complete' or parent['provenance']['missing_ids']:
        raise ValueError('incomplete parent run')
    if (parent['provenance']['query_sha256'] != canonical_hash(initial) or
            parent['provenance']['conditions_sha256'] != canonical_hash(initial_conditions)):
        raise ValueError('parent envelope fingerprint mismatch')
    if initial['anchors'] != current['anchors']:
        raise ValueError('changed evidence anchors require separate evaluation review')
    old = {q['id']: q for q in initial['queries']}
    new = {q['id']: q for q in current['queries']}
    if old.keys() != new.keys():
        raise ValueError('case membership changed')
    for qid in old:
        if annotation_invariant(old[qid]) != annotation_invariant(new[qid]):
            raise ValueError(f'{qid}: retrieval question, scope or evidence bindings changed')
    expected = sorted(new)
    provenance = parent['provenance']
    if (provenance['requested_ids'] != expected or provenance['executed_ids'] != expected or
            sorted(r['id'] for r in parent['results']) != expected):
        raise ValueError('parent lacks complete requested case coverage')
    for result in parent['results']:
        if (result['query_sha256'] != canonical_hash(old[result['id']]) or
                result['question'] != new[result['id']]['question']):
            raise ValueError('parent result question/hash mismatch')
    a, b = copy.deepcopy(initial_conditions), copy.deepcopy(conditions)
    a.pop('query_sha256'); b.pop('query_sha256')
    if a != b or initial['selection_sha256'] != current['selection_sha256']:
        raise ValueError('source selection or condition changed')
    return old, new


def rescore(parent_path, initial_dir, release_dir, corpus_dir, output_path):
    parent_bytes = parent_path.read_bytes()
    parent = json.loads(parent_bytes)
    initial = json.loads((initial_dir / 'queries.json').read_text())
    initial_conditions = json.loads((initial_dir / 'conditions.json').read_text())
    benchmark, _, conditions, _, _, texts = read_release(
        release_dir, corpus_dir, parent['provenance']['condition'])
    old, new = verify_parent(parent, initial, initial_conditions, benchmark, conditions)
    anchors = {a['id']: a for a in benchmark['anchors']}
    used = {aid for q in benchmark['queries'] for s in q['evidence_sets'] for aid in s['anchors']}
    plans = compile_anchor_spans({aid: anchors[aid] for aid in used}, texts, chunk_text)
    feasibility = compile_query_feasibility(benchmark['queries'], anchors, plans,
        {source: chunk_text(text) for source, text in texts.items()})
    if canonical_hash(feasibility) != parent['provenance']['feasibility_sha256']:
        raise ValueError('feasibility changed')
    output = copy.deepcopy(parent)
    output['run_id'] = parent['run_id'] + '-annotation-rescore'
    output['created_at'] = datetime.now(timezone.utc).isoformat()
    output['derivation'] = {'kind': 'offline_annotation_rescore',
        'parent_path': str(parent_path), 'parent_sha256': hashlib.sha256(parent_bytes).hexdigest(),
        'parent_run_id': parent['run_id'], 'parent_provenance': parent['provenance'],
        'initial_release_sha256': canonical_hash(initial),
        'current_release_sha256': canonical_hash(benchmark),
        'helper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'changed_ids': sorted(qid for qid in old if old[qid] != new[qid]),
        'retrieval_calls': 0, 'reason': 'Source-based category/reference corrections; no question, source or evidence change; no score-driven tuning.'}
    output['provenance']['query_sha256'] = canonical_hash(benchmark)
    output['provenance']['subset_sha256'] = canonical_hash(benchmark['queries'])
    output['provenance']['conditions_sha256'] = canonical_hash(conditions)
    for entry in output['results']:
        query = new[entry['id']]
        entry.update(revision=query['revision'], category=query['category'], query_sha256=canonical_hash(query))
        for depth in [3, 8]:
            value = entry[f'n{depth}']
            metrics = score_evidence(value['retrieved_contexts'], value['retrieved_sources'], query, anchors, plans)
            if metrics != value['metrics']:
                raise ValueError('annotation correction unexpectedly changed evidence/document scores')
            value['metrics'] = metrics
    output['summary'] = summarize(output['results'])
    with output_path.open('x') as stream:
        json.dump(output, stream, indent=2, ensure_ascii=False, allow_nan=False)
    print(f'Saved {output_path}: {len(output["results"])} cases, zero retrieval calls')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('parent', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--initial', type=Path, default=Path('benchmark/diabetes/v1/runs/initial-authoring'))
    parser.add_argument('--benchmark', type=Path, default=Path('benchmark/diabetes/v1'))
    parser.add_argument('--corpus-dir', type=Path, default=Path('corpus/diabetes-v1'))
    args = parser.parse_args()
    rescore(args.parent, args.initial, args.benchmark, args.corpus_dir, args.output)
