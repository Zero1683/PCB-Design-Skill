import copy
import tempfile
import unittest
from pathlib import Path
import intake_review as ir
import workflow_io as io
import check_evidence as ce
from test_evidence_fixture import prepare, prepare_intake


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'evidence.txt').write_text('Synthetic fixture, not a user conversation.', encoding='utf8')
        self.data = prepare_intake(self.root)

    def review(self): return ir.evaluate(self.root, self.data, 'A')

    def test_confirmed_plan(self):
        self.assertTrue(self.review()['detailed_design_allowed'])

    def test_unknown_and_proposed_are_not_confirmed_by_silence(self):
        for state in ('unknown', 'proposed'):
            self.data['topics']['board_size']['state'] = state
            self.data['proposal'] = self.data['decision'] = None
            r = self.review()
            self.assertFalse(r['detailed_design_allowed'])
            self.assertIn('board_size', r['pending_topics'])

    def test_not_knowing_size_can_be_resolved_by_accepting_concrete_plan(self):
        self.data['topics']['board_size']['state'] = 'unknown'
        self.data['proposal']['topics_digest'] = io.digest(self.data['topics'])
        self.data['decision']['proposal_digest'] = io.digest(self.data['proposal'])
        self.assertTrue(self.review()['detailed_design_allowed'])

    def test_delegation_never_resolves_unanswered_topics(self):
        self.data['topics']['board_size']['state'] = 'unknown'
        self.data['proposal']['topics_digest'] = io.digest(self.data['topics'])
        self.data['decision'].update(status='delegated', proposal_digest=io.digest(self.data['proposal']))
        self.assertFalse(self.review()['detailed_design_allowed'])

    def test_explicit_delegation_allowed(self):
        self.data['topics']['board_size']['state'] = 'delegated'
        self.data['proposal']['topics_digest'] = io.digest(self.data['topics'])
        self.data['decision'].update(status='delegated', proposal_digest=io.digest(self.data['proposal']))
        self.assertTrue(self.review()['detailed_design_allowed'])

    def test_changed_carrier_invalidates_plan(self):
        self.data['topics']['carrier']['value'] = 'Different enclosure'
        with self.assertRaisesRegex(ValueError, 'Topics changed'): self.review()

    def test_changed_dimension_invalidates_decision(self):
        self.data['proposal']['assembly_envelope_mm']['board_length'] = 80
        with self.assertRaisesRegex(ValueError, 'Proposal changed'): self.review()

    def test_missing_topic_and_zero_height(self):
        original = copy.deepcopy(self.data)
        del self.data['topics']['assembly']
        with self.assertRaises(ValueError): self.review()
        self.data = original
        self.data['proposal']['assembly_envelope_mm']['assembled_height'] = 0
        with self.assertRaises(ValueError): self.review()

    def test_rejected_and_preexisting_decision(self):
        self.data['decision']['status'] = 'rejected'
        self.assertFalse(self.review()['detailed_design_allowed'])
        self.data['decision']['recorded_at'] = '2026-09-21T00:00:00Z'
        with self.assertRaises(ValueError): self.review()

    def test_changed_source_and_cross_baseline(self):
        with self.assertRaises(ValueError): ir.evaluate(self.root, self.data, 'B')
        (self.root/'evidence.txt').write_text('Changed', encoding='utf8')
        with self.assertRaises(ValueError): self.review()

    def test_legacy_missing_intake_does_not_pass_final_gate(self):
        prepare(self.root)
        (self.root/'intake.json').unlink()
        result = ce.audit(self.root, 'A', design_gates=True)
        self.assertFalse(result['records_complete'])
        self.assertTrue(any('Intake review' in error for error in result['record_errors']))

    def test_wrong_project_and_malformed_records(self):
        prepare(self.root)
        self.data['project_id'] = 'another'
        io.save(self.root/'intake.json', self.data)
        self.assertFalse(ce.audit(self.root, 'A', design_gates=True)['records_complete'])
        for bad in ([], {'schema': True}, None):
            with self.assertRaises(ValueError): ir.evaluate(self.root, bad, 'A')


if __name__ == '__main__': unittest.main()
