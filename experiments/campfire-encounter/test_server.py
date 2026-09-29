import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path
from server import App, make_server
from store import Store
import server
from disclosure import identifier


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.now = 1000
        self.app = App(self.temp.name, clock=lambda: self.now)
        self.server = make_server(self.app)
        self.port = self.server.server_port
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.app.dispose()
        self.temp.cleanup()

    def request(self, path, data=None, headers=None, method='POST'):
        connection = http.client.HTTPConnection('127.0.0.1', self.port, timeout=5)
        h = {'Content-Type':'application/json', 'Origin':f'http://127.0.0.1:{self.port}',
             'X-Campfire-Token':self.app.token}
        h.update(headers or {})
        try:
            connection.request(method, path, None if data is None else json.dumps(data), h)
            res = connection.getresponse()
            return res.status, res.read(), dict(res.getheaders())
        finally:
            connection.close()

    def accept(self, producer='A'):
        code, raw, _ = self.request('/api/accept', {'producer':producer, 'disclosure':Store.DISCLOSURE, 'accepts':True})
        self.assertEqual(code, 200)
        return json.loads(raw)['acceptance']

    def append(self, acceptance, **override):
        data = {'acceptance':acceptance, 'request':'r', 'body':'hello', 'relation':'statement', 'target':None, 'carry':True}
        data.update(override)
        return self.request('/api/append', data)

    def test_full_http_loop(self):
        a = self.accept()
        code, raw, _ = self.append(a)
        self.assertEqual(code, 200)
        original = json.loads(raw)['id']
        b = self.accept('B')
        self.assertEqual(self.append(b, relation='dispute', target=original, body='Not established')[0], 200)
        _, raw, _ = self.request('/api/read', {'acceptance':b})
        self.assertEqual(len(json.loads(raw)['entries']), 2)
        _, raw, _ = self.request('/api/export', {'acceptance':b})
        capsule = json.loads(raw)['capsule']
        code, raw, _ = self.request('/api/inspect', {'acceptance':b, 'capsule':capsule})
        self.assertEqual(code, 200)
        self.assertEqual(json.loads(raw)['completeness'], 'NOT_ESTABLISHED')

    def test_return_visit_preserves_originals_and_requires_new_acceptance(self):
        a = self.accept()
        _, raw, _ = self.append(a)
        original = json.loads(raw)['id']
        _, raw, _ = self.request('/api/visit', {'acceptance':a, 'receipt':None})
        receipt = json.loads(raw)['receipt']
        self.assertEqual(set(receipt), {'format', 'room', 'last'})
        self.assertNotIn(a, json.dumps(receipt))
        b = self.accept('B')
        _, raw, _ = self.append(b, relation='dispute', target=original, body='Disagree', carry=False)
        dispute = json.loads(raw)['id']
        self.assertEqual(self.request('/api/visit', {'acceptance':receipt, 'receipt':receipt})[0], 400)
        returning = self.accept('A')
        code, raw, _ = self.request('/api/visit', {'acceptance':returning, 'receipt':receipt})
        self.assertEqual(code, 200)
        result = json.loads(raw)
        self.assertEqual(result['added_ids'], [dispute])
        self.assertEqual(result['entries'][0]['body'], 'hello')
        self.assertEqual(result['entries'][1]['target'], original)
        self.assertEqual(self.request('/api/export', {'acceptance':returning})[0], 400)

    def test_return_marker_unknown_wrong_room_empty_and_expired(self):
        a = self.accept()
        _, raw, _ = self.request('/api/visit', {'acceptance':a, 'receipt':None})
        receipt = json.loads(raw)['receipt']
        self.append(a)
        _, raw, _ = self.request('/api/visit', {'acceptance':a, 'receipt':receipt})
        self.assertEqual(len(json.loads(raw)['added_ids']), 1)
        for field, value, expected in [('room', 'other', 'DIFFERENT_ROOM'), ('last', 'missing', 'MARKER_NOT_FOUND')]:
            _, raw, _ = self.request('/api/visit', {'acceptance':a, 'receipt':dict(receipt, **{field:value})})
            result = json.loads(raw)
            self.assertEqual(result['comparison'], expected)
            self.assertEqual(result['added_ids'], [])
        self.assertEqual(self.request('/api/visit', {'acceptance':a, 'receipt':dict(receipt, authority='ROOT')})[0], 400)
        self.now += 86400
        self.assertEqual(self.request('/api/visit', {'acceptance':a, 'receipt':receipt})[0], 400)

    def test_host_origin_token_and_content_type(self):
        data = {'acceptance':'missing'}
        for headers in ({'Host':'evil.example'}, {'Origin':'https://evil.example'},
                        {'Origin':'null'}, {'X-Campfire-Token':'bad'}):
            self.assertEqual(self.request('/api/read', data, headers)[0], 403)
        self.assertEqual(self.request('/api/read', data, {'Content-Type':'text/plain'})[0], 400)
        self.assertEqual(self.request('/', method='GET', headers={'Host':'evil.example'})[0], 403)

    def test_no_file_serving_or_get_mutations(self):
        for path in ('/server.py', '/encounters.sqlite', '/../store.py', '/api/accept', '/?token=anything'):
            self.assertEqual(self.request(path, method='GET')[0], 404)
        code, raw, headers = self.request('/', method='GET')
        self.assertEqual(code, 200)
        self.assertIn("frame-ancestors 'none'", headers['Content-Security-Policy'])
        self.assertEqual(headers['Cache-Control'], 'no-store')
        self.assertNotIn(b'TOKEN_PLACEHOLDER', raw)

    def test_clock_not_client_controlled_and_expiry_not_delete(self):
        a = self.accept()
        self.assertEqual(self.append(a, now=0)[0], 400)
        self.assertEqual(self.append(a)[0], 200)
        self.now += 86400
        self.assertEqual(self.request('/api/read', {'acceptance':a})[0], 400)
        self.assertTrue(self.app.path.exists())

    def test_no_consent_and_carry_confusion(self):
        self.assertEqual(self.request('/api/read', {'acceptance':'missing'})[0], 400)
        a = self.accept()
        self.assertEqual(self.append(a, carry='yes')[0], 400)
        self.assertEqual(self.append(a, carry=False)[0], 200)
        self.assertEqual(self.request('/api/export', {'acceptance':a})[0], 400)

    def test_no_html_promotion(self):
        a = self.accept('<img src=x onerror=alert(1)>')
        payload = '</script><script>alert(1)</script>'
        self.assertEqual(self.append(a, body=payload)[0], 200)
        _, raw, _ = self.request('/api/read', {'acceptance':a})
        self.assertEqual(json.loads(raw)['entries'][0]['body'], payload)
        # Source-level guard, not a browser execution test.
        js = Path(__file__).with_name('app.js').read_text(encoding='utf-8')
        self.assertNotIn('innerHTML', js)
        self.assertNotIn('eval(', js)

    def test_bad_target_types_do_not_break_next_request(self):
        a = self.accept()
        for target in ([], {}, '', 42, True):
            with self.subTest(target=target):
                self.assertEqual(self.append(a, relation='response', target=target)[0], 400)
        self.assertEqual(self.append(a)[0], 200)

    def test_read_and_export_do_not_distribute_acceptance_capabilities(self):
        a = self.accept('A')
        self.assertEqual(self.append(a)[0], 200)
        b = self.accept('B')
        for operation in ('read', 'export'):
            code, raw, _ = self.request('/api/' + operation, {'acceptance':b})
            self.assertEqual(code, 200)
            self.assertNotIn(a.encode(), raw)
            result = json.loads(raw)
            rows = result['entries'] if operation == 'read' else json.loads(result['capsule'])['entries']
            self.assertNotIn('acceptance', rows[0])
            self.assertNotIn('request', rows[0])
            self.assertEqual(self.append(rows[0]['id'], request='forged')[0], 400)

    def test_dispose_only_known_files_and_no_secure_erasure_claim(self):
        unrelated = Path(self.temp.name) / 'keep.txt'
        unrelated.write_text('unrelated fixture')
        for suffix in ('-wal', '-shm', '-journal'):
            Path(str(self.app.path) + suffix).write_bytes(b'synthetic artifact')
        self.app.dispose()
        self.assertTrue(unrelated.exists())
        self.assertFalse(self.app.path.exists())
        for suffix in ('-wal', '-shm', '-journal'):
            self.assertFalse(Path(str(self.app.path) + suffix).exists())
        with self.assertRaises(ValueError): self.app.dispatch('read', {'acceptance':'x'})

    def test_same_claim_different_handles_not_capabilities(self):
        a, b = self.accept('Codex'), self.accept('Codex')
        self.append(a)
        self.append(b)
        _, raw, _ = self.request('/api/read', {'acceptance':a})
        rows = json.loads(raw)['entries']
        self.assertNotEqual(rows[0]['acceptance_handle'], rows[1]['acceptance_handle'])
        for row in rows:
            self.assertEqual(self.append(row['acceptance_handle'], request='forged')[0], 400)
        js = Path(__file__).with_name('app.js').read_text(encoding='utf-8')
        self.assertIn('Claimed by', js)
        self.assertIn('matches a named role; not verified', js)

    def test_disclosure_endpoint_and_changed_text_rejected(self):
        code, raw, _ = self.request('/api/disclosure', method='GET')
        self.assertEqual(code, 200)
        disclosure = json.loads(raw)
        self.assertEqual(disclosure['id'], identifier(disclosure['text']))
        a = self.accept()
        original = server.DISCLOSURE
        try:
            server.DISCLOSURE = 'Different terms'
            data = {'producer':'B', 'disclosure':disclosure['id'], 'accepts':True}
            self.assertEqual(self.request('/api/accept', data)[0], 400)
            self.assertEqual(self.request('/api/read', {'acceptance':a})[0], 400)
        finally:
            server.DISCLOSURE = original
        self.assertIn('does not securely erase', disclosure['text'])
        self.assertIn('a crash can leave', disclosure['text'])

    def test_acceptance_bound_and_existing_reader_survives(self):
        a = self.accept()
        for i in range(99):
            self.accept(str(i))
        data = {'producer':'overflow', 'disclosure':Store.DISCLOSURE, 'accepts':True}
        self.assertEqual(self.request('/api/accept', data)[0], 400)
        self.assertEqual(self.request('/api/read', {'acceptance':a})[0], 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
