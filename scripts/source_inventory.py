#!/usr/bin/env python3
"""Verify a project-local external board snapshot before treating it as an editable base.

Checks file identity and minimum artifact coverage, not copyright permission,
electrical correctness, EDA import quality, or physical-board operation.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import urlsplit

import workflow_io as io

ROLES = {'schematic', 'pcb', 'license_evidence', 'footprint', 'bom',
         'manufacturing', 'documentation', 'other'}


def check(root, manifest='source-baseline.json'):
    root = io.no_link(root).resolve(strict=True)
    manifest_path = io.no_link(root / manifest).resolve(strict=True)
    if not manifest_path.is_relative_to(root) or not manifest_path.is_file():
        raise ValueError('Manifest must be a project-local regular file')
    data = io.read(manifest_path)
    if not isinstance(data, dict) or type(data.get('schema')) is not int or data['schema'] != 1:
        raise ValueError('source-baseline schema=1 required')
    url = io.text(data.get('source_url'), 'source URL')
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or any(c.isspace() for c in url):
        raise ValueError('Use an exact HTTPS source URL')
    revision = io.text(data.get('revision'), 'source revision')
    if revision.lower() in {'main', 'master', 'latest', 'head'}:
        raise ValueError('Pin a specific source revision, not a moving branch')
    when = io.text(data.get('retrieved_at'), 'retrieval timestamp')
    if datetime.fromisoformat(when.replace('Z', '+00:00')).tzinfo is None:
        raise ValueError('Retrieval timestamp needs timezone')
    kind = data.get('kind')
    if kind not in {'editable_board', 'reference_only'}:
        raise ValueError('kind must be editable_board or reference_only')
    files = data.get('files')
    if not isinstance(files, list) or not files:
        raise ValueError('List the downloaded source files')
    seen, roles = set(), set()
    for item in files:
        if not isinstance(item, dict) or set(item) != {'path', 'role', 'sha256'}:
            raise ValueError('Every source file needs path, role and sha256')
        name = item['path']
        if not isinstance(name, str) or '\\' in name or ':' in name or not name or \
                PurePosixPath(name).is_absolute() or any(p in {'', '.', '..'} for p in name.split('/')):
            raise ValueError('Source file path must stay inside the project')
        if name in seen:
            raise ValueError('Duplicate source file: ' + name)
        seen.add(name)
        role = item['role']
        if role not in ROLES:
            raise ValueError('Unknown source file role')
        roles.add(role)
        expected = item['sha256']
        if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-f]{64}', expected):
            raise ValueError('Invalid source file SHA-256')
        path = io.no_link(root / name).resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size == 0:
            raise ValueError('Source file must be a nonempty regular project-local file: ' + name)
        if io.file_hash(path) != expected:
            raise ValueError('Source file changed since inventory: ' + name)
    if 'license_evidence' not in roles:
        raise ValueError('Record local license evidence for the actual board files')
    if kind == 'editable_board' and not {'schematic', 'pcb'} <= roles:
        raise ValueError('Editable board baseline needs native schematic and PCB files')
    return {'scope': 'source-file-integrity-only', 'state': 'EDITABLE_SOURCE_INVENTORIED'
            if kind == 'editable_board' else 'REFERENCE_ONLY_INVENTORIED',
            'source_url': url, 'revision': revision, 'file_count': len(files),
            'license_permission': 'REQUIRES_ARTIFACT_AND_OUTPUT_REVIEW',
            'native_import_and_pin_net_review': 'NOT_ASSESSED',
            'hardware_validation': 'NOT_ASSESSED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--manifest', default='source-baseline.json')
    args = parser.parse_args()
    try:
        result = check(args.root, args.manifest)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, 'ERROR: ' + str(exc) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
