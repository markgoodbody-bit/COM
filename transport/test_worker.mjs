import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import worker, {Bus, digest} from './worker.mjs';
import {accountForPage} from './client.mjs';
const root = dirname(fileURLToPath(import.meta.url));
const python = process.env.COM_TEST_PYTHON || 'python';
const a = 'a'.repeat(43), b = 'b'.repeat(43);
function database(path) {
  function execute(statements) {
    const run = spawnSync(python, ['-B', join(root, 'sqlite_bridge.py')], {
      input: JSON.stringify({path, statements}), encoding: 'utf8'});
    if (run.status !== 0) throw new Error('SQLITE_BATCH_REFUSAL');
    return JSON.parse(run.stdout);
  }
  return {
    prepare(sql) {
      return {bind(...args) {
        return {sql, args, async first() {return execute([{sql, args}])[0].results[0] ?? null;}};
      }};
    },
    async batch(statements) {return execute(statements);}
  };
}
async function fixture(action) {
  const dir = mkdtempSync(join(tmpdir(), 'com-contract-'));
  const path = join(dir, 'fixture.db');
  try {
    const setup = spawnSync(python, ['-B', '-c',
      'import sqlite3,sys; db=sqlite3.connect(sys.argv[1]); db.executescript(open(sys.argv[2]).read()); db.close()',
      path, join(root, 'schema.sql')], {encoding:'utf8'});
    assert.equal(setup.status, 0, setup.stderr);
    const db = database(path);
    await db.batch([
      db.prepare('INSERT INTO apertures(id,credential_hash) VALUES (?,?)').bind('codex', await digest(a)),
      db.prepare('INSERT INTO apertures(id,credential_hash) VALUES (?,?)').bind('framework', await digest(b))
    ]);
    await action(db);
  } finally { rmSync(dir, {recursive:true, force:true}); }
}
const send = (key='one', body='synthetic') => ({request_key:key, body, to:'framework'});
const request = (path, token=a, data, method=data ? 'POST':'GET') => new Request('https://com.invalid'+path,
  {method, headers:{Authorization:'Bearer '+token, 'Content-Type':'application/json'},
    ...(data ? {body:JSON.stringify(data)} : {})});

test('adapter duplicate delivery and accepted-write lost response', async () => fixture(async db => {
  const env = {DB:db, WRITES_ENABLED:'true'};
  const first = await worker.fetch(request('/v1/messages', a, send()), env);
  assert.equal(first.status, 200);
  const accepted = await first.json();
  const replay = await (await worker.fetch(request('/v1/messages', a, send()), env)).json();
  assert.equal(replay.seq, accepted.seq);
  assert.equal((await new Bus(db).state(await new Bus(db).actor(a))).head_seq, 1);
  const conflict = await worker.fetch(request('/v1/messages', a, send('one','changed')), env);
  assert.equal(conflict.status, 503);
  assert.equal((await new Bus(db).state(await new Bus(db).actor(a))).head_seq, 1);
}));

test('adapter read crash, exact ack and revoked-in-flight guard', async () => fixture(async db => {
  const bus = new Bus(db), actor = await bus.actor(a), reader = await bus.actor(b);
  await bus.send(actor, send());
  const page = await bus.fetch(reader, 0, 20);
  assert.equal((await bus.state(reader)).consumed, 0);
  await assert.rejects(bus.acknowledge(reader, {receipt:page.receipt,through:1}), /DISPOSITION/);
  await assert.rejects(bus.acknowledge(reader, {receipt:page.receipt,through:2,no_answer_owed:'observed'}));
  await bus.acknowledge(reader, {receipt:page.receipt,through:1,no_answer_owed:'observed'});
  await bus.acknowledge(reader, {receipt:page.receipt,through:1,no_answer_owed:'observed'});
  await assert.rejects(bus.fetch(reader, 0, 20));
  await db.batch([db.prepare('UPDATE apertures SET revoked=1 WHERE id=?').bind('codex')]);
  await assert.rejects(bus.send(actor, send('two')));
  assert.equal((await bus.state(reader)).head_seq, 1);
}));

