PRAGMA foreign_keys = ON;
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
