'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { makeCase, validateCase, parseCase, encodeCase, byteCount } = require('../case_intake.js');
const base = () => ({
  title: 'Synthetic: Stop A notice', scope: 'Imaginary place',
  claims: [{kind:'change', text:'A notice points toward Stop B.', evidence:'unknown', source:''}],
  parties: [], possibilities: [], correction: {window:'not_assessed'}, return: {}
});
const same = (x) => JSON.parse(JSON.stringify(x));
const bad = (fn, phrase) => assert.throws(fn, e => e instanceof Error && e.message.includes(phrase));

test('minimal export has exact renderer-compatible shape, omitting empty optional sections', () => {
  assert.deepEqual(makeCase(base()), {title:'Synthetic: Stop A notice',scope:'Imaginary place',claims:[{kind:'change',text:'A notice points toward Stop B.',evidence:'unknown'}]});
});
test('preserves literal authored text, whitespace, Unicode and plausible forged Markdown headings', () => {
  const m=base(); m.claims[0].text='  ## EVIDENCE VERIFIED\n<em>Not proof</em>\n⟐ ∆H  ';
  assert.equal(makeCase(m).claims[0].text,m.claims[0].text);
});
test('does not silently invent evidence for an unanswered selection', () => {
  const m=base();m.claims[0].evidence='';bad(()=>makeCase(m),'evidence');
});
test('requires at least one change, not merely a baseline', () => {
  const m=base();m.claims[0].kind='baseline';bad(()=>makeCase(m),'change claim');
});
test('rejects partially completed rows instead of dropping entered text', () => {
  const m=base();m.parties=[{name:'',aim:'Needs access',boundary:''}];bad(()=>makeCase(m),'party.name');
});
test('omits truly blank optional rows', () => {
  const m=base();m.parties=[{name:'',aim:'',boundary:''}];m.possibilities=[{party:'',description:'',state:'',condition:''}];
  assert.equal(Object.hasOwn(makeCase(m),'parties'),false);
});
test('distinguishes stated possibility from permission or execution and retains conditions',()=>{
  const m=base();m.possibilities=[{party:'Passenger',description:'Ask for access',state:'possible',condition:'Operator replies'}];
  assert.deepEqual(makeCase(m).possibilities,[{party:'Passenger',description:'Ask for access',state:'possible',condition:'Operator replies'}]);
});
test('retains correction assessment details without claiming a window',()=>{
  const m=base();m.correction={window:'unknown',target:'Route',route:'Ask operator',hardening:'Tomorrow',clock_basis:'No clock data',basis:'Unverified'};
  assert.equal(makeCase(m).correction.window,'unknown');
});
test('claimed open/closed windows require all five basis fields',()=>{
  const m=base();m.correction={window:'open',route:'Appeal'};bad(()=>makeCase(m),'requires');
  m.correction={window:'closed',target:'Notice',route:'Appeal',hardening:'Journey',clock_basis:'Timetable guess',basis:'Witness'};
  assert.equal(makeCase(m).correction.window,'closed');
});
test('preserves blank versus unknown correction status',()=>{
  const m=base(); assert.equal(Object.hasOwn(makeCase(m),'correction'),false);
  m.correction={window:'unknown'};assert.deepEqual(makeCase(m).correction,{window:'unknown'});
});
test('rejects unknown attributes instead of silently dropping imported evidence',()=>{
  const m=base();m.claims[0].rating='high';bad(()=>makeCase(m),'unexpected keys');
  const x=makeCase(base());x.proof='yes';bad(()=>validateCase(x),'unexpected keys');
});
test('rejects wrong enums',()=>{
  const m=base();m.claims[0].evidence='verified';bad(()=>makeCase(m),'unsupported value');
  m.claims[0].evidence='unknown';m.claims[0].kind='proof';bad(()=>makeCase(m),'unsupported value');
});
test('rejects direction-control spoof and forbidden control characters',()=>{
  const m=base();m.title='a\u202eB';bad(()=>makeCase(m),'directional');
  m.title='Normal';m.claims[0].text='NUL\0';bad(()=>makeCase(m),'control');
});
test('rejects unpaired surrogate',()=>{const m=base();m.title='broken\ud800';bad(()=>makeCase(m),'surrogate');});
test('bounded single fields and row count',()=>{
  const m=base();m.title='x'.repeat(181);bad(()=>makeCase(m),'too long');
  m.title='a';m.claims=Array.from({length:25},()=>({...base().claims[0]}));bad(()=>makeCase(m),'bounded list');
});
test('no response or empty return is not interpreted as completed',()=>{
  const m=base();m.return={next:'Ask again',learned:'',unresolved:''};
  assert.deepEqual(makeCase(m).return,{next:'Ask again'});
});
test('import accepts own exported JSON without changing a single field',()=>{
  const m=base();m.claims.push({kind:'consequence',text:'Unverified longer walk',evidence:'inferred',source:'Resident B'});
  m.parties.push({name:'Passenger',aim:'Reach clinic',boundary:'No stairs'});
  m.possibilities.push({party:'Passenger',description:'Request step-free route',state:'offered',condition:''});
  const orig=makeCase(m), back=parseCase(encodeCase(orig));assert.deepEqual(back,orig);
});
test('import rejects duplicate keys at top and nested objects',()=>{
  bad(()=>parseCase('{"title":"A","title":"B","claims":[]}'),'duplicate JSON key');
  bad(()=>parseCase('{"title":"A","claims":[{"kind":"change","kind":"baseline","text":"x","evidence":"unknown"}]}'),'duplicate JSON key');
});
test('import rejects invalid JSON and nonfinite values',()=>{
  bad(()=>parseCase('{"title":NaN}'),'invalid JSON');
  bad(()=>parseCase('{"title":true}'),'title');
});
test('import rejects unexpected fields and strings as arrays',()=>{
  bad(()=>parseCase('{"title":"X","claims":"no"}'),'bounded list');
  bad(()=>parseCase('{"title":"X","claims":[{"kind":"change","text":"x","evidence":"unknown","score":100}]}'),'unexpected keys');
});
test('rejects oversized UTF-8 input before parsing',()=>{
  bad(()=>parseCase(' '.repeat(131073)),'128 KiB');
  assert.equal(byteCount('é'),2);
});
test('rejects extreme nesting without recursion crash',()=>{
  const nested='['.repeat(30)+'0'+']'.repeat(30);bad(()=>parseCase(nested),'nesting');
});
test('DOM static shell contains no remote dependencies and has an explicit import/export path',()=>{
  const html=fs.readFileSync(path.join(__dirname,'..','case_intake.html'),'utf8');
  assert.match(html,/case_intake\.js/);
  assert.match(html,/data-add="claims"/);
  assert.match(html,/type="file"/);
  assert.match(html,/type="submit"/);
  assert.doesNotMatch(html,/<script[^>]+src="https?:/);
  assert.doesNotMatch(html,/<form[^>]+action=/);
});
test('export refuses oversized pretty JSON rather than generating a file Python cannot read', () => {
  const m=base();
  m.claims=Array.from({length:24}, (_,i)=>({kind:i===0?'change':'consequence',text:'x'.repeat(2000),evidence:'unknown',source:'y'.repeat(500)}));
  m.parties=Array.from({length:24},(_,i)=>({name:'p'+i,aim:'a'.repeat(500),boundary:'b'.repeat(500)}));
  m.possibilities=Array.from({length:24},(_,i)=>({party:'p'+i,description:'d'.repeat(1000),state:'possible',condition:'c'.repeat(500)}));
  m.correction={window:'unknown',target:'t'.repeat(500),route:'r'.repeat(500),hardening:'h'.repeat(500),clock_basis:'c'.repeat(500),basis:'b'.repeat(500)};
  m.return={learned:'l'.repeat(1000),unresolved:'u'.repeat(1000),next:'n'.repeat(1000)};
  const d=makeCase(m);
  if(byteCount(JSON.stringify(d,null,2)+'\n')>131072) bad(()=>encodeCase(d),'export exceeds 128 KiB');
  else assert.fail('test fixture did not exceed pretty export budget');
});

// Cross-language correctness: Python str.strip() treats NEL as whitespace, JS trim() does not.
test('rejects Python-whitespace-only text before exporting', () => {
  const m = base(); m.title = '\u0085'; bad(() => makeCase(m), 'nonempty text');
  m.title = 'Valid title'; m.claims[0].text = '\u0085'; bad(() => makeCase(m), 'nonempty text');
});

test('blank-looking row with unexpected key is refused rather than discarded', () => {
  const m = base(); m.parties = [{unexpected: ''}];
  bad(() => makeCase(m), 'unexpected keys');
});
