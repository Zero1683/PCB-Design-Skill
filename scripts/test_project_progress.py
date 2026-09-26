"""User journey checks: a fresh project, pending choice, stale record and completed fixture."""
import tempfile
import unittest
from pathlib import Path

import init_project
import project_progress as progress
import workflow_io as io
from test_evidence_fixture import prepare, write_rows


class ProgressJourneyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project'

    def test_fresh_project_does_not_claim_completion_or_ask_for_a_baseline(self):
        init_project.create_project(self.root, 'Tiny keyboard', 'zh')
        result = progress.snapshot(self.root, 'UNSET')
        self.assertEqual(result['next_owner'], 'agent')
        self.assertFalse(result['fabrication_evidence_complete'])
        intake = io.read(self.root / 'intake.json')
        intake['baseline_id'] = 'RevA'
        io.save(self.root / 'intake.json', intake)
        result = progress.snapshot(self.root, 'RevA')
        self.assertEqual(result['next_owner'], 'user')
        self.assertIn('用途', result['next_step'])
        self.assertFalse(result['fabrication_evidence_complete'])

    def test_accepted_plan_does_not_hide_stale_evidence(self):
        self.root.mkdir()
        prepare(self.root)
        ready = progress.snapshot(self.root, 'A')
        self.assertTrue(ready['fabrication_evidence_complete'])
        (self.root / 'evidence.txt').unlink()
        stale = progress.snapshot(self.root, 'A')
        self.assertEqual(stale['next_owner'], 'agent')
        self.assertGreater(stale['record_issues'], 0)
        self.assertFalse(stale['fabrication_evidence_complete'])

    def test_rejected_plan_never_becomes_a_user_approval(self):
        self.root.mkdir()
        prepare(self.root)
        intake = io.read(self.root / 'intake.json')
        intake['decision']['status'] = 'rejected'
        io.save(self.root / 'intake.json', intake)
        result = progress.snapshot(self.root, 'A')
        self.assertEqual(result['next_owner'], 'agent')
        self.assertFalse(result['fabrication_evidence_complete'])

    def test_agent_prepares_the_plan_before_asking_user_to_review_it(self):
        self.root.mkdir()
        prepare(self.root)
        intake = io.read(self.root / 'intake.json')
        intake['proposal'] = intake['decision'] = None
        io.save(self.root / 'intake.json', intake)
        result = progress.snapshot(self.root, 'A')
        self.assertEqual(result['next_owner'], 'agent')
        self.assertIn('预算方案', result['next_step'])
        self.assertFalse(result['fabrication_evidence_complete'])

    def test_all_rows_filled_but_source_binding_stale_needs_agent_repair(self):
        self.root.mkdir()
        prepare(self.root)
        (self.root / 'native.json').write_text('{"synthetic":"changed"}', encoding='utf-8')
        result = progress.snapshot(self.root, 'A')
        self.assertEqual(result['next_owner'], 'agent')
        self.assertGreater(result['record_issues'], 0)
        self.assertEqual(result['state'], 'IN_PROGRESS')
        self.assertFalse(result['fabrication_evidence_complete'])

    def test_unfinished_stage_is_explained_without_raw_check_name(self):
        self.root.mkdir()
        rows = prepare(self.root)
        target = next(row for row in rows if row['stage'] == 'G2')
        target['status'] = 'NOT_RUN'
        write_rows(self.root, rows)
        result = progress.snapshot(self.root, 'A')
        self.assertEqual(result['next_owner'], 'agent')
        self.assertIn('原理图', result['next_step'])
        self.assertNotIn('synthetic', result['next_step'])

    def test_g8_navigation_does_not_skip_missing_physical_stages(self):
        self.root.mkdir()
        prepare(self.root)  # Complete synthetic G0-G5 records, no G6-G8 observations.
        result = progress.snapshot(self.root, 'A', through='G8')
        self.assertEqual(result['state'], 'IN_PROGRESS')
        self.assertEqual(result['stage'], 'G6')
        self.assertIn('焊接', result['next_step'])
        self.assertGreater(result['unfinished_checks'], 0)
        self.assertTrue(result['fabrication_evidence_complete'])


if __name__ == '__main__':
    unittest.main()
