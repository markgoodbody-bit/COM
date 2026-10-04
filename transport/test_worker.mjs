import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import worker, {Bus, digest, parsePayloadJson} from './worker.mjs';
import {accountForPage} from './client.mjs';
import {advanceCheckpoint} from './recovery.mjs';
const root = dirname(fileURLToPath(import.meta.url));
const python = process.env.COM_TEST_PYTHON || 'python';
const a = 'a'.repeat(43), b = 'b'.repeat(43);
const testEpoch='1'.repeat(32);
const rateConfig={TRANSPORT_EPOCH:testEpoch,SEND_WINDOW_SECONDS:'600',SEND_MAX_ALL:'60',SEND_MAX_SHARED:'12',SHARED_LONG_WINDOW_SECONDS:'86400',SHARED_LONG_MAX:'60'};
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
      db.prepare('INSERT INTO transport_meta(id,epoch) VALUES(1,?)').bind(testEpoch),
      db.prepare('INSERT INTO apertures(id,credential_hash) VALUES (?,?)').bind('codex', await digest(a)),
      db.prepare('INSERT INTO apertures(id,credential_hash) VALUES (?,?)').bind('framework', await digest(b))
    ]);
    await action(db);
  } finally { rmSync(dir, {recursive:true, force:true}); }
}
const send = (key='one', body='synthetic') => ({request_key:key, body, to:'framework'});
const request = (path, token=a, data, method=data ? 'POST':'GET') => new Request('https://com.invalid'+path,
  {method, headers:{Authorization:'Bearer '+token, 'Content-Type':'application/json','X-COM-Epoch':testEpoch},
    ...(data ? {body:JSON.stringify(data)} : {})});

test('request JSON rejects duplicate decoded keys and excessive nesting', () => {
  for (const source of ['{"to":"codex","to":"shared"}',
    '{"to":"codex","\\u0074o":"shared"}',
    '{"dispositions":[{"seq":1,"seq":2}]}']) {
    assert.throws(() => parsePayloadJson(source), /JSON_DUPLICATE_KEY/);
  }
  assert.throws(() => parsePayloadJson('{"x":'+'['.repeat(33)+'0'+']'.repeat(33)+'}'), /JSON_DEPTH_BOUND/);
  assert.deepEqual(parsePayloadJson('{"body":"escaped \\" key: to","x":[{"seq":1},{"seq":2}]}'),
    {body:'escaped " key: to',x:[{seq:1},{seq:2}]});
  assert.throws(() => parsePayloadJson('{"to":}'));
  assert.throws(() => parsePayloadJson('[]'), /JSON_INVALID/);
});

test('sender limits refuse atomically while exact replay remains available', async () => fixture(async db => {
  const env={DB:db,WRITES_ENABLED:'true',...rateConfig,SEND_MAX_ALL:'3',SEND_MAX_SHARED:'2'};
  const shared=key=>({...send(key),to:'shared'});
  for (const key of ['cap1','cap2']) assert.equal((await worker.fetch(request('/v1/messages',a,shared(key)),env)).status,200);
  const before=await db.prepare("SELECT seq FROM sqlite_sequence WHERE name='messages'").bind().first();
  const refused=await worker.fetch(request('/v1/messages',a,shared('refused')),env);
  assert.equal(refused.status,429);
  const detail=await refused.json(); assert.equal(detail.status,'RATE_LIMITED');
  assert.ok(detail.retry_after_seconds>=1 && detail.retry_after_seconds<=600);
  assert.deepEqual(await db.prepare("SELECT seq FROM sqlite_sequence WHERE name='messages'").bind().first(),before);
  assert.equal((await worker.fetch(request('/v1/messages',a,send('direct')),env)).status,200);
  assert.equal((await worker.fetch(request('/v1/messages',a,send('fourth')),env)).status,429);
  assert.equal((await worker.fetch(request('/v1/messages',a,shared('cap1')),env)).status,200);
  assert.equal((await worker.fetch(request('/v1/messages',a,{...shared('cap1'),body:'conflict'}),env)).status,409);
  assert.equal((await worker.fetch(request('/v1/messages',a,send('unconfigured')),{DB:db,WRITES_ENABLED:'true',TRANSPORT_EPOCH:testEpoch})).status,503);
  assert.equal((await db.prepare('SELECT COUNT(*) AS n FROM messages').bind().first()).n,3);
}));

