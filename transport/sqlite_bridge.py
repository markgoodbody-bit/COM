"""Tests only: execute adapter SQL/batches against a disposable SQLite file."""
import json
import sqlite3
import sys

packet = json.load(sys.stdin)
db = sqlite3.connect(packet['path'], isolation_level=None)
db.row_factory = sqlite3.Row
db.execute('PRAGMA foreign_keys=ON')
try:
    db.execute('BEGIN IMMEDIATE')
    results = []
    for statement in packet['statements']:
        cursor = db.execute(statement['sql'], statement['args'])
        results.append({'results': [dict(row) for row in cursor.fetchall()]})
    db.execute('COMMIT')
    print(json.dumps(results))
except Exception:
    db.execute('ROLLBACK')
    sys.exit(1)
finally:
    db.close()
