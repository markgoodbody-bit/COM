PRAGMA foreign_keys = ON;
-- Must be explicitly bound by the operator before HTTP service can start.
CREATE TABLE transport_meta (
  id INTEGER PRIMARY KEY CHECK(id=1),
  epoch TEXT NOT NULL CHECK(length(epoch)=32),
  retained_after INTEGER NOT NULL DEFAULT 0 CHECK(retained_after>=0),
  checkpoint_version INTEGER NOT NULL DEFAULT 0 CHECK(checkpoint_version>=0)
);
CREATE TABLE recovery_checkpoints (
  version INTEGER PRIMARY KEY,
  prior_epoch TEXT NOT NULL,
  new_epoch TEXT NOT NULL,
  retained_after INTEGER NOT NULL,
  head_seq INTEGER NOT NULL,
  server_time INTEGER NOT NULL,
  archive_sha256 TEXT NOT NULL,
  github_anchor TEXT NOT NULL,
  prior_head_anchor TEXT
);
CREATE TRIGGER recovery_checkpoints_no_update BEFORE UPDATE ON recovery_checkpoints
BEGIN SELECT RAISE(ABORT, 'append only'); END;
CREATE TRIGGER recovery_checkpoints_no_delete BEFORE DELETE ON recovery_checkpoints
BEGIN SELECT RAISE(ABORT, 'append only'); END;
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
CREATE INDEX messages_sender_time ON messages(sender,received_at);
CREATE INDEX messages_shared_sender_time ON messages(sender,recipient,received_at);
CREATE TABLE comhead (
  id INTEGER PRIMARY KEY CHECK(id=1),
  version INTEGER NOT NULL CHECK(version>0),
  basis_seq INTEGER NOT NULL CHECK(basis_seq>=0),
  updated_at INTEGER NOT NULL,
  body TEXT NOT NULL CHECK(length(body)<=8192),
  github_anchor TEXT NOT NULL
);
-- Operator provisioning only; no HTTP credential-management route.
CREATE TABLE head_capabilities (
  capability TEXT PRIMARY KEY CHECK(capability='comhead_writer'),
  aperture TEXT NOT NULL REFERENCES apertures(id),
  credential_hash TEXT NOT NULL UNIQUE,
  revoked INTEGER NOT NULL DEFAULT 0 CHECK(revoked IN (0,1))
);
CREATE TABLE head_audit (
  version INTEGER PRIMARY KEY,
  aperture TEXT NOT NULL REFERENCES apertures(id),
  capability TEXT NOT NULL CHECK(capability='comhead_writer'),
  server_time INTEGER NOT NULL,
  prior_basis_seq INTEGER,
  new_basis_seq INTEGER NOT NULL,
  github_anchor TEXT NOT NULL
);
CREATE TRIGGER head_audit_no_update BEFORE UPDATE ON head_audit
BEGIN SELECT RAISE(ABORT, 'append only'); END;
CREATE TRIGGER head_audit_no_delete BEFORE DELETE ON head_audit
BEGIN SELECT RAISE(ABORT, 'append only'); END;
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
