"""Generate the readable current-benchmark case index without models or corpus files."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / 'benchmark/combined/v2'
OUTPUT = ROOT / 'benchmark/cases'
TOPICS = ('cardiology', 'diabetes', 'oncology', 'outliers', 'als-ftd')


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def prose(value):
    """Preserve words while removing extraction newlines from Markdown prose."""
    return ' '.join(str(value).split())


def cell(value):
    return prose(value).replace('|', '&#124;')


def article_link(article_id, articles):
    article = articles[article_id]
    version = article['pmc_version']
    return f"[{article_id}](https://pmc.ncbi.nlm.nih.gov/articles/{article_id}.{version}/)"


def article_list(ids, articles):
    return ', '.join(article_link(aid, articles) for aid in ids) or 'None recorded.'


def dependency_ids(query, short, long):
    dependencies = query.get('dependencies', {})
    return dependencies.get(short, dependencies.get(long, []))


def validate_topic(topic, release, articles, dependencies):
    """Reject broken joins rather than publish misleading case/article relationships."""
    anchors = {a['id']: a for a in release['anchors']}
    if len(anchors) != len(release['anchors']):
        raise ValueError(f'{topic}: duplicate anchor IDs')
    ids = set()
    for query in release['queries']:
        qid = query['id']
        if qid in ids:
            raise ValueError(f'{topic}: duplicate query {qid}')
        ids.add(qid)
        dependency = dependencies[(topic, qid)]
        if (dependency['case_sha256'] != canonical_hash(query) or
                dependency['evidence_sets'] != query['evidence_sets']):
            raise ValueError(f'{topic}/{qid}: dependency map differs from current query')
        if not query.get('reference_answer') and query['answerability']['status'] != 'absent_fact':
            raise ValueError(f'{topic}/{qid}: missing expected response')
        for evidence in query['evidence_sets']:
            for aid in evidence['anchors']:
                articles[anchors[aid]['article_id']]
            for fact_anchors in evidence.get('fact_anchors', {}).values():
                if not set(fact_anchors) <= set(evidence['anchors']):
                    raise ValueError(f'{topic}/{qid}: fact binding outside evidence set')
        for distractor in query.get('related_distractors', []):
            article = articles[distractor['article_id']]
            anchor = anchors[distractor['anchor_id']]
            if anchor['article_id'] != article['article_id']:
                raise ValueError(f'{topic}/{qid}: distractor article/anchor mismatch')
        for short, long in [('required', 'required_articles'), ('alternatives', 'alternative_articles'),
                            ('decoys', 'decoy_articles'), ('overlap_review', 'overlap_articles'),
                            ('negative_evidence', 'negative_articles')]:
            for aid in dependency_ids(query, short, long):
                articles[aid]
        for aid in dependency['overlap_review_articles']:
            articles[aid]
        scope = query['answerability'].get('search_scope', {})
        for aid in scope.get('article_ids', []) if isinstance(scope, dict) else []:
            articles[aid]
    return anchors


def render_topic(topic, release, articles, dependencies):
    anchors = validate_topic(topic, release, articles, dependencies)
    lines = [f'# {topic.title()} evaluation cases', '',
             'Generated from the current combined v2 inputs. Regenerate with',
             '`python render_case_index.py`; do not edit this page by hand.', '',
             '[All topics](README.md) · [Article catalogue](articles.md) ·',
             f'[Authoritative questions](../combined/v2/{topic}/queries.json) ·',
             '[Dependency map](../combined/v2/case_dependencies.json)', '',
             'Expected responses are model-reviewed references, not biomedical expert',
             'certification or observed RAG responses. No new scoring is performed here.', '',
             '## Find a question', '', '| ID | Category | Question |', '| --- | --- | --- |']
    for query in release['queries']:
        lines.append(f"| [{query['id']}](#{query['id']}) | {query['category']} | {cell(query['question'])} |")
    for query in release['queries']:
        qid = query['id']
        dependency = dependencies[(topic, qid)]
        lines += ['', f'## {qid}', '',
                  f"**{query['category']} · revision {query['revision']} · {query['answerability']['status']}**", '',
                  prose(query['question']), '', '**Expected response**', '',
                  prose(query['reference_answer']) if query.get('reference_answer') else
                  'No reference answer is recorded for this missing-fact case. Expected handling: ' +
                  prose(query['answer_rubric']['acceptable_alternatives'])]
        facts = query.get('required_facts', [])
        if facts:
            lines += ['', '**Required claims**', '']
            for fact in facts:
                expected = fact.get('expected_text', fact.get('expected'))
                if expected is None:
                    raise ValueError(f'{topic}/{qid}: missing expected claim')
                lines.append(f"- `{fact['id']}`: {prose(expected)}")
        lines += ['', '**Article roles declared by the question**', '',
                  '- Required: ' + article_list(dependency_ids(query, 'required', 'required_articles'), articles),
                  '- Alternatives: ' + article_list(dependency_ids(query, 'alternatives', 'alternative_articles'), articles),
                  '- Decoys: ' + article_list(dependency_ids(query, 'decoys', 'decoy_articles'), articles)]
        if query['evidence_sets']:
            lines += ['', '**Accepted evidence sets**', '',
                      'Each set is a complete accepted route to the answer. Alternatives are not',
                      'additional mandatory sources. Page numbers refer to the pinned PDF.', '',
                      '| Set | Claim | Article | Passage / PDF page | Anchor |',
                      '| --- | --- | --- | --- | --- |']
            for evidence in query['evidence_sets']:
                bindings = evidence.get('fact_anchors', {})
                for aid in evidence['anchors']:
                    anchor = anchors[aid]
                    claims = [fid for fid, aids in bindings.items() if aid in aids]
                    pages = anchor.get('pages') or [anchor['page']]
                    location = f"{anchor['section']}; p. {', '.join(map(str, pages))}"
                    lines.append(f"| {cell(evidence['id'])} | {cell(', '.join(claims) or 'Set-level evidence')} | {article_link(anchor['article_id'], articles)} | {cell(location)} | `{aid}` |")
        else:
            lines += ['', '**Evidence:** No positive answer-evidence set is defined. See the',
                      'expected refusal and the recorded search scope below.']
        distractors = query.get('related_distractors', [])
        if distractors:
            lines += ['', '**Why the distractors matter**', '']
            for distractor in distractors:
                anchor = anchors[distractor['anchor_id']]
                lines += ['- ' + article_link(distractor['article_id'], articles) +
                          f" — {prose(distractor['plausible_confusion'])}",
                          '  ' + prose(distractor['reason_inapplicable']),
                          f"  Passage: {prose(anchor['section'])}; PDF p. {anchor['page']}; anchor `{anchor['id']}`."]
        rubric = query.get('answer_rubric', {})
        forbidden = rubric.get('forbidden_conflations', [])
        if forbidden:
            lines += ['', '**Response distinctions to preserve**', '']
            lines += ['- ' + prose(item) for item in forbidden]
        scope = query['answerability'].get('search_scope', {})
        premise = query['answerability'].get('offending_premise')
        if premise:
            lines += ['', '**Premise to correct:** ' + prose(premise)]
        if scope:
            lines += ['', '**Missing-fact search scope**', '']
            if isinstance(scope, dict):
                lines += [prose(scope.get('note', scope.get('rationale', 'Recorded scope for this question.'))),
                          '', article_list(scope.get('article_ids', []), articles)]
                if scope.get('searched_terms'):
                    lines += ['', 'Recorded search terms: ' + ', '.join(prose(term) for term in scope['searched_terms'])]
            else:
                lines.append(prose(scope))
        reviewed = dependency['overlap_review_articles']
        if reviewed:
            lines += ['', f'**Overlap review:** {len(reviewed)} other articles were considered; see the',
                      '[recorded dependency map](../combined/v2/case_dependencies.json).',
                      'Review scope does not make every article a distractor or accepted source.']
        lines += ['', '[Back to questions](#find-a-question)']
    return '\n'.join(lines) + '\n'


def generate(release=RELEASE):
    manifest = json.loads((release / 'manifest.json').read_text())
    articles = {a['article_id']: a for a in manifest['articles']}
    if len(articles) != len(manifest['articles']):
        raise ValueError('duplicate article IDs')
    records = json.loads((release / 'case_dependencies.json').read_text())['cases']
    dependencies = {(d['topic'], d['query_id']): d for d in records}
    if len(dependencies) != len(records):
        raise ValueError('duplicate dependency cases')
    outputs = {}
    counts = {}
    categories = Counter()
    seen = set()
    for topic in TOPICS:
        data = json.loads((release / topic / 'queries.json').read_text())
        outputs[topic + '.md'] = render_topic(topic, data, articles, dependencies)
        counts[topic] = len(data['queries'])
        categories.update(q['category'] for q in data['queries'])
        seen.update((topic, q['id']) for q in data['queries'])
    if seen != dependencies.keys():
        raise ValueError('query/dependency coverage differs')
    catalogue = ['# Selected articles', '', 'Generated by `python render_case_index.py` from the current combined v2 manifest.', '',
                 '[Case index](README.md) · [Authoritative manifest](../combined/v2/manifest.json)', '',
                 'Article roles depend on the question; inclusion here does not make an article',
                 'a required source or distractor for every case.', '',
                 '| Article / pinned version | Title | Topics | Selection rationale |', '| --- | --- | --- | --- |']
    for aid, article in sorted(articles.items()):
        catalogue.append(f"| {article_link(aid, articles)} / v{article['pmc_version']} | {cell(article['title'])} | {cell(', '.join(article['topics']))} | {cell(article.get('selection_rationale', 'See manifest.'))} |")
    outputs['articles.md'] = '\n'.join(catalogue) + '\n'
    index = ['# Current benchmark case index', '',
             f"Browse all **{sum(counts.values())} questions across {len(articles)} articles** in the combined v2 benchmark.",
             'Each case links the question and expected response to its required/alternative',
             'articles, accepted passage sets and recorded distractors. Article links open',
             'the pinned public PMC version; passage locations refer to physical PDF pages.', '',
             '| Topic | Questions |', '| --- | ---: |']
    index += [f'| [{topic.title()}]({topic}.md) | {count} |' for topic, count in counts.items()]
    index += ['', '## Case categories', '', '| Category | Questions |', '| --- | ---: |']
    index += [f'| {category} | {count} |' for category, count in sorted(categories.items())]
    index += ['', '## How to review a case', '',
              '1. Read the question, category and expected response.',
              '2. Follow the article links and inspect the named PDF sections/pages.',
              '3. Check required claims against each complete accepted evidence set.',
              '4. For distractors, read the recorded similarity and why the source is inapplicable.',
              '5. Preserve attributed conflicts and scope distinctions; do not invent a reconciliation.', '',
              'Expected answers are LLM-authored and reviewed against the articles. They can',
              'be imperfect; corrections belong in the authoritative benchmark inputs.',
              'This index does not generate responses, judge answers or change gold.', '',
              '[Article catalogue](articles.md) · [Benchmark guide](../README.md) ·',
              '[Source-conflict examples](../../docs/evaluation/source-conflicts.md)', '',
              '## Regenerate', '', 'From the repository root:', '', '```sh',
              'python render_case_index.py', 'python render_case_index.py --check', '```', '',
              'These pages are generated from `benchmark/combined/v2/manifest.json`, the five',
              'topic query files and `case_dependencies.json`. The check fails if the pages',
              'are stale or question/article/evidence joins are broken. It uses no models,',
              'network access or downloaded corpus files. Detailed qualifiers, rubric rules',
              'and exact excerpts remain in the linked authoritative query files.']
    outputs['README.md'] = '\n'.join(index) + '\n'
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated pages differ; write nothing')
    args = parser.parse_args()
    outputs = generate()
    if args.check:
        stale = [name for name, text in outputs.items()
                 if not (OUTPUT / name).is_file() or (OUTPUT / name).read_text() != text]
        if stale:
            parser.error('stale case index: ' + ', '.join(stale))
        print('Case index matches current benchmark inputs.')
    else:
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for name, text in outputs.items():
            (OUTPUT / name).write_text(text, encoding='utf-8')
        print(f'Generated {len(outputs)} case-index pages.')


if __name__ == '__main__':
    main()
