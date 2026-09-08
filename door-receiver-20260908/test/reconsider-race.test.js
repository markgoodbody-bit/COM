import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {SqliteAdapter} from '../src/sqlite-adapter.js';
import {Store,newKey,Problem} from '../src/store.js';

const fixed=Date.parse('2026-09-08T18:00:00Z');

/** A store whose next batch() runs one injected mutation first. That is the
 *  window a second actor occupies between a guard read and its write. */
function fixture(t,{onNextBatch=null}={}){
  const dir=mkdtempSync(join(tmpdir(),'psfh-reconsider-')),db=new SqliteAdapter(join(dir,'test.sqlite'));
  let pending=onNextBatch;
  const real=db.batch.bind(db);
  db.batch=async stmts=>{if(pending){const h=pending;pending=null;await h();}return real(stmts);};
  const store=new Store(db,()=>fixed);
  t.after(()=>{db.close();rmSync(dir,{recursive:true,force:true});});
  return {db,store,arm(h){pending=h;}};
}

async function declined(store,keys){
  await store.readiness(true);
  const r=await store.submit({body:'a contribution',display_name:'',
    management_key:keys.manage,retry_key:keys.retry},'client-reconsider');
  await store.moderate(r.id,{action:'decline',revision:1,reason:'not yet'},'moderator');
  return r.id;
}

test('reconsideration refuses a zero-change write instead of reporting false success',async t=>{
  const f=fixture(t),keys={manage:newKey(),retry:newKey()};
  const id=await declined(f.store,keys);
  const before=await f.store.receipt(id,keys.manage);
  assert.equal(before.state,'declined');

  // Legal interleaving: the contributor replaces the body from another window
  // between reconsider()'s guard read and its write. declined -> pending is
  // permitted, so the row moves and reconsider's UPDATE can no longer match.
  f.arm(async()=>{
    await f.store.revise(id,keys.manage,{body:'replaced meanwhile',display_name:'',revision:before.revision});
  });

  await assert.rejects(
    f.store.reconsider(id,keys.manage,'please look again'),
    e=>e instanceof Problem&&e.code==='NOT_RECONSIDERABLE',
    'a reconsideration that changed no row must refuse, not return a receipt');

  const row=f.db.sql.prepare('SELECT state,reconsideration FROM contributions WHERE id=?').get(id);
  assert.equal(row.reconsideration,0,'no reconsideration flag may be left set');
  assert.equal(f.db.sql.prepare(
    "SELECT COUNT(*) AS n FROM events WHERE contribution_id=? AND action='reconsideration'").get(id).n,
    0,'no reconsideration event may be recorded for a write that changed nothing');
});

test('an ordinary reconsideration still succeeds and is recorded',async t=>{
  const f=fixture(t),keys={manage:newKey(),retry:newKey()};
  const id=await declined(f.store,keys);
  const view=await f.store.reconsider(id,keys.manage,'please look again');
  assert.equal(view.reconsideration,true);
  assert.equal(f.db.sql.prepare(
    "SELECT COUNT(*) AS n FROM events WHERE contribution_id=? AND action='reconsideration'").get(id).n,1);
});

test('withdrawal stays idempotent and does not adopt the stricter refusal',async t=>{
  const f=fixture(t),keys={manage:newKey(),retry:newKey()};
  const id=await declined(f.store,keys);
  const first=await f.store.withdraw(id,keys.manage);
  assert.equal(first.state,'withdrawn');
  // A second withdrawal asks for the state it is already in; it must return a
  // receipt rather than refuse. The repair is deliberately not applied here.
  const second=await f.store.withdraw(id,keys.manage);
  assert.equal(second.state,'withdrawn');
  assert.equal(f.db.sql.prepare(
    "SELECT COUNT(*) AS n FROM events WHERE contribution_id=? AND action='withdrawn'").get(id).n,
    1,'an idempotent second withdrawal must not append a second event');
});

// HISTORY, not a passing case. The first probe injected a publish, which is
// illegal from 'declined' and was refused by moderate() before reaching the
// window. It demonstrated nothing, and is recorded so the interleaving that
// does work is not mistaken for the only one attempted.
test('illegal publish injection cannot construct this race',async t=>{
  const f=fixture(t),keys={manage:newKey(),retry:newKey()};
  const id=await declined(f.store,keys);
  const before=await f.store.receipt(id,keys.manage);
  await assert.rejects(
    f.store.moderate(id,{action:'publish',revision:before.revision,reason:'changed mind'},'moderator'),
    e=>e instanceof Problem&&e.code==='MODERATION_STATE_CONFLICT',
    'publish from declined is refused, so this injection never reaches the window');
});
