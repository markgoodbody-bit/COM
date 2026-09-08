import test from 'node:test';
import assert from 'node:assert/strict';
import {runOperator,OperatorError} from '../src/operator-cli.js';

const TOKEN='x'.repeat(32);
const response=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:{'content-type':'application/json'}});

test('queue uses auth header, no token in url or body', async()=>{
  let seen; const output=[];
  const result=await runOperator({
    argv:['queue'], env:{PSFH_ADMIN_TOKEN:TOKEN,PSFH_OPERATOR_URL:'https://discuss.example.test/'},
    fetchImpl:async(url,init)=>{seen={url:String(url),...init};return response({queue:[]});},
    write:s=>output.push(s)
  });
  assert.deepEqual(result,{queue:[]});
  assert.equal(seen.url,'https://discuss.example.test/api/admin');
  assert.equal(seen.headers.Authorization,`Bearer ${TOKEN}`);
  assert.equal(seen.body,'{"action":"queue"}');
  assert.equal(seen.url.includes(TOKEN),false);
  assert.equal(seen.body.includes(TOKEN),false);
  assert.equal(output.join('').includes(TOKEN),false);
});

test('publish reads decision from stdin rather than command arguments', async()=>{
  let body;
  await runOperator({
    argv:['publish'], env:{PSFH_ADMIN_TOKEN:TOKEN},
    readStdin:async()=>JSON.stringify({id:'c1',revision:2,reason:'relevant and safe to display'}),
    fetchImpl:async(_url,init)=>{body=JSON.parse(init.body);return response({id:'c1',state:'published',revision:2});}
  });
  assert.deepEqual(body,{action:'publish',id:'c1',revision:2,reason:'relevant and safe to display'});
});

test('respond keeps response body out of process arguments', async()=>{
  let body;
  await runOperator({
    argv:['respond'], env:{PSFH_ADMIN_TOKEN:TOKEN},
    readStdin:async()=>JSON.stringify({id:'c2',revision:1,body:'Project response'}),
    fetchImpl:async(_url,init)=>{body=JSON.parse(init.body);return response({id:'c2',responded:true});}
  });
  assert.deepEqual(body,{action:'respond',id:'c2',revision:1,body:'Project response'});
});

test('rejects credentials/query in operator url and insecure remote http', async()=>{
  for (const url of ['https://user:pass@example.test/','https://example.test/?token=x','http://example.test/']) {
    await assert.rejects(()=>runOperator({argv:['queue'],env:{PSFH_ADMIN_TOKEN:TOKEN,PSFH_OPERATOR_URL:url}}),OperatorError);
  }
});

test('does not print token when receiver returns an error', async()=>{
  const output=[];
  await assert.rejects(()=>runOperator({
    argv:['pause'], env:{PSFH_ADMIN_TOKEN:TOKEN},
    fetchImpl:async()=>response({error:'MODERATOR_AUTH_REQUIRED'},401), write:s=>output.push(s)
  }),/OPERATOR_REQUEST_FAILED_401_MODERATOR_AUTH_REQUIRED/);
  assert.equal(output.join('').includes(TOKEN),false);
});
