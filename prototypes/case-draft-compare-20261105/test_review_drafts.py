import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import compare
import review_drafts
import make_portable

ROOT = Path(__file__).resolve().parent


class HumanReviewEntryTests(unittest.TestCase):
    def fixtures(self, directory):
        a, b = Path(directory) / 'older & draft.json', Path(directory) / 'newer draft.json'
        a.write_bytes(b'{"value":"PRIVATE_ENTRY_MARKER_BEFORE","count":1}')
        b.write_bytes(b'{"value":"PRIVATE_ENTRY_MARKER_AFTER","count":1}')
        return a, b

    def test_report_is_new_and_repeated_review_preserves_every_input_and_report(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = self.fixtures(directory)
            original = (a.read_bytes(), b.read_bytes())
            first = review_drafts.review_files(a, b)
            first_bytes = first.read_bytes()
            second = review_drafts.review_files(a, b)
            self.assertNotEqual(first.parent, second.parent)
            self.assertEqual(first.read_bytes(), first_bytes)
            self.assertIn(b'PRIVATE_ENTRY_MARKER', first_bytes)
            self.assertEqual((a.read_bytes(), b.read_bytes()), original)

    def test_counts_report_has_no_values_paths_or_content_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = self.fixtures(directory)
            text = review_drafts.review_files(a, b, summary=True).read_text(encoding='utf8')
            for private in ('PRIVATE_ENTRY_MARKER', '/value', str(a), str(b),
                            hashlib.sha256(a.read_bytes()).hexdigest(),
                            hashlib.sha256(b.read_bytes()).hexdigest()):
                self.assertNotIn(private, text)
            self.assertIn('CHANGED: 1', text)

    def test_invalid_or_lossy_input_leaves_no_report_folder(self):
        for bad in (b'{broken', b'{"v":1e-4000}', b'{"v":1,"v":2}', b'{}' + b' ' * compare.MAX_BYTES):
            with self.subTest(bad=bad[:24]), tempfile.TemporaryDirectory() as directory:
                a, b = self.fixtures(directory)
                b.write_bytes(bad)
                with self.assertRaises(compare.CompareError):
                    review_drafts.review_files(a, b)
                self.assertEqual(list(Path(directory).glob('draft-review-*')), [])
                self.assertEqual(b.read_bytes(), bad)

    def test_same_file_is_refused_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            a, _ = self.fixtures(directory)
            with self.assertRaisesRegex(compare.CompareError, 'same file'):
                review_drafts.review_files(a, a)
            self.assertEqual(list(Path(directory).glob('draft-review-*')), [])

    def test_write_failure_does_not_change_prior_files_or_leave_a_success_report(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = self.fixtures(directory)
            prior = Path(directory) / 'prior-report.html'; prior.write_bytes(b'EXISTING')
            with mock.patch.object(compare, '_atomic', side_effect=OSError('synthetic failure')):
                with self.assertRaises(OSError):
                    review_drafts.review_files(a, b)
            self.assertEqual(prior.read_bytes(), b'EXISTING')
            self.assertEqual(list(Path(directory).glob('draft-review-*')), [])

    def test_cancelled_prompt_creates_nothing(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = review_drafts.main([], ask=mock.Mock(side_effect=EOFError))
        self.assertEqual(result, 1)
        self.assertIn('Cancelled', output.getvalue())

    def test_interactive_cli_accepts_quoted_paths_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as other:
            a, b = self.fixtures(directory)
            result = subprocess.run([sys.executable, str(ROOT / 'review_drafts.py')],
                                    input=('"' + str(a) + '"\n"' + str(b) + '"\n').encode(),
                                    cwd=other, capture_output=True, timeout=10,
                                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(b'Your two drafts were not changed', result.stdout)
            self.assertEqual(len(list(Path(directory).glob('draft-review-*/comparison.html'))), 1)

    def test_cli_lossy_refusal_has_no_value_leak_or_output(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = self.fixtures(directory); b.write_bytes(b'{"PRIVATE_ENTRY_MARKER":1e-4000}')
            result = subprocess.run([sys.executable, str(ROOT / 'review_drafts.py'), str(a), str(b), '--summary'],
                                    capture_output=True, timeout=10,
                                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            self.assertEqual(result.returncode, 2)
            self.assertNotIn(b'PRIVATE_ENTRY_MARKER', result.stderr)
            self.assertNotIn(b'1e-4000', result.stderr)
            self.assertEqual(list(Path(directory).glob('draft-review-*')), [])

    def test_portable_build_is_allowlisted_complete_and_refuses_replacement(self):
        import zipfile
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'Review kit'
            result = make_portable.build(destination)
            manifest = json.loads((destination / 'MANIFEST.json').read_text())
            for item in manifest:
                self.assertEqual(hashlib.sha256((destination / item['path']).read_bytes()).hexdigest(), item['sha256'])
            self.assertEqual(result['files'], 11)
            with zipfile.ZipFile(result['zip']) as archive:
                self.assertEqual(len(archive.namelist()), result['files'])
                self.assertFalse(any('test_' in name or '__pycache__' in name for name in archive.namelist()))
                for name in archive.namelist():
                    self.assertEqual(archive.read(name), (destination / Path(name).relative_to(destination.name)).read_bytes())
            original = Path(result['zip']).read_bytes()
            with self.assertRaises(ValueError):
                make_portable.build(destination)
            self.assertEqual(Path(result['zip']).read_bytes(), original)

    @unittest.skipUnless(os.name == 'nt', 'Windows console launchers')
    def test_both_windows_launchers_work_from_a_path_with_spaces_and_ampersand(self):
        with tempfile.TemporaryDirectory(prefix='review kit & spaces ') as directory:
            folder = Path(directory)
            for name in ('compare.py', 'html_report.py', 'review_drafts.py',
                         'Review drafts.cmd', 'Review counts only.cmd'):
                shutil.copyfile(ROOT / name, folder / name)
            for name, summary in (('Review drafts.cmd', False), ('Review counts only.cmd', True)):
                with self.subTest(name=name), tempfile.TemporaryDirectory() as inputs:
                    a, b = self.fixtures(inputs)
                    # Fixed owned launcher is shell-quoted; draft paths enter stdin, never shell text.
                    command = subprocess.list2cmdline([os.environ.get('COMSPEC', 'cmd.exe'), '/d', '/s', '/c'])
                    command += ' ""' + str(folder / name) + '""'
                    result = subprocess.run(command, input=('"' + str(a) + '"\r\n"' + str(b) + '"\r\n\r\n').encode(),
                                            capture_output=True, timeout=10,
                                            creationflags=subprocess.CREATE_NO_WINDOW)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    reports = list(Path(inputs).glob('draft-review-*/comparison.html'))
                    self.assertEqual(len(reports), 1)
                    text = reports[0].read_text(encoding='utf8')
                    self.assertEqual('PRIVATE_ENTRY_MARKER' not in text, summary)


if __name__ == '__main__':
    unittest.main()
