"""Exercise fixed checker execution and fail-closed file-bound evidence in disposable projects."""
import argparse
import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import evidence_binding as binding
import run_bound_check as runner
import workflow_io as io
from test_circuit_checks import snapshot, contract
from test_component_cost import fixture as cost_fixture

WORKDIR = None
REAL_RUN = subprocess.run


class BoundCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=WORKDIR)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        sch = snapshot(); sch['source'] = '测试 fixture source'
        pcb = copy.deepcopy(sch); pcb['kind'] = 'pcb'
        for index, part in enumerate(pcb['components']):
            part.update(body_aabb_mm=[index * 10, 0, index * 10 + 2, 2], side='top', geometry_source='synthetic body drawing')
        for name, value in [('sch.json', sch), ('pcb.json', pcb), ('contract.json', contract()), ('cost.json', cost_fixture())]:
            io.save(self.root / name, value, exclusive=True)
        self.baseline()

    def baseline(self):
        io.save(self.root / 'design-baseline.json', binding.snapshot(self.root, 'P', ['SCH', 'PCB'], 'A', ['sch.json', 'pcb.json', 'cost.json']))

    def run_check(self, mode='connectivity', output='result', **kwargs):
        inputs = {'connectivity': ['sch.json', 'contract.json'], 'compare': ['sch.json', 'pcb.json'], 'geometry': ['pcb.json'], 'cost': ['cost.json']}.get(mode, ['sch.json'])
        args = dict(root=self.root, project='P', baseline='A', check_id='CUSTOM-' + mode, output=output, mode=mode, inputs=inputs,
                    clearance_mm=1 if mode == 'geometry' else None)
        args.update(kwargs)
        return runner.run(**args)

    def test_all_four_real_checkers_and_binding_evaluator(self):
        records = [self.run_check(mode, output=mode) for mode in runner.TOOLS]
        self.assertFalse((self.root / 'check-bindings.json').exists())
        self.assertFalse((self.root / 'CHECKS.csv').exists())
        for record in records:
            self.assertEqual(record['status'], 'PASS')
            self.assertEqual(binding.machine_status(self.root, record['report'], inputs=record['inputs']), 'PASS')
            execution = io.read(self.root / record['evidence'][0]['path'])
            self.assertEqual(execution['inputs_before'], execution['inputs_after'])
            self.assertEqual(execution['tool']['sha256'], execution['tool_sha256_after'])
            self.assertIn('-B', execution['command'])
        io.save(self.root / 'check-bindings.json', {'schema': 1, 'project_id': 'P', 'baseline_id': 'A', 'checks': records})
        rows = [{'id': r['id'], 'stage': 'G2', 'baseline_id': 'A', 'status': 'PASS', 'evidence_path': ';'.join(e['path'] for e in r['evidence'])} for r in records]
        self.assertEqual(binding.evaluate(self.root, 'A', rows, 'G2')['state'], 'BOUND_TO_CURRENT_FILES')

    def test_real_negative_report_is_fail(self):
        value = io.read(self.root / 'contract.json'); value['rules'][0]['kind'] = 'different_nets'
        io.save(self.root / 'contract.json', value)
        record = self.run_check()
        self.assertEqual(record['status'], 'FAIL')
        self.assertEqual(binding.machine_status(self.root, record['report'], inputs=record['inputs']), 'FAIL')

    def test_bad_checker_input_produces_blocked_raw_evidence(self):
        value = io.read(self.root / 'contract.json'); value['rules'] = []
        io.save(self.root / 'contract.json', value)
        record = self.run_check()
        self.assertEqual(record['status'], 'BLOCKED')
        self.assertEqual((self.root / 'result/report.json').read_bytes(), b'')
        self.assertTrue((self.root / 'result/stderr.txt').read_bytes())

    def test_timeout_preserves_partial_output_and_is_blocked(self):
        with patch.object(runner.subprocess, 'run', side_effect=subprocess.TimeoutExpired(['fixed'], 0.1, output=b'{partial', stderr=b'timed out')):
            record = self.run_check(timeout=0.1)
        self.assertEqual(record['status'], 'BLOCKED')
        self.assertEqual((self.root / 'result/report.json').read_bytes(), b'{partial')
        self.assertIn('CHECKER_TIMEOUT', io.read(self.root / 'result/execution.json')['errors'])

    def test_design_and_auxiliary_input_changes_block_pass(self):
        for changed in ('design-baseline.json', 'sch.json', 'contract.json'):
            original = (self.root / changed).read_bytes()
            def mutate(*args, **kwargs):
                result = REAL_RUN(*args, **kwargs)
                with (self.root / changed).open('ab') as stream: stream.write(b' ')
                return result
            with patch.object(runner.subprocess, 'run', side_effect=mutate):
                record = self.run_check(output='changed-' + changed)
            self.assertEqual(record['status'], 'BLOCKED')
            self.assertTrue(any(e.startswith('INPUT_CHANGED') for e in io.read(self.root / ('changed-' + changed) / 'execution.json')['errors']))
            (self.root / changed).write_bytes(original)

    def test_tool_bundle_change_blocks_pass(self):
        real_digest = binding.tool_digest; count = 0
        def changed_digest(name):
            nonlocal count
            count += 1
            return real_digest(name) if count <= 2 else 'changed'
        with patch.object(runner.binding, 'tool_digest', side_effect=changed_digest):
            record = self.run_check()
        self.assertEqual(record['status'], 'BLOCKED')
        self.assertIn('CHECKER_CHANGED', io.read(self.root / 'result/execution.json')['errors'])

    def test_nonzero_exit_cannot_promote_successful_report(self):
        def bad_exit(*args, **kwargs):
            result = REAL_RUN(*args, **kwargs); result.returncode = 1; return result
        with patch.object(runner.subprocess, 'run', side_effect=bad_exit): record = self.run_check()
        self.assertEqual(record['status'], 'BLOCKED')
        self.assertIn('EXIT_REPORT_DISAGREEMENT', io.read(self.root / 'result/execution.json')['errors'])

    def test_launch_failure_and_malformed_success_output_are_blocked(self):
        with patch.object(runner.subprocess, 'run', side_effect=OSError('synthetic launch failure')):
            record = self.run_check(output='launch-error')
        self.assertEqual(record['status'], 'BLOCKED')
        with patch.object(runner.subprocess, 'run', return_value=subprocess.CompletedProcess(['fixed'], 0, b'not JSON', b'')):
            record = self.run_check(output='malformed')
        self.assertEqual(record['status'], 'BLOCKED')
        self.assertEqual((self.root / 'malformed/report.json').read_bytes(), b'not JSON')

    def test_fixed_subprocess_arguments_and_no_shell(self):
        def checked(*args, **kwargs):
            command = args[0]
            self.assertEqual(command[0], sys.executable)
            self.assertEqual(command[1:6], ['-B', '-E', '-s', '-X', 'utf8'])
            self.assertEqual(command[6], str(runner.SCRIPTS / 'check_connectivity.py'))
            self.assertEqual(command[7:], [str(self.root / 'sch.json'), str(self.root / 'contract.json')])
            self.assertFalse(kwargs.get('shell', False))
            self.assertEqual(kwargs['timeout'], 7)
            return REAL_RUN(*args, **kwargs)
        with patch.object(runner.subprocess, 'run', side_effect=checked): record = self.run_check(timeout=7)
        self.assertEqual(record['status'], 'PASS')

    def test_project_baseline_core_ids_and_paths_rejected_before_execution(self):
        core = io.read(runner.SCRIPTS.parent / 'assets/design-check-registry.json')['checks'][0]['id']
        for args in ({'project': 'OTHER'}, {'baseline': 'OLD'}, {'check_id': core}, {'output': '../escape'},
                     {'inputs': ['../sch.json', 'contract.json']}, {'mode': 'arbitrary'}, {'timeout': 0}):
            with patch.object(runner.subprocess, 'run') as launch, self.assertRaises(ValueError): self.run_check(**args)
            launch.assert_not_called()
        self.assertFalse((self.root / 'result').exists())

    def test_unbound_and_mismatched_inputs_rejected(self):
        io.save(self.root / 'other.json', snapshot())
        with self.assertRaises(ValueError): self.run_check(inputs=['other.json', 'contract.json'])
        for key, value in [('baseline_id', 'OLD'), ('project_id', 'OTHER')]:
            data = contract(); data[key] = value; io.save(self.root / 'contract.json', data)
            with self.assertRaises(ValueError): self.run_check()

    def test_existing_output_and_stale_baseline_never_overwritten(self):
        record = self.run_check(); saved = (self.root / 'result/binding.json').read_bytes()
        with self.assertRaises(FileExistsError): self.run_check()
        self.assertEqual((self.root / 'result/binding.json').read_bytes(), saved)
        with (self.root / 'sch.json').open('ab') as stream: stream.write(b' ')
        with self.assertRaises(ValueError): self.run_check(output='stale')
        self.assertFalse((self.root / 'stale').exists())
        with (self.root / 'result/report.json').open('ab') as stream: stream.write(b' ')
        with self.assertRaises(ValueError): binding.machine_status(self.root, record['report'], inputs=record['inputs'])

    def test_cli_plain_arguments_execute_without_shell(self):
        result = REAL_RUN([sys.executable, '-B', str(runner.SCRIPTS / 'run_bound_check.py'), '--root', str(self.root),
                          '--project', 'P', '--baseline', 'A', '--check-id', 'CUSTOM-CLI', '--output', 'cli', '--timeout', '10',
                          'geometry', '--snapshot', 'pcb.json', '--clearance-mm', '1'], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(io.read(self.root / 'cli/binding.json')['status'], 'PASS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--workdir', type=Path, required=True)
    WORKDIR = str(parser.parse_args().workdir.resolve(strict=True))
    unittest.main(argv=[sys.argv[0]], verbosity=2)
