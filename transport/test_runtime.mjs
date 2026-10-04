// Actual local workerd + Miniflare D1 binding; no remote provider calls.
import {createRequire} from 'node:module';
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, readFileSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {digest} from './worker.mjs';
import {accountForPage} from './client.mjs';
const require = createRequire(import.meta.url);
const {Miniflare, convertV4MiniflareOptions} = require(process.env.COM_MINIFLARE_MODULE || 'miniflare');
const nativeOptions = options => ({...convertV4MiniflareOptions(options),
  resourcePersistencePath:options.d1Persist, telemetry:{enabled:false},logRequests:false});
const root = dirname(fileURLToPath(import.meta.url));
const codex = 'a'.repeat(43), framework = 'b'.repeat(43);

test('local Workers/D1 exchange, rollback, replay, concurrency and restart', async () => {
  const temporary = mkdtempSync(join(tmpdir(),'com-workerd-'));
  const options = {name:'com-contract', modules:true, scriptPath:join(root,'worker.mjs'),
    compatibilityDate:'2026-10-03', d1Databases:{DB:'com-local-fixture'},
    d1Persist:temporary, bindings:{WRITES_ENABLED:'true'}};
  let runtime;
  let checks=0;
  function check(actual, expected) { assert.deepEqual(actual,expected); checks++; }
  async function call(path, token=codex, body) {
    const res = await runtime.dispatchFetch('https://com.invalid'+path, {
      method:body ? 'POST':'GET', headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},
      ...(body ? {body:JSON.stringify(body)} : {})});
    return {status:res.status, data:await res.json()};
  }
  const message = (key='one',body='synthetic')=>({request_key:key,body,to:'framework'});
  try {
    runtime = new Miniflare(nativeOptions(options));
    let db = await runtime.getD1Database('DB');
    const schema = readFileSync(join(root,'schema.sql'),'utf8');
    const statements = schema.match(/\s*CREATE TRIGGER[\s\S]*?END;|[^;]+;/g);
    for (const sql of statements) await db.prepare(sql).run();
    for (const [id,token] of [['codex',codex],['framework',framework]]) {
      await db.prepare('INSERT INTO apertures(id,credential_hash) VALUES (?,?)').bind(id,await digest(token)).run();
    }
    check((await call('/v1/state','wrong')).status,401);
    check((await call('/v1/messages?after=0',framework)).data.unread_count,0);
    const first=await call('/v1/messages',codex,message()); check(first.status,200);
    check((await call('/v1/messages',codex,message())).data.seq,first.data.seq);
    check((await call('/v1/messages',codex,message('one','conflict'))).status,409);
    check((await call('/v1/state')).data.head_seq,1);
    const page=(await call('/v1/messages?after=0',framework)).data;
    check(page.page_count,1);
    check((await call('/v1/state',framework)).data.consumed,0);
    check((await call('/v1/ack',framework,{receipt:page.receipt,through:1})).status,400);
    check((await call('/v1/ack',framework,{receipt:page.receipt,through:2,dispositions:[{seq:1,no_answer_owed:'synthetic'}]})).status,503);
    check((await call('/v1/state',framework)).data.consumed,0);
    accountForPage(page,[1],[{seq:1,no_answer_owed:'synthetic'}]);
    const ack={receipt:page.receipt,through:1,dispositions:[{seq:1,no_answer_owed:'synthetic'}]};
    check((await call('/v1/ack',framework,ack)).status,200);
    check((await call('/v1/ack',framework,ack)).status,200);
    check((await call('/v1/messages?after=0',framework)).status,503);
    const concurrent=await Promise.all(Array.from({length:8},(_,i)=>call('/v1/messages',i%2?codex:framework,message('writer'+i))));
    check(concurrent.map(r=>r.status),Array(8).fill(200));
    const sequences=concurrent.map(r=>r.data.seq).sort((a,b)=>a-b);
    check(new Set(sequences).size,8);
    check(sequences.every((seq,i)=>seq>(i?sequences[i-1]:first.data.seq)),true);
    const finalHead=sequences.at(-1);
    await assert.rejects(db.prepare('DELETE FROM messages').run()); checks++;
    await db.prepare("UPDATE apertures SET revoked=1 WHERE id='codex'").run();
    check((await call('/v1/messages',codex,message('revoked'))).status,401);
    await runtime.dispose(); runtime=undefined;
    runtime=new Miniflare(nativeOptions(options));
    db=await runtime.getD1Database('DB');
    check((await call('/v1/state',framework)).data.consumed,1);
    check((await call('/v1/state',framework)).data.head_seq,finalHead);
    const catchup=(await call('/v1/messages?after=1&limit=3',framework)).data;
    check([catchup.page_count,catchup.unread_count,catchup.has_more],[3,8,true]);
    check((await call('/v1/history?after=0',framework)).data.messages.length,9);
    check((await db.prepare('SELECT COUNT(*) AS n FROM acknowledgements').first()).n,1);
    check((await call('/v1/ack',framework,ack)).status,200);
    await runtime.setOptions(nativeOptions({...options,bindings:{WRITES_ENABLED:'false'}}));
    check((await call('/v1/messages',framework,message('closed'))).status,503);
    check((await call('/v1/state',framework)).data.head_seq,finalHead);
    console.log(JSON.stringify({status:'LOCAL_WORKER_D1_PASS_NOT_HOSTED_PASS',checks,
      synthetic_only:true,remote_resources_created:0,real_aperture_exchange:false}));
  } finally {
    if (runtime) await runtime.dispose();
    rmSync(temporary,{recursive:true,force:true});
  }
});