test('separate head capability rejects ordinary auth, extra authority and stale writers', async () => fixture(async db => {
  const token='h'.repeat(43),bus=new Bus(db,rateConfig);
  await db.batch([db.prepare("INSERT INTO head_capabilities VALUES('comhead_writer','codex',?,0)").bind(await digest(token))]);
  const env={DB:db,WRITES_ENABLED:'true',HEAD_WRITES_ENABLED:'true',...rateConfig};
  const data={expected_version:0,basis_seq:0,body:'synthetic head',github_anchor:'https://github.com/markgoodbody-bit/COM/issues/760'};
  assert.equal((await worker.fetch(request('/v1/head',a,data),env)).status,401);
  assert.equal((await worker.fetch(request('/v1/messages',token,send()),env)).status,401);
  assert.equal((await worker.fetch(request('/v1/head',token,{...data,consumed:4}),env)).status,400);
  assert.equal((await worker.fetch(request('/v1/head',token,{...data,github_anchor:null}),env)).status,400);
  assert.equal((await worker.fetch(request('/v1/head',token,data),{...env,HEAD_WRITES_ENABLED:'false'})).status,503);
  assert.equal((await worker.fetch(request('/v1/head',token,data),env)).status,200);
  assert.equal((await worker.fetch(request('/v1/head',token,data),env)).status,409);
  const writer=await bus.headWriter(token);
  await db.batch([db.prepare("UPDATE head_capabilities SET revoked=1").bind()]);
  await assert.rejects(bus.writeHead(writer,{...data,expected_version:1}), /SQLITE_BATCH_REFUSAL/);
  assert.equal((await db.prepare('SELECT COUNT(*) AS n FROM head_audit').bind().first()).n,1);
  assert.equal((await bus.state(await bus.actor(a))).consumed,0);
  assert.equal((await bus.state(await bus.actor(a))).head_seq,0);
  await assert.rejects(db.batch([db.prepare('DELETE FROM head_audit').bind()]));
}));

test('long shared window blocks slow sends but not directs or retained replays', async () => fixture(async db => {
  const env={DB:db,WRITES_ENABLED:'true',...rateConfig,SHARED_LONG_MAX:'2'};
  await db.batch([0,1].map(i=>db.prepare(`INSERT INTO messages(sender,recipient,kind,request_key,body,received_at)
    VALUES('codex','shared','message',?,'synthetic',unixepoch()-601)`).bind('old'+i)));
  const shared=key=>({...send(key),to:'shared'});
  const refused=await worker.fetch(request('/v1/messages',a,shared('new')),env);
  assert.equal(refused.status,429);
  const body=await refused.json(); assert.equal(body.status,'RATE_LIMITED');
  assert.ok(body.retry_after_seconds>600 && body.retry_after_seconds<=86400);
  assert.equal((await worker.fetch(request('/v1/messages',a,send('direct')),env)).status,200);
  assert.equal((await worker.fetch(request('/v1/messages',a,shared('old0')),env)).status,200);
  assert.equal((await worker.fetch(request('/v1/messages',b,shared('other')),env)).status,200);
  assert.equal((await db.prepare("SELECT COUNT(*) AS n FROM messages WHERE sender='codex' AND recipient='shared'").bind().first()).n,2);
}));

test('epoch mismatch and explicit history floor never silently consume', async () => fixture(async db => {
  const bus=new Bus(db,rateConfig),actor=await bus.actor(a),reader=await bus.actor(b);
  await bus.send(actor,send());
  const checkpoint={expected_epoch:testEpoch,expected_checkpoint:0,new_epoch:'2'.repeat(32),retained_after:1,
    archive_sha256:'a'.repeat(64),github_anchor:'https://github.com/markgoodbody-bit/COM/issues/760'};
  await advanceCheckpoint(db,checkpoint);
  await assert.rejects(bus.send(actor,send('stale')), /SQLITE_BATCH_REFUSAL/);
  await assert.rejects(advanceCheckpoint(db,checkpoint), /SQLITE_BATCH_REFUSAL/);
  const env={DB:db,WRITES_ENABLED:'true',...rateConfig,TRANSPORT_EPOCH:checkpoint.new_epoch};
  assert.equal((await worker.fetch(request('/v1/messages?after=0',b),env)).status,409);
  const current=request('/v1/messages?after=0',b); current.headers.set('X-COM-Epoch',checkpoint.new_epoch);
  const response=await worker.fetch(current,env); assert.equal(response.status,409);
  assert.equal((await response.json()).status,'GAP');
  const observe=request('/v1/recovery',b); observe.headers.delete('X-COM-Epoch');
  const recovery=await (await worker.fetch(observe,env)).json();
  assert.equal(recovery.recovery_mode,'CHECKPOINT_BOOTSTRAP_REQUIRED');
  assert.equal(recovery.consumed,0); assert.equal(recovery.checkpoint.version,1);
  assert.equal((await bus.state(reader)).consumed,0);
}));

