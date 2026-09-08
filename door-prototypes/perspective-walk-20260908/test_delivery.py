"""Offline tests of one-shot delivery checks; no claim of public HTTPS success."""
import json
import ssl
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch
import check_delivery as d


class DeliveryTests(unittest.TestCase):
    def test_matching_https(self):
        report, code = d.run({'index.html': b'ok'},
            lambda u: (200, u, b'ok', 'text/html', []))
        self.assertEqual((report['state'], code), ('SELECTED_HTTPS_BYTES_MATCHED', 0))
        self.assertEqual(report['results'][0]['requested'], d.ORIGIN)

    def test_tls_failure_is_failure_without_http_retry(self):
        requested = []
        def fail(url):
            requested.append(url)
            raise ssl.SSLCertVerificationError('hostname mismatch')
        report, code = d.run({'index.html': b'ok'}, fail)
        self.assertEqual(code, 1)
        self.assertEqual(report['matched'], 0)
        self.assertEqual(requested, [d.ORIGIN])

    def test_dns_failure_is_not_a_certificate_diagnosis(self):
        def fail(url):
            raise OSError('name resolution failed')
        report, code = d.run({'index.html': b'ok'}, fail)
        self.assertEqual(code, 1)
        self.assertIn('name resolution failed', report['results'][0]['error'])
        self.assertNotIn('certificate', report['results'][0]['error'])

    def test_wrong_bytes_and_error_status_do_not_pass(self):
        for status, body in [(200, b'old'), (404, b'ok'), (500, b'ok')]:
            with self.subTest(status=status, body=body):
                report, code = d.run({'index.html': b'ok'},
                    lambda u: (status, u, body, 'text/html', []))
                self.assertEqual(code, 1)
                self.assertFalse(report['results'][0]['ok'])

    def test_mixed_pass_and_failure_does_not_pass(self):
        report, code = d.run({'index.html': b'ok', 'llms.txt': b'new'},
            lambda u: (200, u, b'ok', 'text/plain', []))
        self.assertEqual((code, report['matched'], report['selected']), (1, 1, 2))

    def test_unsafe_redirects_are_refused_before_request(self):
        req = urllib.request.Request(d.ORIGIN)
        for target in ('http://pleasestartfromhere.com/', 'https://other.example/',
                       'https://user:secret@pleasestartfromhere.com/',
                       'https://pleasestartfromhere.com:444/',
                       'https://pleasestartfromhere.com/?secret=value'):
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    d.SameOriginRedirect().redirect_request(req, None, 302, 'found', {}, target)

    def test_safe_redirects_remain_bounded(self):
        handler = d.SameOriginRedirect()
        req = urllib.request.Request(d.ORIGIN)
        for _ in range(4):
            new = handler.redirect_request(req, None, 301, 'moved', {}, '/index.html')
            self.assertEqual(new.full_url, d.ORIGIN + 'index.html')
        with self.assertRaises(ValueError):
            handler.redirect_request(req, None, 301, 'moved', {}, '/index.html')

    def test_final_http_or_cross_origin_cannot_pass(self):
        for final in ('http://pleasestartfromhere.com/', 'https://other.example/'):
            report, code = d.run({'index.html': b'ok'},
                lambda u: (200, final, b'ok', 'text/html', []))
            self.assertEqual(code, 1)

    def test_relative_reading_references(self):
        self.assertEqual(d.local_path('explore/start.json', 'nodes/hardening.md'),
                         'explore/nodes/hardening.md')
        for ref in ('../secret', '/file', 'https://other.example/', '%2e%2e/file',
                    'nodes\\hardening.md', 'file?token=x'):
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                d.local_path('explore/start.json', ref)

    def test_local_selection_follows_built_routes_and_requires_real_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            entries = {'index.html': b'root', 'llms.txt': b'guide',
                       'explore/start.json': json.dumps({'format': 'psfh-arrival/0.1',
                           'routes': {'questions': 'questions.json', 'text': 'questions.txt'}}).encode(),
                       'explore/questions.json': json.dumps({'nodes': [{'id': 'hardening',
                           'routes': {'text': 'nodes/hardening.md'}}]}).encode(),
                       'explore/questions.txt': b'question', 'explore/nodes/hardening.md': b'leaf'}
            for p, b in entries.items():
                f = root / p; f.parent.mkdir(parents=True, exist_ok=True); f.write_bytes(b)
            self.assertEqual(d.expected_routes(root), dict(sorted(entries.items())))
            (root / 'explore/nodes/hardening.md').unlink()
            with self.assertRaises(FileNotFoundError):
                d.expected_routes(root)

    def test_external_symlink_target_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); root = base / 'site'; root.mkdir()
            (base / 'private').write_bytes(b'not build data')
            try:
                (root / 'index.html').symlink_to(base / 'private')
            except (OSError, NotImplementedError) as error:
                self.skipTest('Symlink fixture unavailable on this platform: ' + str(error))
            with self.assertRaises(ValueError):
                d.read_expected(root, 'index.html')

    def test_empty_sample_and_oversized_files_refused(self):
        with self.assertRaises(ValueError):
            d.run({})
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root / 'big').write_bytes(b'x' * (d.MAX_BYTES + 1))
            with self.assertRaises(ValueError):
                d.read_expected(root, 'big')

    def test_fetch_bounds_response_without_authentication(self):
        class Response:
            status = 200; url = d.ORIGIN; headers = {'Content-Type': 'text/html'}
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, limit):
                self.limit = limit
                return b'x' * limit
        class Opener:
            def open(self, request, timeout):
                self.request = request
                self.timeout = timeout
                return Response()
        opener = Opener()
        with patch.object(d.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaises(ValueError):
                d.fetch_https(d.ORIGIN)
        self.assertFalse(opener.request.has_header('Authorization'))
        self.assertFalse(opener.request.has_header('Cookie'))
        self.assertEqual(opener.timeout, 8)


if __name__ == '__main__':
    unittest.main()
