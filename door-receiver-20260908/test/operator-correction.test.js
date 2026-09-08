import test from 'node:test';
import assert from 'node:assert/strict';
import {runOperator} from '../src/operator-cli.js';
const TOKEN='x'.repeat(32);
const response=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:{'content-type':'application/json'}});

test('corrections queue is a no-stdin operator action',async()=>{
  let sent,stdin=false;
  const result=await runOperator({argv:['corrections'],env:{PSFH_ADMIN_TOKEN:TOKEN},readStdin:async()=>{stdin=true;return '';},fetchImpl:async(_u,i)=>{sent=JSON.parse(i.body);return response({corrections:[]});}});
  assert.equal(stdin,false);assert.deepEqual(sent,{action:'corrections'});assert.deepEqual(result,{corrections:[]});
});

test('resolve-correction is explicit and does not accept arbitrary outcome',async()=>{
  let sent;
  await runOperator({argv:['resolve-correction'],env:{PSFH_ADMIN_TOKEN:TOKEN},readStdin:async()=>JSON.stringify({id:'r1',outcome:'content_removed',reason:'Synthetic review result'}),fetchImpl:async(_u,i)=>{sent=JSON.parse(i.body);return response({id:'r1',state:'resolved'});}});
  assert.deepEqual(sent,{action:'resolve-correction',id:'r1',outcome:'content_removed',reason:'Synthetic review result'});
  await assert.rejects(()=>runOperator({argv:['resolve-correction'],env:{PSFH_ADMIN_TOKEN:TOKEN},readStdin:async()=>JSON.stringify({id:'r1',outcome:'delete_everything',reason:'bad'})}),/VALID_CORRECTION_OUTCOME_REQUIRED/);
});