test('adapter duplicate delivery and accepted-write lost response', async () => fixture(async db => {
  const env = {DB:db, WRITES_ENABLED:'true',...rateConfig};
  const first = await worker.fetch(request('/v1/messages', a, send()), env);
  assert.equal(first.status, 200);
  const accepted = await first.json();
  const replay = await (await worker.fetch(request('/v1/messages', a, send()), env)).json();
  assert.equal(replay.seq, accepted.seq);
  assert.equal((await new Bus(db).state(await new Bus(db).actor(a))).head_seq, 1);
  const conflict = await worker.fetch(request('/v1/messages', a, send('one','changed')), env);
  assert.equal(conflict.status, 409);
  assert.equal((await new Bus(db).state(await new Bus(db).actor(a))).head_seq, 1);
}));

test('adapter read crash, exact ack and revoked-in-flight guard', async () => fixture(async db => {
  const bus = new Bus(db,rateConfig), actor = await bus.actor(a), reader = await bus.actor(b);
  await bus.send(actor, send());
  const page = await bus.fetch(reader, 0, 20);
  assert.equal((await bus.state(reader)).consumed, 0);
  await assert.rejects(bus.acknowledge(reader, {receipt:page.receipt,through:1}), /DISPOSITION/);
  await assert.rejects(bus.acknowledge(reader, {receipt:page.receipt,through:2,dispositions:[{seq:1,no_answer_owed:'observed'}]}));
  await bus.acknowledge(reader, {receipt:page.receipt,through:1,dispositions:[{seq:1,no_answer_owed:'observed'}]});
  await bus.acknowledge(reader, {receipt:page.receipt,through:1,dispositions:[{seq:1,no_answer_owed:'observed'}]});
  await assert.rejects(bus.fetch(reader, 0, 20));
  await db.batch([db.prepare('UPDATE apertures SET revoked=1 WHERE id=?').bind('codex')]);
  await assert.rejects(bus.send(actor, send('two')));
  assert.equal((await bus.state(reader)).head_seq, 1);
}));

test('adapter receipt replacement, wrong owner and decision anchors', async () => fixture(async db => {
  const bus = new Bus(db,rateConfig), actor = await bus.actor(a), reader = await bus.actor(b);
  await assert.rejects(bus.send(actor, {...send(),kind:'decision'}), /ANCHOR_REQUIRED/);
  await assert.rejects(bus.send(actor, {...send(),to:'typo'}));
  await bus.send(actor, {...send(),kind:'decision',github_anchor:'https://github.com/markgoodbody-bit/COM/issues/760'});
  const page = await bus.fetch(reader, 0, 20);
  await assert.rejects(bus.acknowledge(actor, {receipt:page.receipt,through:1,dispositions:[{seq:1,no_answer_owed:'observed'}]}));
  await bus.fetch(reader, 0, 20);
  await assert.rejects(bus.acknowledge(reader, {receipt:page.receipt,through:1,dispositions:[{seq:1,no_answer_owed:'observed'}]}));
}));

test('client refuses clipped display, omitted disposition, or miscount', () => {
  const page = {epoch:testEpoch,messages:[{seq:1},{seq:2}],page_count:2,unread_count:51,head_seq:51,
    server_time:1,has_more:true,consumed:0,through:2,receipt:'synthetic'};
  const dispositions = [1,2].map(seq => ({seq,no_answer_owed:'observed'}));
  assert.equal(accountForPage(page,[1,2],dispositions).through,2);
  assert.equal(accountForPage(page,[1,2],dispositions).epoch,testEpoch);
  assert.throws(() => accountForPage({...page,epoch:null},[1,2],dispositions));
  assert.throws(() => accountForPage(page,[1],dispositions));
  assert.throws(() => accountForPage(page,[1,2],dispositions.slice(0,1)));
  assert.throws(() => accountForPage({...page,page_count:1},[1,2],dispositions));
  assert.throws(() => accountForPage(page,[1,2],[{seq:1},{seq:2}]));
});

test('HTTP closed writes, auth, bound payload, measured zero, storage failure', async () => fixture(async db => {
  const env = {DB:db, WRITES_ENABLED:'false',TRANSPORT_EPOCH:testEpoch};
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
  const bus = new Bus(db,rateConfig), actor = await bus.actor(a), reader = await bus.actor(b);
  for (let i=0;i<13;i++) await bus.send(actor,send(String(i)));
  let cursor=0; const seen=[];
  while (true) {
    const page = await bus.fetch(reader,cursor,4);
    if (!page.messages.length) break;
    seen.push(...page.messages.map(row=>row.seq));
    const dispositions=page.messages.map(row=>({seq:row.seq,no_answer_owed:'synthetic'}));
    accountForPage(page,page.messages.map(row=>row.seq),dispositions);
    await bus.acknowledge(reader,{receipt:page.receipt,through:page.through,dispositions});
    cursor=page.through;
  }
  assert.deepEqual(seen,Array.from({length:13},(_,i)=>i+1));
  assert.equal((await bus.state(reader)).consumed,13);
}));

