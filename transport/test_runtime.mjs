// Actual local workerd + Miniflare D1 binding; no remote provider calls.
import {createRequire} from 'node:module';
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, readFileSync, writeFileSync, rmSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {tmpdir} from 'node:os';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {digest} from './worker.mjs';
import {accountForPage} from './client.mjs';
import {advanceCheckpoint} from './recovery.mjs';
import {exportArchive,verifyArchive,restoreArchive,archiveHistory} from './archive.mjs';
const require = createRequire(import.meta.url);
const {Miniflare, convertV4MiniflareOptions} = require(process.env.COM_MINIFLARE_MODULE || 'miniflare');
const nativeOptions = options => ({...convertV4MiniflareOptions(options),
  resourcePersistencePath:options.d1Persist, telemetry:{enabled:false},logRequests:false});
const root = dirname(fileURLToPath(import.meta.url));
const codex = 'a'.repeat(43), framework = 'b'.repeat(43);
const testEpoch='1'.repeat(32);
const rateConfig={TRANSPORT_EPOCH:testEpoch,SEND_WINDOW_SECONDS:'600',SEND_MAX_ALL:'60',SEND_MAX_SHARED:'12',SHARED_LONG_WINDOW_SECONDS:'86400',SHARED_LONG_MAX:'60'};

