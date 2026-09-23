"""External-design admission checks with nearby invalid cases."""
import tempfile
import unittest
from pathlib import Path

import source_inventory as source
import workflow_io as io


class SourceInventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data = {'schema': 1, 'source_url': 'https://example.org/board',
                     'revision': 'a1234567', 'retrieved_at': '2026-09-23T12:00:00Z',
                     'kind': 'editable_board', 'files': []}
        for name, role in (('source/design.kicad_sch', 'schematic'),
                           ('source/design.kicad_pcb', 'pcb'),
                           ('source/LICENSE', 'license_evidence')):
            path = self.root / name
            path.parent.mkdir(exist_ok=True)
            path.write_text(name, encoding='utf-8')
            self.data['files'].append({'path': name, 'role': role, 'sha256': io.file_hash(path)})
        self.save()

    def save(self):
        io.save(self.root / 'source-baseline.json', self.data)

    def test_editable_source_does_not_become_a_licensed_or_tested_board(self):
        result = source.check(self.root)
        self.assertEqual(result['state'], 'EDITABLE_SOURCE_INVENTORIED')
        self.assertEqual(result['license_permission'], 'REQUIRES_ARTIFACT_AND_OUTPUT_REVIEW')
        self.assertEqual(result['hardware_validation'], 'NOT_ASSESSED')

    def test_reference_only_cannot_be_misrepresented_as_editable_board(self):
        self.data['files'] = [f for f in self.data['files'] if f['role'] != 'pcb']
        self.save()
        with self.assertRaisesRegex(ValueError, 'native schematic and PCB'):
            source.check(self.root)
        self.data['kind'] = 'reference_only'
        self.save()
        self.assertEqual(source.check(self.root)['state'], 'REFERENCE_ONLY_INVENTORIED')

    def test_changed_file_or_absent_license_evidence_blocks_inventory(self):
        (self.root / 'source/design.kicad_pcb').write_text('replaced', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'changed'):
            source.check(self.root)
        self.data['files'] = [f for f in self.data['files'] if f['role'] != 'pcb']
        self.data['kind'] = 'reference_only'
        self.data['files'] = [f for f in self.data['files'] if f['role'] != 'license_evidence']
        self.save()
        with self.assertRaisesRegex(ValueError, 'license evidence'):
            source.check(self.root)

    def test_moving_revision_and_path_escape_rejected(self):
        self.data['revision'] = 'main'
        self.save()
        with self.assertRaisesRegex(ValueError, 'specific source revision'):
            source.check(self.root)
        self.data['revision'] = 'a1234567'
        self.data['files'][0]['path'] = '../outside.kicad_sch'
        self.save()
        with self.assertRaisesRegex(ValueError, 'inside the project'):
            source.check(self.root)

    def test_incomplete_source_url_rejected(self):
        self.data['source_url'] = 'https://'
        self.save()
        with self.assertRaisesRegex(ValueError, 'HTTPS source URL'):
            source.check(self.root)


if __name__ == '__main__':
    unittest.main()
