#!/usr/bin/env python3
"""Exercise release integrity and non-overwriting project initialization without EDA access."""
import argparse
import csv
import json
from pathlib import Path
import tempfile
import unittest

import init_project
import release_manifest as rm

WORKDIR = None


class HelpersTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pcb-skill-check-', dir=WORKDIR)
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'release'
        self.root.mkdir()
        (self.root / 'hardware').mkdir()
        (self.root / 'hardware' / '板框.txt').write_bytes(b'board-revision-A')
        (self.root / 'empty.txt').write_bytes(b'')

    def freeze(self):
        return rm.create(self.root, 'revA', 'baseline-A')

    def rewrite_manifest(self, transform):
        path = self.root / rm.MANIFEST
        data = json.loads(path.read_text(encoding='utf-8'))
        transform(data)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

    def test_roundtrip_unicode_nested_empty(self):
        self.freeze()
        result = rm.verify(self.root)
        self.assertEqual(result['files'], 2)
        self.assertEqual(result['byte_integrity'], 'PASS')
        self.assertEqual(result['electrical_and_hardware_validation'], 'NOT_ASSESSED')

    def test_detect_same_size_tamper(self):
        self.freeze()
        (self.root / 'hardware' / '板框.txt').write_bytes(b'board-revision-B')
        with self.assertRaisesRegex(ValueError, 'changed'):
            rm.verify(self.root)

    def test_detect_missing(self):
        self.freeze()
        (self.root / 'empty.txt').unlink()
        with self.assertRaisesRegex(ValueError, 'missing'):
            rm.verify(self.root)

    def test_detect_extra(self):
        self.freeze()
        (self.root / 'unreviewed.txt').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'extra'):
            rm.verify(self.root)

    def test_no_manifest_overwrite(self):
        self.freeze()
        before = (self.root / rm.MANIFEST).read_bytes()
        with self.assertRaises(ValueError):
            rm.create(self.root, 'revB', 'baseline-B')
        self.assertEqual(before, (self.root / rm.MANIFEST).read_bytes())

    def test_reject_empty_release(self):
        empty = self.base / 'empty'
        empty.mkdir()
        with self.assertRaises(ValueError):
            rm.create(empty, 'revA', 'A')

    def test_reject_path_escape_and_absolute_paths(self):
        self.freeze()
        for name in ('../secret', '/etc/passwd', 'C:/secret', 'a\\..\\secret', 'a/./b'):
            with self.subTest(name=name):
                self.rewrite_manifest(lambda d: d['files'].update({name: {'bytes': 0, 'sha256': '0' * 64}}))
                with self.assertRaises(ValueError):
                    rm.verify(self.root)
                self.rewrite_manifest(lambda d: d['files'].pop(name))

    def test_reject_duplicate_json_key(self):
        self.freeze()
        path = self.root / rm.MANIFEST
        content = path.read_text(encoding='utf-8')
        path.write_text(content.replace('"schema": 1', '"schema": 1, "schema": 1'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            rm.verify(self.root)

    def test_reject_bad_hash_metadata(self):
        self.freeze()
        self.rewrite_manifest(lambda d: d['files']['empty.txt'].update({'sha256': 'not-a-sha'}))
        with self.assertRaisesRegex(ValueError, 'Invalid hash'):
            rm.verify(self.root)

    def test_reject_symlink(self):
        target = self.base / 'external.txt'
        target.write_text('outside', encoding='utf-8')
        try:
            (self.root / 'alias.txt').symlink_to(target)
        except OSError as exc:
            self.skipTest(f'OS does not permit symlink creation: {exc}')
        with self.assertRaisesRegex(ValueError, 'Link'):
            self.freeze()

    def test_initialize_and_refuse_existing(self):
        target = self.base / 'project'
        init_project.create_project(target, '测试传感器板')
        project = (target / 'PROJECT.md').read_text(encoding='utf-8')
        self.assertIn('测试传感器板', project)
        self.assertNotIn('{{', project)
        with (target / 'CHECKS.csv').open(encoding='utf-8', newline='') as stream:
            checks = list(csv.DictReader(stream))
        self.assertTrue(checks)
        self.assertTrue(all(row['status'] == 'NOT_RUN' and None not in row for row in checks))
        with self.assertRaises(ValueError):
            init_project.create_project(target, 'replacement')
        self.assertEqual(project, (target / 'PROJECT.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workdir', type=Path, required=True, help='Existing directory for temporary test data')
    args = parser.parse_args()
    WORKDIR = str(args.workdir.resolve(strict=True))
    unittest.main(argv=['test_helpers.py'], verbosity=2)