test('adapter receipt replacement, wrong owner and decision anchors', async () => fixture(async db => {
  const bus = new Bus(db), actor = await bus.actor(a), reader = await bus.actor(b);
  await assert.rejects(bus.send(actor, {...send(),kind:'decision'}), /ANCHOR_REQUIRED/);
  await assert.rejects(bus.send(actor, {...send(),to:'typo'}));
  await bus.send(actor, {...send(),kind:'decision',github_anchor:'https://github.com/markgoodbody-bit/COM/issues/760'});
  const page = await bus.fetch(reader, 0, 20);
  await assert.rejects(bus.acknowledge(actor, {receipt:page.receipt,through:1,no_answer_owed:'observed'}));
  await bus.fetch(reader, 0, 20);
  await assert.rejects(bus.acknowledge(reader, {receipt:page.receipt,through:1,no_answer_owed:'observed'}));
}));

test('client refuses clipped display, omitted disposition, or miscount', () => {
  const page = {messages:[{seq:1},{seq:2}],page_count:2,unread_count:51,head_seq:51,
    server_time:1,has_more:true,consumed:0,through:2,receipt:'synthetic'};
  const dispositions = [1,2].map(seq => ({seq,no_answer_owed:'observed'}));
  assert.equal(accountForPage(page,[1,2],dispositions).through,2);
  assert.throws(() => accountForPage(page,[1],dispositions));
  assert.throws(() => accountForPage(page,[1,2],dispositions.slice(0,1)));
  assert.throws(() => accountForPage({...page,page_count:1},[1,2],dispositions));
  assert.throws(() => accountForPage(page,[1,2],[{seq:1},{seq:2}]));
});

test('HTTP closed writes, auth, bound payload, measured zero, storage failure', async () => fixture(async db => {
  const env = {DB:db, WRITES_ENABLED:'false'};
  assert.equal((await worker.fetch(request('/v1/messages',a,send()),env)).status,503);
  assert.equal((await worker.fetch(request('/v1/state','wrong'),env)).status,401);
  const zero = await (await worker.fetch(request('/v1/messages?after=0',b),env)).json();
  assert.equal(zero.unread_count,0); assert.equal(zero.head_seq,0);
  assert.equal((await worker.fetch(request('/v1/messages',a,send('large','x'.repeat(21000))),{...env,WRITES_ENABLED:'true'})).status,413);
  const failed = await worker.fetch(request('/v1/messages?after=0',b),{DB:{prepare(){throw Error('secret SQL');}}});
  assert.equal(failed.status,503);
  const text = await failed.text();
  assert.ok(text.includes('sync_complete')); assert.ok(!text.includes('secret SQL'));
  assert.equal((await worker.fetch(request('/v1/messages?after=-1',b),env)).status,400);
}));

test('adapter absent aperture catches up with bounded pages on independent connections', async () => fixture(async db => {
  const bus = new Bus(db), actor = await bus.actor(a), reader = await bus.actor(b);
  for (let i=0;i<13;i++) await bus.send(actor,send(String(i)));
  let cursor=0; const seen=[];
  while (true) {
    const page = await bus.fetch(reader,cursor,4);
    if (!page.messages.length) break;
    seen.push(...page.messages.map(row=>row.seq));
    const dispositions=page.messages.map(row=>({seq:row.seq,no_answer_owed:'synthetic'}));
    accountForPage(page,page.messages.map(row=>row.seq),dispositions);
    await bus.acknowledge(reader,{receipt:page.receipt,through:page.through,no_answer_owed:'all synthetic observations'});
    cursor=page.through;
  }
  assert.deepEqual(seen,Array.from({length:13},(_,i)=>i+1));
  assert.equal((await bus.state(reader)).consumed,13);
}));
