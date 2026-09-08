import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('importer', Path(__file__).with_name('import-resources.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
ROOT = Path(__file__).resolve().parent.parent / 'public/resources'


class ImportTests(unittest.TestCase):
    def test_all_original_formats_and_identities(self):
        for project in m.source_input()['projects']:
            for file in project['files']:
                raw = (ROOT / project['id'] / file['path']).read_bytes()
                m.check_body(file, raw)
                m.inspect_format(file, raw)
                with self.assertRaises(ValueError):
                    m.check_body(file, raw + b'changed')

    def test_svg_active_external_and_missing_reference_refused(self):
        samples = ['<script/>', '<foreignObject/>', '<image href="https://example.com/a.png"/>',
                   '<path onclick="alert(1)"/>', '<style>.x{fill:url(https://example.com/)}</style>',
                   '<style>.x{fill:url(#missing)}</style>', '<g xmlns="https://example.com"/>',
                   '<path id="a"/><path id="a"/>', '<g xml:base="https://example.com"/>',
                   '<style>.x{width:expression(alert(1))}</style>']
        for sample in samples:
            with self.assertRaises(ValueError):
                m.inspect_format({'path': 'test.svg'}, ('<svg xmlns="http://www.w3.org/2000/svg">' + sample + '</svg>').encode())

    def test_missing_dependency_and_unsafe_output_refused(self):
        with self.assertRaisesRegex(ValueError, 'Missing local dependency'):
            m.dependencies({'files': [{'path': 'a.md'}]}, {'a.md': b'[image](missing.png)'})
        for path in ['../secret', '/root', 'a/../b', 'a\\b']:
            with self.assertRaises(ValueError):
                m.safe_path(path)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'keep').write_bytes(b'original')
            with self.assertRaisesRegex(ValueError, 'nonempty'):
                m.write_new(root, {'keep': b'changed'})
            self.assertEqual((root / 'keep').read_bytes(), b'original')

    def test_reassembly_and_retained_snapshots_identical(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'assembled'
            m.assemble(ROOT, output, ROOT)
            for source in ROOT.rglob('*'):
                if source.is_file():
                    self.assertEqual(source.read_bytes(), (output / source.relative_to(ROOT)).read_bytes())


if __name__ == '__main__':
    unittest.main()
