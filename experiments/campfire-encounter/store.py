"""Synthetic-only encounter store. No authentication, server, or erasure promise."""
import json
import sqlite3
import uuid


class Store:
    DISCLOSURE = 'synthetic-shared-room-v1'

    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        version = self.db.execute('PRAGMA user_version').fetchone()[0]
        existing = self.db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='entries'").fetchone()
        if existing and version != 1:
            self.db.close()
            raise ValueError('Old probe database: preserved; automatic migration not implemented')
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS encounters (
          id TEXT PRIMARY KEY, disclosure TEXT NOT NULL, expires INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS acceptances (
          id TEXT PRIMARY KEY, encounter TEXT NOT NULL REFERENCES encounters(id),
          participant_claim TEXT NOT NULL, disclosure TEXT NOT NULL,
          observed_route TEXT NOT NULL, accepted_at INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS entries (
          id TEXT PRIMARY KEY, encounter TEXT NOT NULL REFERENCES encounters(id),
          request TEXT NOT NULL, claimed_producer TEXT NOT NULL, body TEXT NOT NULL,
          relation TEXT NOT NULL, target TEXT REFERENCES entries(id),
          carry INTEGER NOT NULL, acceptance TEXT NOT NULL REFERENCES acceptances(id),
          observed_route TEXT NOT NULL, UNIQUE(acceptance, request));
        PRAGMA user_version=1;
        ''')

    def close(self):
        self.db.close()

    def encounter(self, *, accepts, now, ttl=3600):
        if accepts is not True or type(ttl) is not int or not 0 < ttl <= 86400:
            raise ValueError('Explicit acceptance and bounded synthetic TTL required')
        identity = str(uuid.uuid4())
        with self.db:
            self.db.execute('INSERT INTO encounters VALUES (?,?,?)',
                            (identity, self.DISCLOSURE, now + ttl))
        return identity

    def accept(self, encounter, participant, *, disclosure, accepts, now):
        if (accepts is not True or disclosure != self.DISCLOSURE
                or not isinstance(participant, str) or not participant
                or len(participant.encode('utf-8')) > 128):
            raise ValueError('Explicit participant acceptance of this disclosure required')
        identity = str(uuid.uuid4())
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            self._live(encounter, now)
            # This storage-only caller supplies no authenticated route. Do not
            # accept a caller's invented route as a host observation.
            self.db.execute('INSERT INTO acceptances VALUES (?,?,?,?,?,?)',
                            (identity, encounter, participant, disclosure, 'UNKNOWN', now))
        return identity

    def _live(self, encounter, now):
        row = self.db.execute('SELECT * FROM encounters WHERE id=?', (encounter,)).fetchone()
        if row is None or now >= row['expires']:
            raise ValueError('Encounter missing or expired')
        return row

    def append(self, encounter, request, producer, body, *, now, acceptance, carry,
               relation='statement', target=None):
        for value, limit in ((request, 128), (producer, 128), (body, 8192)):
            if not isinstance(value, str) or not value or len(value.encode('utf-8')) > limit:
                raise ValueError('Invalid or oversized text')
        if type(carry) is not bool or relation not in ('statement', 'response', 'dispute', 'correction', 'decline'):
            raise ValueError('Invalid operation')
        if (relation == 'statement') != (target is None):
            raise ValueError('Linked entries require a target; statements do not')
        if target is not None and (not isinstance(target, str) or not target or len(target) > 128):
            raise ValueError('Invalid target identifier')
        values = (producer, body, relation, target, int(carry))
        with self.db:
            # Serialize the live/target check and append against other writers.
            self.db.execute('BEGIN IMMEDIATE')
            self._live(encounter, now)
            consent = self.db.execute('SELECT * FROM acceptances WHERE id=? AND encounter=?',
                                      (acceptance, encounter)).fetchone()
            if (consent is None or consent['participant_claim'] != producer
                    or consent['disclosure'] != self.DISCLOSURE):
                raise ValueError('No matching participant acceptance')
            prior = self.db.execute('SELECT * FROM entries WHERE acceptance=? AND request=?',
                                    (acceptance, request)).fetchone()
            if prior:
                if tuple(prior[k] for k in ('claimed_producer', 'body', 'relation', 'target', 'carry')) != values:
                    raise ValueError('Request ID reused with different content')
                return prior['id']
            if target and not self.db.execute('SELECT 1 FROM entries WHERE id=? AND encounter=?',
                                             (target, encounter)).fetchone():
                raise ValueError('Target missing or belongs to another encounter')
            if self.db.execute('SELECT count(*) FROM entries WHERE encounter=?', (encounter,)).fetchone()[0] >= 100:
                raise ValueError('Synthetic encounter limit reached')
            identity = str(uuid.uuid4())
            self.db.execute('INSERT INTO entries VALUES (?,?,?,?,?,?,?,?,?,?)',
                            (identity, encounter, request, *values, acceptance, consent['observed_route']))
        return identity

    def read(self, encounter, *, now):
        self._live(encounter, now)
        # Acceptance is a reusable local capability, not portable provenance.
        # Never distribute it (or internal retry keys) to readers/export holders.
        return [dict(r) for r in self.db.execute(
            'SELECT id,encounter,claimed_producer,body,relation,target,carry,observed_route '
            'FROM entries WHERE encounter=? ORDER BY rowid', (encounter,))]

    def export(self, encounter, *, now):
        entries = self.read(encounter, now=now)
        # A partial export could remove the only disagreement. Refuse the whole
        # bundle rather than imply a selectively exported thread is complete.
        if any(not row['carry'] for row in entries):
            raise ValueError('Whole-thread export blocked by carry-forward choice')
        return json.dumps({'format': 'campfire-synthetic-v2',
                           'authority': 'NONE', 'identity_verified': False,
                           'entries': entries}, ensure_ascii=False)
