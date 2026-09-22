#!/usr/bin/env python3
"""Run a fixed read-only checker and save file-bound evidence, not cryptographic execution proof."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import evidence_binding as binding
from report_provenance import identity
import workflow_io as io

SCRIPTS = Path(__file__).resolve().parent
TOOLS = {'connectivity': 'check_connectivity.py', 'compare': 'audit_design.py',
         'geometry': 'audit_design.py', 'cost': 'component_cost.py'}


def relative(name):
    io.text(name, 'project-relative path')
    if Path(name).is_absolute() or '..' in Path(name).parts or ':' in name or '\\' in name:
        raise ValueError('Use a project-relative path with forward slashes')
    return name


def run(root, project, baseline, check_id, output, mode, inputs, timeout=60, clearance_mm=None):
    root = io.no_link(root).resolve(strict=True)
    io.text(project, 'project'); io.text(check_id, 'check ID')
    if check_id != check_id.strip(): raise ValueError('Check ID cannot have surrounding whitespace')
    registry = io.read(SCRIPTS.parent / 'assets/design-check-registry.json')
    if check_id in {item['id'] for item in registry['checks']}:
        raise ValueError('Builtin gates need composite review; use a subordinate machine check ID')
    if mode not in TOOLS: raise ValueError('Unsupported checker mode')
    io.finite(timeout, 'timeout')
    if timeout <= 0: raise ValueError('Timeout must be positive')
    if not isinstance(inputs, list) or len(inputs) != (2 if mode in ('connectivity', 'compare') else 1):
        raise ValueError('Wrong checker input count')
    paths = [binding.local(root, relative(name)) for name in inputs]
    baseline_path = binding.local(root, 'design-baseline.json')
    baseline_hash = io.file_hash(baseline_path)
    design = binding.design(root, baseline)
    if design['project_id'] != project: raise ValueError('Project identity mismatch')
    design_names = {entry['path'] for entry in design['inputs']}
    primary = inputs[:1] if mode == 'connectivity' else inputs
    if any(name not in design_names for name in primary):
        raise ValueError('Checker design inputs must belong to the current design baseline')
    names = sorted(design_names | set(inputs) | {'design-baseline.json'})
    before = [{'path': name, 'sha256': io.file_hash(binding.local(root, name))} for name in names]
    if next(item['sha256'] for item in before if item['path'] == 'design-baseline.json') != baseline_hash:
        raise ValueError('Design baseline changed during preparation')
    for entry in design['inputs']:
        if next(item['sha256'] for item in before if item['path'] == entry['path']) != entry['sha256']:
            raise ValueError('Design input changed during preparation')
    for path in paths:
        data = io.read(path)
        identity(data, design)
    tool = {'name': TOOLS[mode], 'sha256': binding.tool_digest(TOOLS[mode])}
    command = [sys.executable, '-B', '-E', '-s', '-X', 'utf8', str(SCRIPTS / tool['name'])]
    if mode == 'connectivity': command += [str(path) for path in paths]
    elif mode == 'compare': command += ['compare', *map(str, paths)]
    elif mode == 'geometry':
        io.finite(clearance_mm, 'clearance_mm')
        if clearance_mm < 0: raise ValueError('Clearance must be nonnegative')
        command += ['geometry', str(paths[0]), '--clearance-mm', str(clearance_mm)]
    else: command += ['--input', str(paths[0])]
    if mode != 'geometry' and clearance_mm is not None: raise ValueError('Clearance is only valid for geometry')
    destination = io.no_link(root / relative(output))
    if not destination.resolve().is_relative_to(root): raise ValueError('Output must stay inside project')
    # Verify the same bytes immediately before launch, then reserve a never-overwritten output directory.
    for entry in before: binding.reference(root, entry)
    if binding.tool_digest(tool['name']) != tool['sha256']: raise ValueError('Checker changed before launch')
    destination.mkdir(exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    errors, stdout, stderr, returncode = [], b'', b'', None
    try:
        result = subprocess.run(command, cwd=SCRIPTS, capture_output=True, timeout=timeout, check=False)
        stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr = exc.stdout or b'', exc.stderr or b''
        errors.append('CHECKER_TIMEOUT')
    except OSError as exc:
        errors.append('CHECKER_LAUNCH_FAILED: ' + str(exc))
    after = []
    for entry in before:
        try:
            current = {'path': entry['path'], 'sha256': io.file_hash(binding.local(root, entry['path']))}
            if current != entry: errors.append('INPUT_CHANGED: ' + entry['path'])
        except (OSError, ValueError) as exc:
            current = {'path': entry['path'], 'sha256': None}
            errors.append('INPUT_UNAVAILABLE: ' + entry['path'] + ': ' + str(exc))
        after.append(current)
    try:
        tool_after = binding.tool_digest(tool['name'])
        if tool_after != tool['sha256']: errors.append('CHECKER_CHANGED')
    except (OSError, ValueError) as exc:
        tool_after = None; errors.append('CHECKER_UNAVAILABLE: ' + str(exc))
    # Preserve exact bytes, including partial output on timeout or invalid JSON.
    for name, payload in (('report.json', stdout), ('stderr.txt', stderr)):
        with io.no_link(destination / name).open('xb') as stream: stream.write(payload)
    def ref(path): return {'path': path.relative_to(root).as_posix(), 'sha256': io.file_hash(path)}
    report = {'tool': tool, 'output': ref(destination / 'report.json')}
    observed_status = None
    if stdout:
        try:
            payload = io.read(destination / 'report.json')
            if not isinstance(payload, dict) or payload.get('baseline_id') != baseline:
                raise ValueError('Checker output baseline mismatch')
            observed_status = binding.machine_status(root, report, design, before)
        except (ValueError, KeyError, TypeError, OSError) as exc:
            errors.append('INVALID_REPORT: ' + str(exc))
    else: errors.append('EMPTY_REPORT')
    if returncode not in (0, 1): errors.append('CHECKER_EXIT: ' + str(returncode))
    elif (returncode == 0) != (observed_status == 'PASS'):
        errors.append('EXIT_REPORT_DISAGREEMENT')
    status = 'BLOCKED' if errors else observed_status
    finished = datetime.now(timezone.utc).isoformat()
    execution = {'schema': 1, 'project_id': project, 'baseline_id': baseline, 'id': check_id,
                 'mode': mode, 'command': command, 'started_at': started, 'finished_at': finished,
                 'timeout_seconds': timeout, 'returncode': returncode, 'status': status,
                 'inputs_before': before, 'inputs_after': after, 'tool': tool,
                 'tool_sha256_after': tool_after, 'errors': errors,
                 'scope': 'Local checker invocation and file hashes; not cryptographic execution proof; unsaved EDA state not assessed'}
    io.save(destination / 'execution.json', execution, exclusive=True)
    evidence = [ref(destination / 'execution.json')]
    if stdout: evidence.append(report['output'])
    if stderr: evidence.append(ref(destination / 'stderr.txt'))
    record = {'id': check_id, 'mode': 'machine', 'project_id': project, 'baseline_id': baseline,
              'design_digest': io.digest(design), 'status': status, 'checked_at': finished,
              'method': 'run_bound_check.py fixed ' + mode + ' checker; see execution.json for arguments and scope',
              'inputs': before, 'evidence': evidence, 'report': report,
              'execution_authenticity': 'NOT_CRYPTOGRAPHICALLY_ATTESTED'}
    io.save(destination / 'binding.json', record, exclusive=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--project', required=True); parser.add_argument('--baseline', required=True)
    parser.add_argument('--check-id', required=True); parser.add_argument('--output', required=True)
    parser.add_argument('--timeout', type=float, default=60)
    modes = parser.add_subparsers(dest='mode', required=True)
    conn = modes.add_parser('connectivity'); conn.add_argument('--snapshot', required=True); conn.add_argument('--contract', required=True)
    comp = modes.add_parser('compare'); comp.add_argument('--left', required=True); comp.add_argument('--right', required=True)
    geom = modes.add_parser('geometry'); geom.add_argument('--snapshot', required=True); geom.add_argument('--clearance-mm', type=float, required=True)
    cost = modes.add_parser('cost'); cost.add_argument('--input', required=True)
    args = parser.parse_args()
    inputs = [args.snapshot, args.contract] if args.mode == 'connectivity' else [args.left, args.right] if args.mode == 'compare' else [args.snapshot] if args.mode == 'geometry' else [args.input]
    try:
        record = run(args.root, args.project, args.baseline, args.check_id, args.output, args.mode, inputs,
                     args.timeout, getattr(args, 'clearance_mm', None))
    except (ValueError, KeyError, TypeError, OSError) as exc: parser.exit(2, 'ERROR: ' + str(exc) + '\n')
    print(io.encoded({'status': record['status'], 'binding': args.output + '/binding.json'}).decode('utf-8'))
    return 0 if record['status'] == 'PASS' else 1


if __name__ == '__main__': raise SystemExit(main())
