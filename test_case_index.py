"""Offline checks against misleading case-index article and evidence relationships."""
from copy import deepcopy
import unittest

from tools.evaluation.render_case_index import canonical_hash, render_topic


class CaseIndexRelationshipTests(unittest.TestCase):
    def setUp(self):
        self.articles = {
            aid: {'article_id': aid, 'pmc_version': 1}
            for aid in ['PMC100001', 'PMC100002', 'PMC100003']
        }
        self.release = {
            'anchors': [
                {'id': 'some_primary', 'article_id': 'PMC100001', 'page': 2,
                 'section': 'Results: synthetic trial'},
                {'id': 'some_alternative', 'article_id': 'PMC100002', 'page': 3,
                 'section': 'Table 2: synthetic replication'},
                {'id': 'some_decoy', 'article_id': 'PMC100003', 'page': 4,
                 'section': 'Results: different test population'},
            ],
            'queries': [{
                'id': 'test001', 'revision': 1, 'category': 'cross_doc_distractor',
                'question': 'Which synthetic cohort reported an outcome of 7?',
                'reference_answer': 'The synthetic trial reported 7 at six months.',
                'answerability': {'status': 'answerable'},
                'required_facts': [{'id': 'f1', 'expected_text': '7 at six months'}],
                'evidence_sets': [
                    {'id': 'primary', 'anchors': ['some_primary'],
                     'fact_anchors': {'f1': ['some_primary']}},
                    {'id': 'alternative', 'anchors': ['some_alternative'],
                     'fact_anchors': {'f1': ['some_alternative']}},
                ],
                'related_distractors': [{
                    'article_id': 'PMC100003', 'anchor_id': 'some_decoy',
                    'plausible_confusion': 'Both test reports discuss the same synthetic endpoint.',
                    'reason_inapplicable': 'The decoy measures a different test population.'}],
                'answer_rubric': {'forbidden_conflations': ['Do not substitute the decoy population.']},
                'dependencies': {'required': ['PMC100001'], 'alternatives': ['PMC100002'],
                                 'decoys': ['PMC100003']},
            }],
        }
        self.refresh_dependencies()

    def refresh_dependencies(self):
        query = self.release['queries'][0]
        self.dependencies = {('some-topic', query['id']): {
            'case_sha256': canonical_hash(query),
            'evidence_sets': deepcopy(query['evidence_sets']),
            'overlap_review_articles': ['PMC100003'],
        }}

    def render(self):
        return render_topic('some-topic', self.release, self.articles, self.dependencies)

    def test_alternative_routes_and_distractor_reason_are_preserved(self):
        text = self.render()
        self.assertIn('| primary | f1 | [PMC100001]', text)
        self.assertIn('| alternative | f1 | [PMC100002]', text)
        self.assertIn('Alternatives are not\nadditional mandatory sources.', text)
        self.assertIn('https://pmc.ncbi.nlm.nih.gov/articles/PMC100003.1/', text)
        self.assertIn('The decoy measures a different test population.', text)
        self.assertIn('PDF p. 4', text)
        self.assertIn('Review scope does not make every article a distractor', text)

    def test_stale_dependency_join_is_rejected(self):
        self.release['queries'][0]['reference_answer'] = 'A corrected synthetic claim.'
        with self.assertRaisesRegex(ValueError, 'dependency map differs'):
            self.render()

    def test_distractor_anchor_cannot_be_attributed_to_another_article(self):
        self.release['queries'][0]['related_distractors'][0]['article_id'] = 'PMC100002'
        self.refresh_dependencies()
        with self.assertRaisesRegex(ValueError, 'distractor article/anchor mismatch'):
            self.render()

    def test_fact_binding_cannot_escape_its_accepted_set(self):
        self.release['queries'][0]['evidence_sets'][0]['fact_anchors']['f1'] = ['some_decoy']
        self.refresh_dependencies()
        with self.assertRaisesRegex(ValueError, 'fact binding outside evidence set'):
            self.render()

    def test_missing_fact_uses_recorded_handling_without_inventing_answer_evidence(self):
        query = self.release['queries'][0]
        query.update(category='unanswerable', reference_answer=None, required_facts=[],
                     evidence_sets=[], related_distractors=[], dependencies={})
        query['answerability'] = {'status': 'absent_fact', 'search_scope': {
            'article_ids': ['PMC100001'], 'rationale': 'The test source does not report this number.'}}
        query['answer_rubric'] = {'acceptable_alternatives': 'Explain the missing number without inventing one.'}
        self.refresh_dependencies()
        text = self.render()
        self.assertIn('No reference answer is recorded', text)
        self.assertIn('Explain the missing number without inventing one.', text)
        self.assertIn('The test source does not report this number.', text)
        self.assertNotIn('**Accepted evidence sets**', text)

    def test_unknown_source_is_not_silently_omitted(self):
        del self.articles['PMC100001']
        with self.assertRaises(KeyError):
            self.render()


if __name__ == '__main__':
    unittest.main()
