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
const rateConfig={SEND_WINDOW_SECONDS:'600',SEND_MAX_ALL:'60',SEND_MAX_SHARED:'12'};

test('local Workers/D1 exchange, rollback, replay, concurrency and restart', async () => {
  const temporary = mkdtempSync(join(tmpdir(),'com-workerd-'));
  const options = {name:'com-contract', modules:true, scriptPath:join(root,'worker.mjs'),
    compatibilityDate:'2026-10-03', d1Databases:{DB:'com-local-fixture'},
    d1Persist:temporary, bindings:{WRITES_ENABLED:'true',...rateConfig}};
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
    const schema = readFileSync(join(root,'schema.sql'),'utf8').replace(/^--.*$/gm,'');
    const statements = schema.match(/\s*CREATE TRIGGER[\s\S]*?END;|[^;]+;/g);
    for (const sql of statements) await db.prepare(sql).run();
    for (const [id,token] of [['codex',codex],['framework',framework]]) {
      await db.prepare('INSERT INTO apertures(id,credential_hash) VALUES (?,?)').bind(id,await digest(token)).run();
    }
    check((await call('/v1/state','wrong')).status,401);
    check((await call('/v1/messages?after=0',framework)).data.unread_count,0);
    check((await call('/v1/head',framework)).data.reason,'HEAD_MISSING');
    for (const [body,code] of [
      ['{"request_key":"ambiguous","body":"a","to":"framework","to":"shared"}','JSON_DUPLICATE_KEY'],
      ['{"request_key":"ambiguous","body":"a","to":"framework","\\u0074o":"shared"}','JSON_DUPLICATE_KEY'],
      ['{"receipt":"x","through":1,"dispositions":[{"seq":1,"seq":2}]}','JSON_DUPLICATE_KEY'],
      ['{"x":'+'['.repeat(33)+'0'+']'.repeat(33)+'}','JSON_DEPTH_BOUND']]) {
      const res=await runtime.dispatchFetch('https://com.invalid/v1/messages', {
        method:'POST',headers:{Authorization:'Bearer '+codex,'Content-Type':'application/json'},body});
      check(res.status,400); check((await res.json()).status,code);
    }
    check((await call('/v1/state')).data.head_seq,0);
    const first=await call('/v1/messages',codex,message()); check(first.status,200);
    check((await call('/v1/messages',codex,message())).data.seq,first.data.seq);
    check((await call('/v1/messages',codex,message('one','conflict'))).status,409);
    check((await call('/v1/state')).data.head_seq,1);
    const page=(await call('/v1/messages?after=0',framework)).data;
    check(page.page_count,1);
    check((await call('/v1/state',framework)).data.consumed,0);
    check((await call('/v1/messages?after=0',codex)).data.unread_count,0);
    check((await call('/v1/history',codex)).data.messages.length,1);
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
    await runtime.setOptions(nativeOptions({...options,bindings:{WRITES_ENABLED:'true',...rateConfig,HEAD_MAX_AGE_SECONDS:'60',HEAD_MAX_LAG:'0'}}));
    db=await runtime.getD1Database('DB');
    await db.prepare('INSERT INTO comhead VALUES(1,1,?,unixepoch(),?,?)').bind(finalHead,'synthetic orientation','https://github.com/markgoodbody-bit/COM/issues/760').run();
    check((await call('/v1/head',framework)).data.freshness,'CURRENT');
    const claude='c'.repeat(43);
    await db.prepare('INSERT INTO apertures(id,credential_hash) VALUES (?,?)').bind('claude',await digest(claude)).run();
    const broadcast=await call('/v1/messages',framework,{...message('broadcast'),to:'shared'});
    check(broadcast.status,200);
    const sharedPage=(await call('/v1/messages?after=0',claude)).data;
    check(sharedPage.page_count,1);
    check(sharedPage.messages[0].recipient,'shared');
    check((await call('/v1/ack',claude,{receipt:sharedPage.receipt,through:sharedPage.through,
      dispositions:[{seq:sharedPage.through,no_answer_owed:'synthetic broadcast'}]})).status,200);
    check((await call('/v1/head',framework)).data.freshness,'STALE');
    const catchup=(await call('/v1/messages?after=1&limit=3',framework)).data;
    check([catchup.page_count,catchup.unread_count,catchup.has_more],[3,9,true]);
    check((await call('/v1/history?after=0',framework)).data.messages.length,10);
    check((await db.prepare('SELECT COUNT(*) AS n FROM acknowledgements').first()).n,2);
    check((await call('/v1/ack',framework,ack)).status,200);
    // Tight synthetic limits test the same configured atomic boundary, not
    // elapsed wall-clock sleeps or an operator-side check-then-write.
    await runtime.setOptions(nativeOptions({...options,bindings:{WRITES_ENABLED:'true',
      SEND_WINDOW_SECONDS:'600',SEND_MAX_ALL:'3',SEND_MAX_SHARED:'2'}}));
    db=await runtime.getD1Database('DB');
    const shared = key=>({...message(key),to:'shared'});
    const r1=await call('/v1/messages',claude,shared('cap1')); check(r1.status,200);
    check((await call('/v1/messages',claude,shared('cap2'))).status,200);
    const beforeLimit=await db.prepare("SELECT seq FROM sqlite_sequence WHERE name='messages'").first();
    const rejected=await call('/v1/messages',claude,shared('cap3'));
    check(rejected.status,429); check(rejected.data.status,'RATE_LIMITED');
    check(rejected.data.retry_after_seconds>=1 && rejected.data.retry_after_seconds<=600,true);
    check(await db.prepare("SELECT seq FROM sqlite_sequence WHERE name='messages'").first(),beforeLimit);
    check((await call('/v1/messages',claude,message('direct-cap'))).status,200);
    check((await call('/v1/messages',claude,message('all-refusal'))).status,429);
    check((await call('/v1/messages',claude,shared('cap1'))).data.seq,r1.data.seq);
    check((await call('/v1/messages',claude,{...shared('cap1'),body:'changed'})).status,409);
    check((await db.prepare("SELECT COUNT(*) AS n FROM messages WHERE sender='claude'").first()).n,3);
    check((await call('/v1/messages?after='+sharedPage.through,claude)).data.messages.every(m=>m.delivery==='shared'),true);
    const racer='d'.repeat(43),other='e'.repeat(43),expired='f'.repeat(43);
    for (const [id,token] of [['racer',racer],['other',other],['expired',expired]]) {
      await db.prepare('INSERT INTO apertures(id,credential_hash) VALUES (?,?)').bind(id,await digest(token)).run();
    }
    const races=await Promise.all(Array.from({length:8},(_,i)=>call('/v1/messages',racer,shared('race'+i))));
    check(races.filter(r=>r.status===200).length,2);
    check(races.filter(r=>r.status===429).length,6);
    check((await db.prepare("SELECT COUNT(*) AS n FROM messages WHERE sender='racer'").first()).n,2);
    check((await call('/v1/messages',other,shared('independent'))).status,200);
    for (let i=0;i<3;i++) await db.prepare(`INSERT INTO messages(sender,recipient,kind,request_key,body,received_at)
      VALUES('expired','shared','message',?,'synthetic expired',unixepoch()-600)`).bind('expired'+i).run();
    check((await call('/v1/messages',expired,shared('new-window'))).status,200);
    await runtime.setOptions(nativeOptions({...options,bindings:{WRITES_ENABLED:'true',...rateConfig}}));
    db=await runtime.getD1Database('DB');
    const trial='g'.repeat(43);
    await db.prepare('INSERT INTO apertures(id,credential_hash) VALUES (?,?)').bind('trial',await digest(trial)).run();
    const broadcasts=await Promise.all(Array.from({length:60},(_,i)=>call('/v1/messages',trial,shared('trial-shared'+i))));
    check(broadcasts.filter(r=>r.status===200).length,12);
    check(broadcasts.filter(r=>r.status===429).length,48);
    const directs=await Promise.all(Array.from({length:50},(_,i)=>call('/v1/messages',trial,message('trial-direct'+i))));
    check(directs.filter(r=>r.status===200).length,48);
    check(directs.filter(r=>r.status===429).length,2);
    check((await db.prepare("SELECT COUNT(*) AS n FROM messages WHERE sender='trial'").first()).n,60);
    const rateHead=(await call('/v1/state',framework)).data.head_seq;
    check((await db.prepare('SELECT COUNT(*) AS n FROM acknowledgements').first()).n,2);
    await runtime.setOptions(nativeOptions({...options,bindings:{WRITES_ENABLED:'false'}}));
    check((await call('/v1/messages',framework,message('closed'))).status,503);
    check((await call('/v1/state',framework)).data.head_seq,rateHead);
    console.log(JSON.stringify({status:'LOCAL_WORKER_D1_PASS_NOT_HOSTED_PASS',checks,
      synthetic_only:true,remote_resources_created:0,real_aperture_exchange:false}));
  } finally {
    if (runtime) await runtime.dispose();
    rmSync(temporary,{recursive:true,force:true});
  }
});
