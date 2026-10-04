"""Local storage-contract fixture. Not a deployed Worker or D1 adapter."""
import hashlib
import re
import secrets
import sqlite3
import time
from pathlib import Path


class Refusal(Exception):
    pass


class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=10, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys = ON')

    def initialize(self):
        self.db.executescript(Path(__file__).with_name('schema.sql').read_text())

    def provision(self, aperture, token):
        # Operator-only fixture setup; never an unauthenticated endpoint.
        self.db.execute('INSERT INTO apertures(id,credential_hash) VALUES (?,?)',
                        (aperture, self.digest(token)))

    @staticmethod
    def digest(token):
        return hashlib.sha256(token.encode()).hexdigest()

    def authenticate(self, token):
        row = self.db.execute(
            'SELECT * FROM apertures WHERE credential_hash=? AND revoked=0',
            (self.digest(token),)).fetchone()
        if row is None:
            raise Refusal('UNAUTHORIZED')
        return row

    def state(self, token):
        aperture = self.authenticate(token)
        head = self.db.execute('SELECT COALESCE(MAX(seq),0) FROM messages').fetchone()[0]
        return {'consumed': aperture['consumed'], 'head_seq': head,
                'server_time': int(time.time())}

    def send(self, token, request_key, body, recipient, kind='message', github_anchor=None):
        if not isinstance(request_key, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', request_key):
            raise Refusal('INVALID_REQUEST_KEY')
        if not isinstance(body, str) or not 1 <= len(body.encode('utf-8')) <= 16384:
            raise Refusal('INVALID_BODY')
        if kind not in ('message', 'decision'):
            raise Refusal('INVALID_KIND')
        if github_anchor is not None and (not isinstance(github_anchor, str) or
                not re.fullmatch(r'https://github\.com/markgoodbody-bit/COM/(issues|pull)/[1-9][0-9]*(#issuecomment-[0-9]+)?', github_anchor)):
            raise Refusal('INVALID_ANCHOR')
        if kind == 'decision' and github_anchor is None:
            raise Refusal('DECISION_ANCHOR_REQUIRED')
        self.db.execute('BEGIN IMMEDIATE')
        try:
            sender = self.authenticate(token)['id']
            if not self.db.execute('SELECT 1 FROM apertures WHERE id=? AND revoked=0', (recipient,)).fetchone():
                raise Refusal('UNKNOWN_RECIPIENT')
            previous = self.db.execute(
                'SELECT * FROM messages WHERE sender=? AND request_key=?',
                (sender, request_key)).fetchone()
            if previous:
                if (previous['body'], previous['recipient'], previous['kind'], previous['github_anchor']) != (body, recipient, kind, github_anchor):
                    raise Refusal('REQUEST_KEY_CONFLICT')
                seq = previous['seq']
            else:
                seq = self.db.execute(
                    'INSERT INTO messages(sender,recipient,kind,github_anchor,request_key,body,received_at) VALUES (?,?,?,?,?,?,?)',
                    (sender, recipient, kind, github_anchor, request_key, body, int(time.time()))).lastrowid
            self.db.execute('COMMIT')
            return seq
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def fetch(self, token, after, limit=20):
        if type(after) is not int or type(limit) is not int or not 1 <= limit <= 100:
            raise Refusal('INVALID_PAGE')
        self.db.execute('BEGIN IMMEDIATE')
        try:
            aperture = self.authenticate(token)
            if after != aperture['consumed']:
                raise Refusal('CURSOR_MISMATCH')
            rows = self.db.execute('SELECT * FROM messages WHERE seq>? ORDER BY seq LIMIT ?',
                                   (after, limit)).fetchall()
            # One outstanding page per aperture; a refetch invalidates the old receipt.
            self.db.execute('DELETE FROM deliveries WHERE aperture=? AND disposition IS NULL', (aperture['id'],))
            receipt = None
            if rows:
                receipt = secrets.token_urlsafe(24)
                self.db.execute('INSERT INTO deliveries(receipt,aperture,start_seq,end_seq) VALUES (?,?,?,?)',
                                (receipt, aperture['id'], after, rows[-1]['seq']))
            head = self.db.execute('SELECT COALESCE(MAX(seq),0) FROM messages').fetchone()[0]
            unread = self.db.execute('SELECT COUNT(*) FROM messages WHERE seq>?', (after,)).fetchone()[0]
            self.db.execute('COMMIT')
            return {'messages': [dict(row) for row in rows], 'receipt': receipt,
                    'consumed': after, 'through': rows[-1]['seq'] if rows else after,
                    'head_seq': head, 'unread_count': unread, 'page_count': len(rows),
                    'has_more': unread > len(rows), 'server_time': int(time.time())}
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def acknowledge(self, token, receipt, through, *, no_answer_owed=None, answered_by=None):
        # Caller explicitly asserts consumption; the server cannot prove comprehension.
        if type(through) is not int:
            raise Refusal('INVALID_ACK')
        if (no_answer_owed is None) == (answered_by is None):
            raise Refusal('ACK_DISPOSITION_REQUIRED')
        if no_answer_owed is not None:
            if not isinstance(no_answer_owed, str) or not 1 <= len(no_answer_owed.strip().encode()) <= 1024:
                raise Refusal('INVALID_DISPOSITION')
            disposition = 'no_answer_owed:' + no_answer_owed
        else:
            if type(answered_by) is not int or answered_by < 1:
                raise Refusal('INVALID_ANSWER')
            disposition = 'answered_by:' + str(answered_by)
        self.db.execute('BEGIN IMMEDIATE')
        try:
            aperture = self.authenticate(token)
            page = self.db.execute('SELECT * FROM deliveries WHERE receipt=? AND aperture=?',
                                   (receipt, aperture['id'])).fetchone()
            if page is None or page['end_seq'] != through:
                raise Refusal('UNDELIVERED_ACK')
            if answered_by is not None and not self.db.execute(
                    'SELECT 1 FROM messages WHERE seq=? AND sender=?',
                    (answered_by, aperture['id'])).fetchone():
                raise Refusal('INVALID_ANSWER')
            if page['disposition'] is not None and page['disposition'] != disposition:
                raise Refusal('ACK_DISPOSITION_CONFLICT')
            if aperture['consumed'] not in (page['start_seq'], page['end_seq']):
                raise Refusal('CURSOR_MISMATCH')
            self.db.execute('UPDATE apertures SET consumed=? WHERE id=?',
                            (through, aperture['id']))
            self.db.execute('UPDATE deliveries SET disposition=? WHERE receipt=?', (disposition, receipt))
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def close(self):
        self.db.close()
