ALTER TABLE service ADD COLUMN correction_limit INTEGER NOT NULL DEFAULT 100 CHECK (correction_limit > 0);

CREATE TABLE correction_requests (
  id TEXT PRIMARY KEY,
  retry_hash TEXT NOT NULL UNIQUE,
  request_hash TEXT NOT NULL,
  manage_hash TEXT NOT NULL,
  target_id TEXT NOT NULL,
  kind TEXT NOT NULL CHECK(kind IN ('privacy','safety','misattribution','other')),
  note TEXT NOT NULL DEFAULT '',
  state TEXT NOT NULL CHECK(state IN ('pending','resolved','withdrawn')),
  operator_outcome TEXT,
  operator_reason TEXT,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  closed_at INTEGER,
  client_hash TEXT NOT NULL,
  mutation_token TEXT
);
CREATE INDEX correction_requests_state ON correction_requests(state);
CREATE INDEX correction_requests_target ON correction_requests(target_id);

CREATE TABLE correction_events (
  id INTEGER PRIMARY KEY,
  correction_id TEXT NOT NULL REFERENCES correction_requests(id) ON DELETE CASCADE,
  action TEXT NOT NULL,
  actor TEXT NOT NULL,
  reason TEXT,
  created_at INTEGER NOT NULL
);

CREATE TABLE correction_rate_hits (
  client_hash TEXT NOT NULL,
  bucket INTEGER NOT NULL,
  hits INTEGER NOT NULL,
  PRIMARY KEY(client_hash, bucket)
);

CREATE TRIGGER correction_guard BEFORE INSERT ON correction_requests BEGIN
  SELECT CASE WHEN (SELECT COUNT(*) FROM correction_requests WHERE state='pending') >=
    (SELECT correction_limit FROM service WHERE id=1)
    THEN RAISE(ABORT, 'CORRECTION_QUEUE_FULL') END;
  DELETE FROM correction_rate_hits WHERE bucket < CAST(NEW.created_at / 3600000 AS INTEGER) - 1;
  INSERT INTO correction_rate_hits(client_hash,bucket,hits)
    VALUES(NEW.client_hash, CAST(NEW.created_at / 3600000 AS INTEGER), 1)
    ON CONFLICT(client_hash,bucket) DO UPDATE SET hits=hits+1;
  SELECT CASE WHEN (SELECT hits FROM correction_rate_hits WHERE client_hash=NEW.client_hash
    AND bucket=CAST(NEW.created_at / 3600000 AS INTEGER)) > 12
    THEN RAISE(ABORT, 'CORRECTION_RATE_LIMITED') END;
END;

CREATE TRIGGER correction_receipt_event AFTER INSERT ON correction_requests BEGIN
  INSERT INTO correction_events(correction_id,action,actor,created_at)
    VALUES(NEW.id,'received','reporter',NEW.created_at);
END;
