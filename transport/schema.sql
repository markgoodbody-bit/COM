PRAGMA foreign_keys = ON;
CREATE TABLE mutation_guard (id INTEGER PRIMARY KEY CHECK(id=1), ok INTEGER NOT NULL CHECK(ok=1));
CREATE TABLE apertures (
  id TEXT PRIMARY KEY,
  credential_hash TEXT NOT NULL UNIQUE,
  revoked INTEGER NOT NULL DEFAULT 0 CHECK (revoked IN (0, 1)),
  consumed INTEGER NOT NULL DEFAULT 0 CHECK (consumed >= 0)
);
CREATE TABLE messages (
  seq INTEGER PRIMARY KEY AUTOINCREMENT,
  sender TEXT NOT NULL REFERENCES apertures(id),
  recipient TEXT NOT NULL REFERENCES apertures(id),
  kind TEXT NOT NULL CHECK(kind IN ('message','decision')),
  github_anchor TEXT,
  request_key TEXT NOT NULL,
  body TEXT NOT NULL,
  received_at INTEGER NOT NULL,
  UNIQUE(sender, request_key),
  CHECK(kind != 'decision' OR github_anchor IS NOT NULL)
);
-- Reserved broadcast destination; no valid bearer hashes to this sentinel.
INSERT INTO apertures(id,credential_hash,revoked) VALUES('shared','NO_CREDENTIAL:shared',1);
CREATE INDEX messages_recipient_seq ON messages(recipient,seq);
CREATE TABLE comhead (
  id INTEGER PRIMARY KEY CHECK(id=1),
  version INTEGER NOT NULL CHECK(version>0),
  basis_seq INTEGER NOT NULL CHECK(basis_seq>=0),
  updated_at INTEGER NOT NULL,
  body TEXT NOT NULL CHECK(length(body)<=8192),
  github_anchor TEXT NOT NULL
);
CREATE TRIGGER messages_no_update BEFORE UPDATE ON messages
BEGIN SELECT RAISE(ABORT, 'append only'); END;
CREATE TRIGGER messages_no_delete BEFORE DELETE ON messages
BEGIN SELECT RAISE(ABORT, 'append only'); END;
CREATE TABLE deliveries (
  receipt TEXT PRIMARY KEY,
  aperture TEXT NOT NULL REFERENCES apertures(id),
  start_seq INTEGER NOT NULL,
  end_seq INTEGER NOT NULL,
  disposition TEXT
);
CREATE TABLE acknowledgements (
  receipt TEXT NOT NULL REFERENCES deliveries(receipt),
  aperture TEXT NOT NULL REFERENCES apertures(id),
  seq INTEGER NOT NULL REFERENCES messages(seq),
  disposition TEXT NOT NULL,
  PRIMARY KEY(receipt,seq)
);
CREATE TRIGGER acknowledgements_no_update BEFORE UPDATE ON acknowledgements
BEGIN SELECT RAISE(ABORT, 'append only'); END;
CREATE TRIGGER acknowledgements_no_delete BEFORE DELETE ON acknowledgements
BEGIN SELECT RAISE(ABORT, 'append only'); END;
