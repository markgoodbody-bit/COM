import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {SqliteAdapter} from '../src/sqlite-adapter.js';
import {Store,newKey} from '../src/store.js';

const fixed=Date.parse('2026-09-08T15:00:00Z');
const draft=()=>({body:'audit-marker-independent',display_name:'Invented reader',retry_key:newKey(),management_key:newKey()});

test('audit events do not depend on connection-scoped changes() carrying between batch statements',async t=>{
  const dir=mkdtempSync(join(tmpdir(),'psfh-portability-')),path=join(dir,'test.sqlite');
  const db=new SqliteAdapter(path),store=new Store(db,()=>fixed);
  t.after(()=>{db.close();rmSync(dir,{recursive:true,force:true});});
  await store.readiness(true);

  // Deliberately reset SQLite changes() to zero after every statement in a batch.
  // The old audit-event pattern (`... WHERE changes()=1`) loses events here.
  db.batch=async statements=>{
    db.sql.exec('BEGIN IMMEDIATE');
    try {
      const results=[];
      for(const statement of statements){
        results.push(statement.execute());
        db.sql.prepare('UPDATE service SET enabled=enabled WHERE id=0').run();
      }
      db.sql.exec('COMMIT');
      return results;
    } catch(error){
      db.sql.exec('ROLLBACK');
      throw error;
    }
  };

  const input=draft(),r=await store.submit(input,'audit-client');
  await store.revise(r.id,input.management_key,{body:'revision two',revision:1});
  await store.moderate(r.id,{action:'decline',revision:2,reason:'synthetic decline'},'operator');
  await store.reconsider(r.id,input.management_key,'synthetic reconsideration');
  await store.moderate(r.id,{action:'publish',revision:2,reason:'synthetic publish'},'operator');
  await store.withdraw(r.id,input.management_key);

  const actions=db.sql.prepare('SELECT action FROM events WHERE contribution_id=? ORDER BY id').all(r.id).map(x=>x.action);
  assert.deepEqual(actions,['received','revised','decline','reconsideration','publish','withdrawn']);
});
