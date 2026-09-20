#!/usr/bin/env python3
"""Fingerprint a frozen release. Integrity only, never electrical approval. Python 3.10+."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

MANIFEST = 'MANIFEST.sha256.json'


def is_link(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & 0x400)


def get_root(path: Path) -> Path:
    if is_link(path) or not path.is_dir():
        raise ValueError('Release root must be an existing real directory, not a link/junction')
    return path.resolve(strict=True)


def safe_name(name: str) -> str:
    if not isinstance(name, str) or not name or '\\' in name or ':' in name:
        raise ValueError('Invalid manifest relative path')
    pure = PurePosixPath(name)
    if pure.is_absolute() or any(part in ('', '.', '..') for part in name.split('/')):
        raise ValueError('Manifest paths must remain inside release root')
    if name == MANIFEST:
        raise ValueError('Manifest must not list itself')
    return name


def inventory(root: Path) -> dict[str, Path]:
    found = {}
    def on_error(error):
        raise error
    for base, dirs, files in os.walk(root, followlinks=False, onerror=on_error):
        for entry in dirs + files:
            item = Path(base) / entry
            if is_link(item):
                raise ValueError(f'Link/reparse point is not allowed: {item.relative_to(root)}')
        for entry in files:
            item = Path(base) / entry
            if not stat.S_ISREG(item.stat().st_mode):
                raise ValueError(f'Non-regular file: {item.relative_to(root)}')
            name = item.relative_to(root).as_posix()
            if name != MANIFEST:
                safe_name(name)
                found[name] = item
    return dict(sorted(found.items()))


def fingerprint(path: Path) -> dict:
    before = path.stat()
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError(f'File changed while hashing: {path.name}')
    return {'bytes': after.st_size, 'sha256': digest.hexdigest()}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def create(root: Path, revision: str, baseline: str) -> dict:
    root = get_root(root)
    if not revision.strip() or not baseline.strip():
        raise ValueError('Revision and baseline must be nonempty')
    if (root / MANIFEST).exists():
        raise ValueError('Manifest already exists; use a new frozen release directory')
    files = inventory(root)
    if not files:
        raise ValueError('Cannot fingerprint an empty release')
    data = {'schema': 1, 'revision': revision, 'baseline_id': baseline,
            'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'scope': 'file-byte-integrity-only',
            'files': {name: fingerprint(path) for name, path in files.items()}}
    with (root / MANIFEST).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return {'action': 'create', 'files': len(files), 'revision': revision,
            'scope': data['scope'], 'manifest': str(root / MANIFEST)}


def verify(root: Path) -> dict:
    root = get_root(root)
    # Inventory first also rejects a manifest which is itself a symlink.
    current = inventory(root)
    data = json.loads((root / MANIFEST).read_text(encoding='utf-8'), object_pairs_hook=unique_object)
    if not isinstance(data, dict) or type(data.get('schema')) is not int or data['schema'] != 1:
        raise ValueError('Unsupported manifest schema')
    if data.get('scope') != 'file-byte-integrity-only':
        raise ValueError('Unexpected manifest scope')
    for field in ('revision', 'baseline_id'):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f'Missing {field}')
    expected = data.get('files')
    if not isinstance(expected, dict) or not expected:
        raise ValueError('Manifest file map must be nonempty')
    for name, details in expected.items():
        safe_name(name)
        if not isinstance(details, dict) or type(details.get('bytes')) is not int or details['bytes'] < 0:
            raise ValueError(f'Invalid size for {name}')
        if not isinstance(details.get('sha256'), str) or not re.fullmatch('[0-9a-f]{64}', details['sha256']):
            raise ValueError(f'Invalid hash for {name}')
    missing = sorted(set(expected) - set(current))
    extra = sorted(set(current) - set(expected))
    changed = [name for name in sorted(set(expected) & set(current))
               if fingerprint(current[name]) != expected[name]]
    if missing or extra or changed:
        raise ValueError(json.dumps({'missing': missing, 'extra': extra, 'changed': changed}, ensure_ascii=False))
    return {'action': 'verify', 'files': len(expected), 'revision': data['revision'],
            'baseline_id': data['baseline_id'], 'byte_integrity': 'PASS',
            'electrical_and_hardware_validation': 'NOT_ASSESSED'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    creator = sub.add_parser('create')
    creator.add_argument('--root', type=Path, required=True)
    creator.add_argument('--revision', required=True)
    creator.add_argument('--baseline', required=True)
    verifier = sub.add_parser('verify')
    verifier.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = create(args.root, args.revision, args.baseline) if args.action == 'create' else verify(args.root)
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
