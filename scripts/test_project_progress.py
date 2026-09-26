"""User journey checks: a fresh project, pending choice, stale record and completed fixture."""
import copy
import tempfile
import unittest
from pathlib import Path

import check_evidence
import init_project
import project_progress as progress
import workflow_io as io
from test_evidence_fixture import prepare, write_rows


class ProgressJourneyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project'

    def prepare_through(self, through):
        """Extend the real G5 fixture with synthetic, separately bound physical records."""
        self.root.mkdir(exist_ok=True)
        rows = prepare(self.root)
        bindings = io.read(self.root / 'check-bindings.json')
        registry = io.read(Path(check_evidence.__file__).resolve().parents[1]
                           / 'assets/design-check-registry.json')
        for gate in registry['checks']:
            if not 6 <= int(gate['stage'][1:]) <= int(through[1:]):
                continue
            name = 'synthetic-' + gate['id'] + '.txt'
            (self.root / name).write_text('Synthetic record only; no actual board tested.', encoding='utf-8')
            row = dict(rows[0])
            row.update(id=gate['id'], stage=gate['stage'], applicability=gate['applicability'],
                       actual='synthetic observation', board_id='synthetic-board-A',
                       firmware_id='synthetic-firmware-A', evidence_path=name)
            rows.append(row)
            binding = copy.deepcopy(bindings['checks'][0])
            binding.update(id=gate['id'], evidence=[{'path': name, 'sha256': io.file_hash(self.root / name)}])
            bindings['checks'].append(binding)
        write_rows(self.root, rows)
        io.save(self.root / 'check-bindings.json', bindings)
        return rows

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

    def test_complete_g8_and_g9_records_keep_fabrication_separate_from_physical_claims(self):
        for through in ('G8', 'G9'):
            with self.subTest(through=through):
                rows = self.prepare_through(through)
                result = progress.snapshot(self.root, 'A', through=through)
                self.assertEqual(result['state'], 'RECORDS_FILLED')
                self.assertEqual(result['stage'], through)
                self.assertEqual(result['selected_checks'], len(rows))
                self.assertEqual(result['unfinished_checks'], 0)
                self.assertEqual(result['record_issues'], 0)
                self.assertEqual(result['first_record_issues'], [])
                self.assertTrue(result['fabrication_evidence_complete'])
                self.assertEqual(result['physical_board_test'], 'NOT_ASSESSED')

    def test_filled_g8_rows_require_complete_physical_evidence_bindings(self):
        for defect in ('missing_binding', 'empty_evidence', 'changed_evidence'):
            with self.subTest(defect=defect):
                self.prepare_through('G8')
                bindings = io.read(self.root / 'check-bindings.json')
                entry = next(b for b in bindings['checks'] if b['id'] == 'POWER-CORNERS')
                if defect == 'missing_binding':
                    bindings['checks'].remove(entry)
                    expected = 'Missing design binding: POWER-CORNERS'
                elif defect == 'empty_evidence':
                    entry['evidence'] = []
                    expected = 'Bound inputs and evidence required: POWER-CORNERS'
                else:
                    (self.root / entry['evidence'][0]['path']).write_text('Changed synthetic observation.', encoding='utf-8')
                    expected = 'File changed: synthetic-POWER-CORNERS.txt'
                io.save(self.root / 'check-bindings.json', bindings)
                # A populated CSV and nonempty evidence files pass the shallow audit;
                # the later-stage design-gate audit must still reject their binding.
                self.assertTrue(check_evidence.audit(self.root, 'A', through='G8')['records_complete'])
                result = progress.snapshot(self.root, 'A', through='G8')
                self.assertEqual(result['state'], 'IN_PROGRESS')
                self.assertEqual(result['unfinished_checks'], 0)
                self.assertEqual(result['record_issues'], 1)
                self.assertIn(expected, result['first_record_issues'][0])
                self.assertTrue(result['fabrication_evidence_complete'])
                self.assertEqual(result['next_owner'], 'agent')

    def test_missing_or_empty_physical_evidence_does_not_invalidate_complete_fabrication(self):
        for defect in ('missing', 'empty'):
            with self.subTest(defect=defect):
                self.prepare_through('G8')
                evidence = self.root / 'synthetic-POWER-CORNERS.txt'
                if defect == 'missing':
                    evidence.unlink()
                else:
                    evidence.write_text('', encoding='utf-8')
                result = progress.snapshot(self.root, 'A', through='G8')
                self.assertEqual(result['state'], 'IN_PROGRESS')
                self.assertEqual(result['unfinished_checks'], 0)
                self.assertEqual(result['record_issues'], 1)
                self.assertIn('evidence must be a nonempty project-local file', result['first_record_issues'][0])
                self.assertIn(evidence.name, result['first_record_issues'][0])
                self.assertTrue(result['fabrication_evidence_complete'])

    def test_deleting_one_g8_registry_row_leaves_a_functional_test_pending(self):
        rows = self.prepare_through('G8')
        write_rows(self.root, [row for row in rows if row['id'] != 'POWER-CORNERS'])
        result = progress.snapshot(self.root, 'A', through='G8')
        self.assertEqual(result['state'], 'IN_PROGRESS')
        self.assertEqual(result['stage'], 'G8')
        self.assertEqual(result['unfinished_checks'], 1)
        self.assertEqual(result['record_issues'], 0)
        self.assertIn('功能', result['next_step'])
        self.assertTrue(result['fabrication_evidence_complete'])


if __name__ == '__main__':
    unittest.main()
