PRAGMA foreign_keys = ON;
CREATE TABLE service (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  ready_until INTEGER NOT NULL DEFAULT 0,
  enabled INTEGER NOT NULL DEFAULT 0 CHECK (enabled IN (0,1)),
  pending_limit INTEGER NOT NULL DEFAULT 100 CHECK (pending_limit > 0),
  body_limit INTEGER NOT NULL DEFAULT 1000 CHECK (body_limit > 0),
  hourly_limit INTEGER NOT NULL DEFAULT 6 CHECK (hourly_limit > 0)
);
INSERT INTO service(id) VALUES(1);
CREATE TABLE contributions (
  id TEXT PRIMARY KEY,
  retry_hash TEXT NOT NULL UNIQUE,
  request_hash TEXT NOT NULL,
  manage_hash TEXT NOT NULL,
  display_name TEXT NOT NULL,
  body TEXT,
  state TEXT NOT NULL CHECK(state IN ('pending','published','declined','withdrawn','expired')),
  revision INTEGER NOT NULL DEFAULT 1,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  body_expires_at INTEGER,
  closed_at INTEGER,
  moderation_reason TEXT,
  reconsideration INTEGER NOT NULL DEFAULT 0,
  client_hash TEXT NOT NULL,
  mutation_token TEXT
);
CREATE INDEX contributions_state ON contributions(state);
CREATE TABLE responses (
  id INTEGER PRIMARY KEY,
  contribution_id TEXT NOT NULL REFERENCES contributions(id) ON DELETE CASCADE,
  revision INTEGER NOT NULL,
  actor TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
CREATE TABLE events (
  id INTEGER PRIMARY KEY,
  contribution_id TEXT NOT NULL REFERENCES contributions(id) ON DELETE CASCADE,
  revision INTEGER NOT NULL,
  action TEXT NOT NULL,
  actor TEXT NOT NULL,
  reason TEXT,
  created_at INTEGER NOT NULL
);
CREATE TABLE rate_hits (
  client_hash TEXT NOT NULL,
  bucket INTEGER NOT NULL,
  hits INTEGER NOT NULL,
  PRIMARY KEY(client_hash, bucket)
);
-- These checks run within the INSERT statement, not a racy read-before-write check.
CREATE TRIGGER intake_guard BEFORE INSERT ON contributions BEGIN
  SELECT CASE WHEN NOT EXISTS (
    SELECT 1 FROM service WHERE id=1 AND enabled=1 AND ready_until > NEW.created_at
  ) THEN RAISE(ABORT, 'INTAKE_PAUSED') END;
  SELECT CASE WHEN (SELECT COUNT(*) FROM contributions WHERE state='pending') >=
    (SELECT pending_limit FROM service WHERE id=1)
    THEN RAISE(ABORT, 'QUEUE_FULL') END;
  SELECT CASE WHEN (SELECT COUNT(*) FROM contributions WHERE body IS NOT NULL) >=
    (SELECT body_limit FROM service WHERE id=1)
    THEN RAISE(ABORT, 'BODY_CAPACITY') END;
  DELETE FROM rate_hits WHERE bucket < CAST(NEW.created_at / 3600000 AS INTEGER) - 1;
  INSERT INTO rate_hits(client_hash,bucket,hits)
    VALUES(NEW.client_hash, CAST(NEW.created_at / 3600000 AS INTEGER), 1)
    ON CONFLICT(client_hash,bucket) DO UPDATE SET hits=hits+1;
  SELECT CASE WHEN (SELECT hits FROM rate_hits WHERE client_hash=NEW.client_hash
    AND bucket=CAST(NEW.created_at / 3600000 AS INTEGER)) >
    (SELECT hourly_limit FROM service WHERE id=1)
    THEN RAISE(ABORT, 'RATE_LIMITED') END;
END;
CREATE TRIGGER receipt_event AFTER INSERT ON contributions BEGIN
  INSERT INTO events(contribution_id,revision,action,actor,created_at)
    VALUES(NEW.id,1,'received','contributor',NEW.created_at);
END;
