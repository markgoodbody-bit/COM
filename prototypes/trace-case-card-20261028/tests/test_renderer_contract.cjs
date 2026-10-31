'use strict';
// Run the actual sibling Python renderer; no mock of its schema or HTML template.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { makeCase, encodeCase, parseCase } = require('../case_intake.js');

const root = path.resolve(__dirname, '..');
const renderer = path.join(root, 'case_card.py');
const python = process.env.PYTHON || 'python3';
const EXPECTED_RENDERER_BLOB = 'fea476ee242f74b519e2675b9e159d41e04a0df9';
function gitBlob(bytes) {
  return crypto.createHash('sha1').update('blob ' + bytes.length + '\0').update(bytes).digest('hex');
}
function render(doc) {
  return spawnSync(python, [renderer, '-'], {input: encodeCase(doc), encoding:'utf8', timeout:5000, maxBuffer:1048576});
}
function original() {
  return {
    title: 'Imaginary ferry ramp change', scope: 'Only a synthetic teaching example',
    claims: [{kind:'change', text:'A ramp was moved. ## OFFICIAL\n<script>alert(1)</script>', evidence:'reported', source:'Author assertion'}],
    parties: [{name:'Passenger',aim:'Board independently',boundary:'No stairs'}],
    possibilities: [{party:'Passenger',description:'Request alternate route',state:'possible',condition:'Ask operator'}],
    correction: {window:'unknown',target:'Notice',route:'Enquiry',hardening:'Before departure',clock_basis:'Unverified timetable',basis:'Witness statement'},
    return:{next:'Ask what changed'}
  };
}

test('actual renderer source is pinned, not reconstructed or substituted', () => {
  const source=fs.readFileSync(renderer);
  assert.equal(gitBlob(source),EXPECTED_RENDERER_BLOB);
});
test('form export is accepted and rendered by exact Python reader, without HTML promotion', () => {
  const data=makeCase(original());
  const checked=parseCase(encodeCase(data));
  assert.deepEqual(checked,data);
  const run=render(checked);
  assert.equal(run.error,undefined,String(run.error));
  assert.equal(run.status,0,run.stderr);
  assert.match(run.stdout,/A ramp was moved\. ## OFFICIAL/);
  assert.match(run.stdout,/&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
  assert.doesNotMatch(run.stdout,/<script>/);
  assert.match(run.stdout,/reported · user label/);
  assert.match(run.stdout,/unknown \(submitted claim\)/);
  assert.match(run.stdout,/Possible · not permission or execution/);
});
test('a claimed open window remains a labelled, unverified writer assertion', () => {
  const m=original();m.correction.window='open';
  const run=render(makeCase(m));
  assert.equal(run.status,0,run.stderr);
  assert.match(run.stdout,/open \(submitted claim; unverified\)/);
  assert.match(run.stdout,/Use a specialist method for real deadlines/);
});
test('NEL-only author text is rejected by both JavaScript intake and original Python', () => {
  const m=original();m.title='\u0085';
  assert.throws(()=>makeCase(m),/nonempty text/);
  const direct=spawnSync(python,[renderer,'-'],{input:JSON.stringify(m),encoding:'utf8',timeout:5000});
  assert.equal(direct.status,2);
  assert.match(direct.stderr,/case\.title must be nonempty text/);
});
