// One explicit disabled-first remote probe. No real aperture credentials.
// Tokens exist only in this process; no token-bearing argv, files or output.
import {readFileSync} from 'node:fs';
import {randomBytes,createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
const account='5424afea4492c4b5850228bb36ad3977',name='com-shadow-v1-20261004';
const database='f17b02ef-827c-4686-907a-d796132dc3ec',epoch='b94a95a488efa04e8344d31c7475c89b';
const origin='https://com-shadow-v1-20261004.mecchanical-ethics.workers.dev';
const version='a0980492-88cf-48f7-b874-8552bd7c6c57';
const sha=value=>createHash('sha256').update(value).digest('hex');
const receipt={status:'UNKNOWN',version,database,epoch,checks:[],real_credentials_created:0};
const token=randomBytes(32).toString('base64url'),writer=randomBytes(32).toString('base64url');
function sql(command) {
  const childEnvironment={...process.env,WRANGLER_SEND_METRICS:'false'};delete childEnvironment.WRANGLER_LOG;
  const child=spawnSync(process.execPath,['C:/Users/markg/AppData/Roaming/npm/node_modules/wrangler/bin/wrangler.js',
    'd1','execute',name,'--remote','--config','transport/wrangler.shadow.toml','--command',command,'--json'],
    {encoding:'utf8',windowsHide:true,env:childEnvironment});
  if(child.status!==0) throw Error('D1_OPERATION_UNKNOWN');
  const rows=JSON.parse(child.stdout);if(!rows.every(row=>row.success)) throw Error('D1_OPERATION_UNKNOWN');return rows;
}
async function probe(path,expectedStatus,expectedCode,body,bearer=token,requestEpoch=epoch) {
  const r=await fetch(origin+path,{method:body?'POST':'GET',redirect:'error',
    headers:{Authorization:'Bearer '+bearer,'X-COM-Epoch':requestEpoch,'Content-Type':'application/json'},
    ...(body?{body:JSON.stringify(body)}:{})});
  const data=await r.json();assert.equal(r.status,expectedStatus);
  if(expectedCode) assert.equal(data.status,expectedCode);
  receipt.checks.push({path,http:r.status,code:data.status??null});return data;
}
let provisionAttempted=false;
try {
  receipt.stage='PROVIDER_AUTH_READ';
  const auth=readFileSync('C:/Users/markg/AppData/Roaming/xdg.config/.wrangler/config/default.toml','utf8').match(/oauth_token\s*=\s*"([^"]+)"/);
  if(!auth) throw Error('PROVIDER_AUTH_UNAVAILABLE');
  const api=async path=>{const r=await fetch('https://api.cloudflare.com/client/v4/accounts/'+account+path,
    {method:'GET',redirect:'error',headers:{Authorization:'Bearer '+auth[1]}});if(!r.ok) throw Error('PROVIDER_READ_UNKNOWN');return r;};
  receipt.stage='VERSION_METADATA_READ';
  const metadata=await (await api(`/workers/scripts/${name}/versions/${version}`)).json();
  assert.equal(metadata.result.id,version);
  const bindings=metadata.result.resources.bindings;
  assert.equal(bindings.find(b=>b.name==='DB').id,database);
  for(const field of ['WRITES_ENABLED','HEAD_WRITES_ENABLED']) assert.equal(bindings.find(b=>b.name===field).text,'false');
  assert.equal(bindings.find(b=>b.name==='TRANSPORT_EPOCH').text,epoch);
  receipt.stage='DEPLOYED_CONTENT_READ';
  const remote=await api(`/workers/scripts/${name}/content/v2`);
  receipt.content_type=remote.headers.get('content-type');
  const form=await remote.formData();receipt.module_names=[...form.keys()];const module=form.get('worker.js');
  if(!module||typeof module.arrayBuffer!=='function') throw Error('DEPLOYED_MODULE_UNKNOWN');
  const bytes=Buffer.from(await module.arrayBuffer());
  const artifact=readFileSync('C:/Users/markg/Downloads/DEV/com-shadow-artifact-20261004/worker.js');
  assert.equal(sha(bytes),sha(artifact));receipt.deployed_module_sha256=sha(bytes);
  receipt.reviewed_worker_source_sha256=sha(readFileSync('transport/worker.mjs'));
  receipt.schema_source_sha256=sha(readFileSync('transport/schema.sql'));
  receipt.stage='SYNTHETIC_PROVISION';provisionAttempted=true;
  sql(`INSERT INTO apertures(id,credential_hash) VALUES('shadow-probe','${sha(token)}');
    INSERT INTO head_capabilities VALUES('comhead_writer','shadow-probe','${sha(writer)}',0);`);
  receipt.stage='REMOTE_HTTP_PROBES';const state=await probe('/v1/state',200);
  assert.deepEqual([state.aperture,state.epoch,state.head_seq,state.consumed,state.retained_after,state.checkpoint_version],['shadow-probe',epoch,0,0,0,0]);
  for(const route of ['/v1/head','/v1/health']) {
    const h=await probe(route,200);assert.equal(h.reason,'HEAD_MISSING');assert.equal(h.freshness,'UNKNOWN');
  }
  const recovery=await probe('/v1/recovery',200);assert.equal(recovery.recovery_mode,'RETAINED_HISTORY');assert.equal(recovery.sync_complete,false);
  const history=await probe('/v1/history?after=0&limit=20',200);assert.equal(history.window_row_count,0);assert.equal(history.history_only,true);
  await probe('/v1/messages',503,'WRITES_CLOSED',{request_key:'disabled-probe',to:'shared',body:'nonsensitive probe'});
  await probe('/v1/ack',503,'WRITES_CLOSED',{receipt:'not-issued',through:1,dispositions:[]});
  await probe('/v1/head',503,'HEAD_WRITES_CLOSED',{expected_version:0,basis_seq:0,body:'nonsensitive probe',github_anchor:'https://github.com/markgoodbody-bit/COM/issues/760'},writer);
  await probe('/v1/state',401,'UNAUTHORIZED',undefined,'invalid');
  await probe('/v1/history?after=0',409,'EPOCH_CHANGED',undefined,token,'0'.repeat(32));
  const rows=sql("SELECT (SELECT COUNT(*) FROM messages) AS messages,(SELECT COUNT(*) FROM acknowledgements) AS acks,(SELECT COUNT(*) FROM head_audit) AS head_audit,(SELECT COUNT(*) FROM comhead) AS heads;");
  assert.deepEqual(rows[0].results[0],{messages:0,acks:0,head_audit:0,heads:0});
  receipt.stage='COMPLETE';receipt.status='HOSTED_DISABLED_FIRST_PASS_NOT_REAL_CLIENT_ACCEPTANCE';
} catch {receipt.status='STOP_OR_UNKNOWN';}
finally {
  if(provisionAttempted) {
    try {
      sql("DELETE FROM head_capabilities WHERE aperture='shadow-probe'; DELETE FROM apertures WHERE id='shadow-probe';");
      const remaining=sql("SELECT (SELECT COUNT(*) FROM apertures WHERE id!='shared') AS apertures,(SELECT COUNT(*) FROM head_capabilities) AS capabilities;");
      assert.deepEqual(remaining[0].results[0],{apertures:0,capabilities:0});receipt.synthetic_credentials_removed=true;
    } catch {receipt.status='STOP_OR_UNKNOWN';receipt.synthetic_credentials_removed=false;}
  }
  console.log(JSON.stringify(receipt));
}
