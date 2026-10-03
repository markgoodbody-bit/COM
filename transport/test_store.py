import concurrent.futures
import sqlite3
import tempfile
import unittest
from pathlib import Path
from store import Refusal, Store


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'fixture.db'
        self.store = Store(self.path)
        self.store.initialize()
        self.store.provision('codex', 'synthetic-codex')
        self.store.provision('framework', 'synthetic-framework')

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def send(self, key='one', body='synthetic'):
        return self.store.send('synthetic-codex', key, body, 'framework')

    def test_duplicate_and_lost_response_have_one_effect(self):
        committed = self.send()
        self.store.close()  # Discard response; new connection resolves same request.
        self.store = Store(self.path)
        self.assertEqual(committed, self.send())
        self.assertEqual(1, self.store.db.execute('SELECT count(*) FROM messages').fetchone()[0])

    def test_request_key_conflict(self):
        self.send()
        with self.assertRaisesRegex(Refusal, 'CONFLICT'):
            self.send(body='different')

    def test_read_crash_does_not_consume(self):
        self.send()
        first = self.store.fetch('synthetic-framework', 0)
        self.store.close()
        self.store = Store(self.path)
        second = self.store.fetch('synthetic-framework', 0)
        self.assertEqual(first['messages'], second['messages'])
        self.assertEqual(0, second['consumed'])

    def test_ack_delivered_boundary_and_idempotent_retry(self):
        self.send()
        page = self.store.fetch('synthetic-framework', 0)
        self.send('two')
        with self.assertRaisesRegex(Refusal, 'UNDELIVERED'):
            self.store.acknowledge('synthetic-framework', page['receipt'], 2, no_answer_owed='synthetic observation')
        self.store.acknowledge('synthetic-framework', page['receipt'], 1, no_answer_owed='synthetic observation')
        self.store.acknowledge('synthetic-framework', page['receipt'], 1, no_answer_owed='synthetic observation')
        self.assertEqual(2, self.store.fetch('synthetic-framework', 1)['through'])

    def test_wrong_aperture_and_replaced_receipt(self):
        self.send()
        old = self.store.fetch('synthetic-framework', 0)
        with self.assertRaises(Refusal):
            self.store.acknowledge('synthetic-codex', old['receipt'], 1, no_answer_owed='synthetic observation')
        self.store.fetch('synthetic-framework', 0)
        with self.assertRaises(Refusal):
            self.store.acknowledge('synthetic-framework', old['receipt'], 1, no_answer_owed='synthetic observation')

    def test_stale_and_forward_cursor_refused(self):
        self.send()
        page = self.store.fetch('synthetic-framework', 0)
        self.store.acknowledge('synthetic-framework', page['receipt'], 1, no_answer_owed='synthetic observation')
        for cursor in (0, 2, -1):
            with self.assertRaisesRegex(Refusal, 'CURSOR_MISMATCH'):
                self.store.fetch('synthetic-framework', cursor)

    def test_wrong_and_revoked_credentials(self):
        with self.assertRaisesRegex(Refusal, 'UNAUTHORIZED'):
            self.store.fetch('wrong', 0)
        self.store.db.execute("UPDATE apertures SET revoked=1 WHERE id='codex'")
        with self.assertRaisesRegex(Refusal, 'UNAUTHORIZED'):
            self.send()

    def test_multiwriter_ordering_and_namespaced_keys(self):
        def writer(index):
            store = Store(self.path)
            try:
                token = 'synthetic-codex' if index % 2 else 'synthetic-framework'
                return store.send(token, str(index // 2), 'synthetic', 'framework')
            finally:
                store.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            sequences = list(executor.map(writer, range(20)))
        self.assertEqual(list(range(1, 21)), sorted(sequences))

    def test_absent_aperture_bounded_catchup_and_restart(self):
        for index in range(43):
            self.send(str(index))
        cursor, seen = 0, []
        while True:
            page = self.store.fetch('synthetic-framework', cursor, 7)
            if not page['messages']:
                break
            seen.extend(row['seq'] for row in page['messages'])
            self.store.acknowledge('synthetic-framework', page['receipt'], page['through'], no_answer_owed='synthetic observation')
            cursor = page['through']
        self.store.close()
        self.store = Store(self.path)
        self.assertEqual(list(range(1, 44)), seen)
        self.assertEqual([], self.store.fetch('synthetic-framework', cursor)['messages'])

    def test_append_only(self):
        self.send()
        for sql in ('DELETE FROM messages', "UPDATE messages SET body='changed'"):
            with self.assertRaisesRegex(sqlite3.IntegrityError, 'append only'):
                self.store.db.execute(sql)

    def test_input_bounds(self):
        for key, body in (('', 'x'), ('x'*65, 'x'), ('x', ''), ('x', 'x'*16385)):
            with self.assertRaises(Refusal):
                self.send(key, body)
        for after, limit in ((True, 20), (0, 0), (0, 101)):
            with self.assertRaises(Refusal):
                self.store.fetch('synthetic-codex', after, limit)

    def test_ack_needs_disposition_and_valid_answer(self):
        self.send()
        page = self.store.fetch('synthetic-framework', 0)
        with self.assertRaisesRegex(Refusal, 'DISPOSITION_REQUIRED'):
            self.store.acknowledge('synthetic-framework', page['receipt'], 1)
        with self.assertRaisesRegex(Refusal, 'INVALID_ANSWER'):
            self.store.acknowledge('synthetic-framework', page['receipt'], 1, answered_by=1)
        answer = self.store.send('synthetic-framework', 'answer', 'received', 'codex')
        self.store.acknowledge('synthetic-framework', page['receipt'], 1, answered_by=answer)
        with self.assertRaisesRegex(Refusal, 'DISPOSITION_CONFLICT'):
            self.store.acknowledge('synthetic-framework', page['receipt'], 1, no_answer_owed='changed story')

    def test_recipient_and_decision_anchor(self):
        with self.assertRaisesRegex(Refusal, 'UNKNOWN_RECIPIENT'):
            self.store.send('synthetic-codex', 'x', 'body', 'unknown')
        with self.assertRaisesRegex(Refusal, 'ANCHOR_REQUIRED'):
            self.store.send('synthetic-codex', 'x', 'body', 'framework', kind='decision')
        seq = self.store.send('synthetic-codex', 'x', 'body', 'framework', kind='decision',
                              github_anchor='https://github.com/markgoodbody-bit/COM/issues/760')
        self.assertEqual(1, seq)

    def test_truncation_is_visible_and_zero_is_measured(self):
        for index in range(51):
            self.send(str(index))
        page = self.store.fetch('synthetic-framework', 0, 10)
        self.assertEqual((51, 51, 10, True),
                         (page['head_seq'], page['unread_count'], page['page_count'], page['has_more']))
        self.assertGreater(page['server_time'], 0)
        self.assertEqual(0, self.store.state('synthetic-framework')['consumed'])
        empty = self.store.fetch('synthetic-codex', 0, 100)
        self.store.acknowledge('synthetic-codex', empty['receipt'], 51, no_answer_owed='synthetic observation')
        zero = self.store.fetch('synthetic-codex', 51)
        self.assertEqual((0, 51, False), (zero['unread_count'], zero['head_seq'], zero['has_more']))


if __name__ == '__main__':
    unittest.main()
