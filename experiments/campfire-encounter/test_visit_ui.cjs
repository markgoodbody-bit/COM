// State tests with a small DOM double; not browser rendering or usability proof.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
function harness() {
  const elements = new Map();
  const element = () => ({value:'', checked:false, disabled:false, textContent:'',
    children:[], append(...v){this.children.push(...v);}, replaceChildren(){this.children=[];},
    click(){}, focus(){}});
  const get = id => {if (!elements.has(id)) elements.set(id, element()); return elements.get(id);};
  const carry = {checked:true, value:'yes'};
  const calls = [];
  let responder = async () => ({acceptance:'SECRET'});
  const context = vm.createContext({document:{getElementById:get, createElement:element,
    createTextNode:text=>text, querySelector:s=>s.startsWith('meta') ? {content:'token'} : carry,
    querySelectorAll:()=>[carry]}, fetch:async (url, options)=>{
      calls.push({url, data:JSON.parse(options.body)});
      const body = await responder(url); return {ok:true, json:async()=>body};
    }, Blob, URL:{createObjectURL:()=> 'blob:test', revokeObjectURL(){}},
    setTimeout:fn=>fn(), crypto:{randomUUID:()=> 'request'}});
  vm.runInContext(fs.readFileSync(__dirname+'/app.js','utf8'), context);
  return {get, calls, respond:fn=>responder=fn};
}
test('leave clears page state and does not export acceptance', async()=>{
  const h=harness(); await h.get('join').onclick();
  h.respond(async()=>({entries:[], added_ids:[], comparison:'DIFFERENT_ROOM',
    receipt:{format:'campfire-return-v1',room:'room',last:null}}));
  await h.get('refresh').onclick();
  assert.match(h.get('overview').textContent, /does not repair a failed comparison/);
  h.get('capsule').value='old text'; h.get('inspection').textContent='old inspection';
  await h.get('leave').onclick();
  assert.equal(h.get('capsule').value,''); assert.equal(h.get('inspection').textContent,'');
  assert.equal(h.get('leave').disabled,true);
  assert.equal(h.calls.length,2); // leaving makes no network request
  assert.match(h.get('status').textContent, /not server permissions/);
});
test('inflight retrieval excludes leave and other overlapping operations', async()=>{
  const h=harness(); await h.get('join').onclick();
  let resolve; h.respond(()=>new Promise(r=>resolve=r));
  const reading=h.get('refresh').onclick();
  await h.get('leave').onclick(); await h.get('join').onclick();
  assert.equal(h.calls.length,2);
  assert.match(h.get('status').textContent, /wait/);
  resolve({entries:[],added_ids:[],comparison:'NO_PRIOR_MARKER',receipt:{room:'r',last:null}});
  await reading;
  await h.get('leave').onclick();
  assert.equal(h.get('entries').children.length,0);
  assert.equal(h.get('leave').disabled,true);
});
test('failed refresh invalidates the previous downloadable position', async()=>{
  const h=harness(); await h.get('join').onclick();
  h.respond(async()=>({entries:[],added_ids:[],comparison:'NO_PRIOR_MARKER',receipt:{room:'r',last:null}}));
  await h.get('refresh').onclick(); assert.equal(h.get('leave').disabled,false);
  h.respond(async()=>{throw Error('network failed');});
  await h.get('refresh').onclick(); assert.equal(h.get('leave').disabled,true);
});