test('CC regressions: durable per-message ack, history and permanent errors', async () => fixture(async db => {
  const bus=new Bus(db,rateConfig),actor=await bus.actor(a),reader=await bus.actor(b);
  await bus.send(actor,send('one'));
  await bus.send(actor,send('two'));
  const page=await bus.fetch(reader,0,20);
  const dispositions=page.messages.map(row=>({seq:row.seq,no_answer_owed:'synthetic '+row.seq}));
  await assert.rejects(bus.acknowledge(reader,{receipt:page.receipt,through:page.through,dispositions:dispositions.slice(0,1)}));
  assert.equal((await bus.state(reader)).consumed,0);
  await bus.acknowledge(reader,{receipt:page.receipt,through:page.through,dispositions});
  await bus.fetch(reader,page.through,20);
  const kept=(await db.batch([db.prepare('SELECT * FROM acknowledgements ORDER BY seq').bind()]))[0].results;
  assert.equal(kept.length,2);
  assert.deepEqual(kept.map(row=>JSON.parse(row.disposition)),dispositions);
  await bus.acknowledge(reader,{receipt:page.receipt,through:page.through,dispositions});
  const history=await bus.history(reader,0,20);
  assert.equal(history.messages.length,2); assert.equal(history.history_only,true);
  assert.deepEqual(history.messages.map(row=>JSON.parse(row.my_disposition)),dispositions);
  assert.equal(history.receipt,undefined); assert.equal((await bus.state(reader)).consumed,page.through);
  const env={DB:db,WRITES_ENABLED:'true',...rateConfig};
  assert.equal((await worker.fetch(request('/v1/messages',a,{...send('x'),to:'nobody'}),env)).status,400);
  assert.equal((await worker.fetch(request('/v1/messages',a,send('one','changed')),env)).status,409);
  await assert.rejects(db.batch([db.prepare('DELETE FROM acknowledgements').bind()]));
}));

test('actionable inbox separates direct destination from shared visibility', async () => fixture(async db => {
  const bus=new Bus(db,rateConfig),actor=await bus.actor(a),reader=await bus.actor(b);
  await bus.send(actor,send('direct'));
  const shared=await bus.send(actor,{...send('broadcast'),to:'shared'});
  const mine=await bus.fetch(actor,0,20),theirs=await bus.fetch(reader,0,20);
  assert.equal(mine.messages.length,1); assert.equal(mine.messages[0].recipient,'shared');
  assert.equal(mine.messages[0].to_me,0); assert.equal(theirs.messages.length,2);
  assert.equal(theirs.messages[0].to_me,1);
  await assert.rejects(bus.acknowledge(actor,{receipt:mine.receipt,through:shared.seq,
    dispositions:[{seq:1,no_answer_owed:'not delivered'}]}));
  await bus.acknowledge(actor,{receipt:mine.receipt,through:shared.seq,
    dispositions:[{seq:shared.seq,no_answer_owed:'broadcast observed'}]});
  assert.equal((await bus.history(actor,0,20)).messages.length,2);
  assert.equal((await bus.fetch(actor,shared.seq,20)).unread_count,0);
}));

test('COMHEAD missing, bounds unset, stale age/lag and invalid future basis', async () => fixture(async db => {
  const bus=new Bus(db,rateConfig),actor=await bus.actor(a);
  assert.equal((await bus.head(actor,{})).reason,'HEAD_MISSING');
  await db.batch([db.prepare('INSERT INTO comhead VALUES(1,1,0,unixepoch(),?,?)').bind('orientation','https://github.com/markgoodbody-bit/COM/issues/760')]);
  assert.equal((await bus.head(actor,{})).freshness,'UNKNOWN');
  const bounds={HEAD_MAX_AGE_SECONDS:'60',HEAD_MAX_LAG:'0'};
  assert.equal((await bus.head(actor,bounds)).freshness,'CURRENT');
  await bus.send(actor,send());
  assert.equal((await bus.head(actor,bounds)).freshness,'STALE');
  await db.batch([db.prepare('UPDATE comhead SET basis_seq=1,updated_at=unixepoch()-120').bind()]);
  assert.equal((await bus.head(actor,bounds)).freshness,'STALE');
  await db.batch([db.prepare('UPDATE comhead SET basis_seq=999,updated_at=unixepoch()').bind()]);
  assert.equal((await bus.head(actor,bounds)).reason,'HEAD_BASIS_INVALID');
}));
