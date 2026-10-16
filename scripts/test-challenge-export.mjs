import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import vm from 'node:vm';

const root = new URL('../public/explore/', import.meta.url);
const read = file => readFileSync(new URL(file, root), 'utf8');
const page = read('challenge-local.html');
const door = read('challenge.html');
const textDoor = read('challenge.md');
const script = page.match(/<script>([\s\S]*?)<\/script>/)?.[1];
const style = page.match(/<style media="all">([\s\S]*?)<\/style>/)?.[1];

test('complete local page is self-contained; inline JavaScript hash matches restrictive CSP', () => {
  assert.ok(script && style);
  const hash = createHash('sha256').update(script).digest('base64');
  assert.ok(page.includes("script-src 'sha256-" + hash + "'"));
  assert.match(page,/connect-src 'none'; form-action 'none'/);
  assert.match(page,/default-src 'none'/);
  assert.doesNotMatch(page,/<script[^>]+src=/);
  assert.doesNotMatch(page,/<link[^>]+rel="stylesheet"/);
});
test('existing human and Markdown routes show the local draft without implying receipt', () => {
  assert.match(door,/href="challenge-local\.html"/);
  assert.match(textDoor,/\[local challenge draft and export\]\(challenge-local\.html\)/);
  for (const item of [door,textDoor,page]) {
    assert.match(item,/not (?:submission|submit|submitting)|not<\/strong> submitting/i);
  }
  assert.match(door,/needs a GitHub account/);
});
test('no submission API, browser persistence, tracking or implicit network request',()=>{
  assert.match(script,/event\.preventDefault\(\)/);
  for (const forbidden of [/\bfetch\s*\(/,/\bXMLHttpRequest\b/,/\bWebSocket\b/,/\bsendBeacon\b/,/\blocalStorage\b/,/\bsessionStorage\b/,/\bindexedDB\b/,/\bdocument\.cookie\b/,/\bserviceWorker\b/]) assert.doesNotMatch(script, forbidden);
  assert.doesNotMatch(page, /<form[^>]+action=/);
  assert.doesNotMatch(page, /<(?:iframe|img)[^>]*>/);
  assert.match(page, /No account needed/);
});
test('form fields have labels; no identity/contact field is required',()=>{
  for(const key of ['edition','claim','concern','evidence','unknown','change']){
    assert.ok(page.includes('for="'+key+'"') && page.includes('id="'+key+'"'),key);
  }
  assert.doesNotMatch(page,/<input[^>]+type="(?:email|password|hidden)"/);
  assert.match(page,/avoid names, secrets, contact details/);
});
test('formatter makes useful partial, reproducible UTF-8 plain text and marks uncertainty',()=>{
  const modified=script.replace("  if (typeof document === 'undefined') return;", "  globalThis.__testPacket = makePacket;\n  if (typeof document === 'undefined') return;");
  const context=vm.createContext({});
  vm.runInContext(modified,context,{timeout:1000});
  const input={claim:'  Door is open  ',concern:'Maybe wrong\r\nA ≠ B — café 雪'};
  const value=context.__testPacket(input);
  assert.equal(value,context.__testPacket(input));
  assert.match(value,/CLAIM OR PASSAGE\nDoor is open/);
  assert.match(value,/Maybe wrong\nA ≠ B — café 雪/);
  assert.match(value,/UNKNOWN[S]? OR UNCERTAINTIES\n\(not supplied\)/i);
  assert.match(value,/NOT SUBMITTED\. NOT RECEIVED/);
  assert.match(value,/Reader choice: keep this draft/);
});
test('no untrusted preview HTML execution; explicit copy and save only',()=>{
  assert.match(script,/printPacket\.textContent = packet\.value/);
  assert.doesNotMatch(script,/\.innerHTML\s*=/);
  assert.match(script,/form\.addEventListener\('input', invalidate\)/);
  assert.match(script,/copy\.disabled = true/);
  assert.match(script,/save\.disabled = true/);
  assert.match(script,/copy\.addEventListener\('click'/);
  assert.match(script,/save\.addEventListener\('click'/);
  assert.match(script,/new Blob\(\[packet\.value\]/);
  assert.match(script,/reader-challenge-local-draft\.txt/);
});
test('keyboard labels, copy status, mobile and print affordances exist',()=>{
  assert.match(page,/aria-live="polite"/);
  assert.match(page,/role="status"/);
  assert.match(page,/<noscript>/);
  assert.match(style,/@media\(max-width:37rem\)/);
  assert.match(style,/@media print/);
  assert.match(style,/#print-packet\{display:block!important\}/);
  assert.match(style,/:focus-visible/);
});
test('build pipeline keeps inline local styles rather than discarding them',()=>{
  // house-style.mjs removes only a literal <style> head element, not this media-qualified one.
  assert.match(page,/<style media="all">/);
  assert.doesNotMatch(page,/<style>/);
});