test('local Workers/D1 exchange, rollback, replay, concurrency and restart', async () => {
  const temporary = mkdtempSync(join(tmpdir(),'com-workerd-'));
  const options = {name:'com-contract', modules:true, scriptPath:join(root,'worker.mjs'),
    compatibilityDate:'2026-10-03', d1Databases:{DB:'com-local-fixture'},
    d1Persist:temporary, bindings:{WRITES_ENABLED:'true',...rateConfig}};
  let runtime,restoredRuntime;
  let checks=0;
  function check(actual, expected) { assert.deepEqual(actual,expected); checks++; }
  async function call(path, token=codex, body, epoch=testEpoch) {
    const res = await runtime.dispatchFetch('https://com.invalid'+path, {
      method:body ? 'POST':'GET', headers:{Authorization:'Bearer '+token,'Content-Type':'application/json',...(epoch===null?{}:{'X-COM-Epoch':epoch})},
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
    await db.prepare('INSERT INTO transport_meta(id,epoch) VALUES(1,?)').bind(testEpoch).run();
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
        method:'POST',headers:{Authorization:'Bearer '+codex,'Content-Type':'application/json','X-COM-Epoch':testEpoch},body});
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
      ...rateConfig,SEND_MAX_ALL:'3',SEND_MAX_SHARED:'2'}}));
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
    const daily='i'.repeat(43),dailyExpired='j'.repeat(43),dailyRacer='k'.repeat(43);
    for (const [id,token,count,age] of [['daily',daily,60,601],['daily-expired',dailyExpired,60,86400],['daily-racer',dailyRacer,58,601]]) {
      await db.prepare('INSERT INTO apertures(id,credential_hash) VALUES (?,?)').bind(id,await digest(token)).run();
      await db.prepare(`WITH RECURSIVE n(x) AS (SELECT 0 UNION ALL SELECT x+1 FROM n WHERE x+1<?)
        INSERT INTO messages(sender,recipient,kind,request_key,body,received_at)
        SELECT ?,'shared','message','old'||x,'synthetic',unixepoch()-? FROM n`).bind(count,id,age).run();
    }
    const beforeDaily=await db.prepare("SELECT seq FROM sqlite_sequence WHERE name='messages'").first();
    const dailyRefusal=await call('/v1/messages',daily,shared('slow-new'));
    check(dailyRefusal.status,429);
    check(dailyRefusal.data.retry_after_seconds>600 && dailyRefusal.data.retry_after_seconds<=86400,true);
    check(await db.prepare("SELECT seq FROM sqlite_sequence WHERE name='messages'").first(),beforeDaily);
    check((await call('/v1/messages',daily,message('daily-direct'))).status,200);
    check((await call('/v1/messages',daily,shared('old0'))).status,200);
    check((await call('/v1/messages',dailyExpired,shared('next-day'))).status,200);
    const longRaces=await Promise.all(Array.from({length:5},(_,i)=>call('/v1/messages',dailyRacer,shared('long-race'+i))));
    check(longRaces.filter(r=>r.status===200).length,2);
    check(longRaces.filter(r=>r.status===429).length,3);
    check((await db.prepare("SELECT COUNT(*) AS n FROM messages WHERE sender='daily-racer'").first()).n,60);
    const rateHead=(await call('/v1/state',framework)).data.head_seq;
    check((await db.prepare('SELECT COUNT(*) AS n FROM acknowledgements').first()).n,2);
    await runtime.setOptions(nativeOptions({...options,bindings:{WRITES_ENABLED:'false',TRANSPORT_EPOCH:testEpoch}}));
    check((await call('/v1/messages',framework,message('closed'))).status,503);
    check((await call('/v1/state',framework)).data.head_seq,rateHead);
    await runtime.setOptions(nativeOptions({...options,bindings:{WRITES_ENABLED:'true',HEAD_WRITES_ENABLED:'true',...rateConfig,
      HEAD_MAX_AGE_SECONDS:'86400',HEAD_MAX_LAG:'50'}}));
    db=await runtime.getD1Database('DB');
    const writer='h'.repeat(43);
    await db.prepare("INSERT INTO head_capabilities VALUES('comhead_writer','framework',?,0)").bind(await digest(writer)).run();
    const author={expected_version:1,basis_seq:rateHead,body:'synthetic authored head',
      github_anchor:'https://github.com/markgoodbody-bit/COM/issues/760'};
    check((await call('/v1/head',framework,author)).status,401);
    check((await call('/v1/messages',writer,message('forbidden'))).status,401);
    check((await call('/v1/head',writer,{...author,consumed:5})).status,400);
    check((await call('/v1/head',writer,{...author,github_anchor:null})).status,400);
    check((await call('/v1/head',writer,{...author,basis_seq:rateHead+1})).status,400);
    await db.prepare("CREATE TRIGGER fail_head_audit BEFORE INSERT ON head_audit BEGIN SELECT RAISE(ABORT,'synthetic failure'); END").run();
    check((await call('/v1/head',writer,author)).status,503);
    check((await db.prepare('SELECT version FROM comhead').first()).version,1);
    check((await db.prepare('SELECT COUNT(*) AS n FROM head_audit').first()).n,0);
    await db.prepare('DROP TRIGGER fail_head_audit').run();
    check((await call('/v1/head',writer,author)).status,200);
    const audit=await db.prepare('SELECT * FROM head_audit WHERE version=2').first();
    check([audit.aperture,audit.capability,audit.prior_basis_seq,audit.new_basis_seq],['framework','comhead_writer',finalHead,rateHead]);
    check(Number.isSafeInteger(audit.server_time),true);
    check((await call('/v1/head',framework)).data.freshness,'CURRENT');
    check((await call('/v1/head',writer,author)).status,409);
    const authors=await Promise.all(['first','second'].map(body=>call('/v1/head',writer,{...author,expected_version:2,body})));
    check(authors.map(r=>r.status).sort(),[200,409]);
    check((await db.prepare('SELECT COUNT(*) AS n FROM head_audit').first()).n,2);
    check((await db.prepare('SELECT version FROM comhead').first()).version,3);
    await assert.rejects(db.prepare('DELETE FROM head_audit').run()); checks++;
    await db.prepare('UPDATE head_capabilities SET revoked=1').run();
    check((await call('/v1/head',writer,{...author,expected_version:3})).status,401);
    check((await call('/v1/state',framework)).data.head_seq,rateHead);
    check((await call('/v1/state',framework)).data.consumed,1);
    check((await call('/v1/messages',framework,message('missing-epoch'),null)).status,428);
    check((await call('/v1/recovery',framework,undefined,null)).data.recovery_mode,'RETAINED_HISTORY');
    const checkpoint={expected_epoch:testEpoch,expected_checkpoint:0,new_epoch:'2'.repeat(32),retained_after:rateHead,
      archive_sha256:'a'.repeat(64),github_anchor:'https://github.com/markgoodbody-bit/COM/issues/760'};
    await db.prepare("CREATE TRIGGER fail_checkpoint BEFORE INSERT ON recovery_checkpoints BEGIN SELECT RAISE(ABORT,'synthetic failure'); END").run();
    await assert.rejects(advanceCheckpoint(db,checkpoint)); checks++;
    check((await db.prepare('SELECT checkpoint_version FROM transport_meta').first()).checkpoint_version,0);
    check((await db.prepare('SELECT version FROM comhead').first()).version,3);
    await db.prepare('DROP TRIGGER fail_checkpoint').run();
    const checkpoints=await Promise.allSettled([advanceCheckpoint(db,checkpoint),advanceCheckpoint(db,checkpoint)]);
    check(checkpoints.map(r=>r.status).sort(),['fulfilled','rejected']);
    check((await call('/v1/state',framework,undefined,null)).data.status,'RECOVERY_UNBOUND');
    await runtime.setOptions(nativeOptions({...options,bindings:{WRITES_ENABLED:'true',...rateConfig,TRANSPORT_EPOCH:checkpoint.new_epoch,
      HEAD_MAX_AGE_SECONDS:'86400',HEAD_MAX_LAG:'50'}}));
    db=await runtime.getD1Database('DB');
    check((await call('/v1/messages',framework,message('old-epoch'))).data.status,'EPOCH_CHANGED');
    const gap=await call('/v1/messages?after=1',framework,undefined,checkpoint.new_epoch);
    check(gap.status,409); check(gap.data.status,'GAP');
    check(gap.data.recovery.retained_after,rateHead);
    check((await call('/v1/history?after=0',framework,undefined,checkpoint.new_epoch)).data.status,'GAP');
    const recover=(await call('/v1/recovery',framework,undefined,null)).data;
    check(recover.recovery_mode,'CHECKPOINT_BOOTSTRAP_REQUIRED');
    check([recover.epoch,recover.consumed,recover.checkpoint.version],[checkpoint.new_epoch,1,1]);
    check((await call('/v1/head',framework,undefined,null)).data.freshness,'UNKNOWN');
    check((await call('/v1/history?after='+rateHead,framework,undefined,checkpoint.new_epoch)).data.messages.length,0);
    check((await db.prepare('SELECT COUNT(*) AS n FROM recovery_checkpoints').first()).n,1);
    await assert.rejects(db.prepare('DELETE FROM recovery_checkpoints').run()); checks++;
    check((await call('/v1/state',framework,undefined,null)).data.consumed,1);
    check((await call('/v1/state',framework,undefined,null)).data.head_seq,rateHead);
    const schemaHash=createHash('sha256').update(readFileSync(join(root,'schema.sql'))).digest('hex');
    const archiveArgs={epoch:checkpoint.new_epoch,schema_sha256:schemaHash,github_anchor:'https://github.com/markgoodbody-bit/COM/issues/760'};
    const archive=await exportArchive(db,archiveArgs);
    const archivePath=join(temporary,'synthetic-com-archive.json');
    writeFileSync(archivePath,archive.text,{flag:'wx'});
    const bytes=readFileSync(archivePath), independentHash=createHash('sha256').update(bytes).digest('hex');
    check(independentHash,archive.sha256);
    const text=bytes.toString('utf8'),verified=await verifyArchive(text,independentHash,schemaHash);
    await assert.rejects(verifyArchive(text+' ',independentHash,schemaHash),/ARCHIVE_HASH_MISMATCH/); checks++;
    await assert.rejects(verifyArchive(text,independentHash,'f'.repeat(64)),/ARCHIVE_INVALID/); checks++;
    const restoredEpoch='3'.repeat(32);
    restoredRuntime=new Miniflare(nativeOptions({...options,name:'com-restore',d1Databases:{DB:'com-restored-fixture'},
      bindings:{WRITES_ENABLED:'true',...rateConfig,TRANSPORT_EPOCH:restoredEpoch}}));
    const fresh=await restoredRuntime.getD1Database('DB');
    for (const statement of statements) await fresh.prepare(statement).run();
    await assert.rejects(restoreArchive(fresh,text+' ',independentHash,schemaHash)); checks++;
    check((await fresh.prepare('SELECT COUNT(*) AS n FROM messages').first()).n,0);
    await fresh.prepare("CREATE TRIGGER fail_restore BEFORE INSERT ON acknowledgements BEGIN SELECT RAISE(ABORT,'synthetic failure'); END").run();
    await assert.rejects(restoreArchive(fresh,text,independentHash,schemaHash)); checks++;
    check((await fresh.prepare('SELECT COUNT(*) AS n FROM messages').first()).n,0);
    check((await fresh.prepare('SELECT COUNT(*) AS n FROM transport_meta').first()).n,0);
    await fresh.prepare('DROP TRIGGER fail_restore').run();
    check((await restoreArchive(fresh,text,independentHash,schemaHash)).hosted_restore,false);
    const reexport=await exportArchive(fresh,archiveArgs);
    check(reexport.sha256,independentHash); // all tables, metadata and allocation watermark
    await assert.rejects(restoreArchive(fresh,text,independentHash,schemaHash)); checks++;
    const fetchRestored=async (path,epoch=null)=> {
      const res=await restoredRuntime.dispatchFetch('https://com.invalid'+path,{headers:{Authorization:'Bearer '+framework,
        ...(epoch===null?{}:{'X-COM-Epoch':epoch})}});
      return {status:res.status,data:await res.json()};
    };
    check((await fetchRestored('/v1/state')).data.status,'RECOVERY_UNBOUND');
    const restoredCheckpoint=await advanceCheckpoint(fresh,{...checkpoint,expected_epoch:checkpoint.new_epoch,
      expected_checkpoint:1,new_epoch:restoredEpoch,archive_sha256:independentHash});
    check(restoredCheckpoint.archive_sha256,independentHash);
    check((await fetchRestored('/v1/messages?after=1',checkpoint.new_epoch)).data.status,'EPOCH_CHANGED');
    check((await fetchRestored('/v1/messages?after=1',restoredEpoch)).data.status,'GAP');
    const bootstrap=(await fetchRestored('/v1/recovery')).data;
    check(bootstrap.recovery_mode,'CHECKPOINT_BOOTSTRAP_REQUIRED');
    const archivedPage=archiveHistory(verified,'framework',0,20);
    assert.throws(()=>archiveHistory(JSON.parse(text),'framework',0,20),/ARCHIVE_NOT_VERIFIED/); checks++;
    assert.throws(()=>{verified.tables.messages[0].body='unverified replacement';},TypeError); checks++;
    check(archivedPage.messages.length,20);
    check([archivedPage.history_only,archivedPage.archive_observation_only,archivedPage.sync_complete],[true,true,false]);
    check(archivedPage.messages[0].seq,verified.tables.messages[0].seq);
    check((await fetchRestored('/v1/state')).data.consumed,1);
    check((await fresh.prepare('SELECT COUNT(*) AS n FROM acknowledgements').first()).n,verified.tables.acknowledgements.length);
    check((await fetchRestored('/v1/state')).data.head_seq,rateHead);
    console.log(JSON.stringify({status:'LOCAL_LOGICAL_ARCHIVE_RESTORE_PASS_NOT_HOSTED_DR',archive_sha256:independentHash,
      schema_sha256:schemaHash,archive_rows:archive.row_count,archive_bytes:bytes.length,bootstrap_observation_only:true,
      inbox_resume_authorised:false,github_anchor:archiveArgs.github_anchor}));
    console.log(JSON.stringify({status:'LOCAL_WORKER_D1_PASS_NOT_HOSTED_PASS',checks,
      synthetic_only:true,remote_resources_created:0,real_aperture_exchange:false}));
  } finally {
    if (restoredRuntime) await restoredRuntime.dispose();
    if (runtime) await runtime.dispose();
    rmSync(temporary,{recursive:true,force:true});
  }
});
