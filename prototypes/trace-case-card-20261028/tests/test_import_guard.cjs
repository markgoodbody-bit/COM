'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '..', 'case_intake.js'), 'utf8');
const html = fs.readFileSync(path.join(__dirname, '..', 'case_intake.html'), 'utf8');
const record = {title:'Imported synthetic case', claims:[{kind:'change',text:'An authored claim',evidence:'unknown'}]};
const encoded = JSON.stringify(record);

class Element {
  constructor() {
    this.children = []; this.handlers = {}; this.fields = [];
    this.dataset = {}; this.hidden = true; this.value = ''; this.textContent = '';
  }
  addEventListener(name, callback) { this.handlers[name] = callback; }
  focus() { this.focused = true; }
  querySelectorAll(selector) { return selector === '[data-field]' ? this.fields : []; }
  querySelector(selector) {
    return selector === '[data-remove]' ? this.removeButton :
      selector === '[data-field]' ? this.fields[0] : null;
  }
  setAttribute(name, value) { this[name] = value; }
  cloneNode() {
    const row = new Element();
    row.fields = this.fields.map(f => {
      const x = new Element(); x.dataset = {...f.dataset}; x.value = f.value; return x;
    });
    row.removeButton = new Element();
    return row;
  }
  appendChild(child) { this.children.push(child); }
  replaceChildren(...children) { this.children = children; }
  remove() { this.removed = true; }
}

function loadUI() {
  const ids = ('rows-claims rows-parties rows-possibilities template-claims ' +
    'template-parties template-possibilities case-title case-scope correction-fields ' +
    'return-fields status draft-review intake-form review-draft import-json ' +
    'pending-import pending-import-summary confirm-import cancel-import').split(' ');
  const elements = Object.fromEntries(ids.map(id => [id, new Element()]));
  for (const [kind, fields] of Object.entries({
    claims:['kind','text','evidence','source'],
    parties:['name','aim','boundary'],
    possibilities:['party','description','state','condition']
  })) {
    const row = new Element();
    row.fields = fields.map(field => {
      const input = new Element(); input.dataset = {field}; return input;
    });
    elements['template-' + kind].content = {firstElementChild:row};
  }
  const listeners = {};
  const document = {
    getElementById(id) { return elements[id]; },
    querySelectorAll() { return []; },
    querySelector() { return null; },
    addEventListener(name, callback) { listeners[name] = callback; },
    createElement() { return new Element(); },
    body: new Element()
  };
  vm.runInNewContext(source, {document, window:{}, TextEncoder, Blob, URL, setTimeout,
    module:{exports:{}}}, {timeout:1000});
  listeners.DOMContentLoaded();
  return elements;
}
async function select(elements, text=encoded) {
  const input = elements['import-json'];
  const target = {files:[{size:Buffer.byteLength(text), text:async()=>text}],value:'selection'};
  await input.handlers.change({target});
  assert.equal(target.value, '');
}

test('HTML offers an explicit local replacement choice', () => {
  for (const id of ['pending-import','pending-import-summary','confirm-import','cancel-import']) {
    assert.match(html, new RegExp('id="' + id + '"'));
  }
  assert.match(html, /Nothing is replaced until you choose Replace/);
});
test('file selection stages without overwriting existing text, then cancel preserves it', async () => {
  const e = loadUI(); e['case-title'].value = 'Unsaved author work';
  await select(e);
  assert.equal(e['case-title'].value, 'Unsaved author work');
  assert.equal(e['pending-import'].hidden, false);
  assert.match(e['pending-import-summary'].textContent, /Imported synthetic case/);
  e['cancel-import'].handlers.click();
  assert.equal(e['case-title'].value, 'Unsaved author work');
  assert.equal(e['pending-import'].hidden, true);
});
test('explicit confirmation alone applies validated imported content', async () => {
  const e = loadUI(); e['case-title'].value = 'Unsaved author work';
  await select(e);
  e['confirm-import'].handlers.click();
  assert.equal(e['case-title'].value, 'Imported synthetic case');
  assert.equal(e['pending-import'].hidden, true);
});
test('in-flight file read cannot replace or re-stage after a draft edit', async () => {
  const e = loadUI(); e['case-title'].value = 'Newer author work';
  let resolve;
  const fileRead = new Promise(r => { resolve = r; });
  const pending = e['import-json'].handlers.change({
    target:{files:[{size:Buffer.byteLength(encoded), text:()=>fileRead}],value:'pending'}
  });
  e['intake-form'].handlers.input();
  resolve(encoded); await pending;
  assert.equal(e['case-title'].value, 'Newer author work');
  assert.equal(e['pending-import'].hidden, true);
});
test('duplicate keys refuse without replacing the current form', async () => {
  const e = loadUI(); e['case-title'].value = 'Keep this work';
  await select(e, '{"title":"x","title":"y","claims":[]}');
  assert.equal(e['case-title'].value, 'Keep this work');
  assert.equal(e['pending-import'].hidden, true);
  assert.match(e['status'].textContent, /Import refused/);
});
test('hostile-looking title remains literal text in confirmation summary', async () => {
  const e = loadUI();
  await select(e, JSON.stringify({...record,title:'<script>fictional</script>\n# AUTHORITY'}));
  assert.match(e['pending-import-summary'].textContent, /<script>fictional<\/script>/);
  assert.equal(e['pending-import'].hidden, false);
});
