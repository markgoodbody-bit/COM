// stdlib-only deterministic source tests; run: node --test test.mjs
import { readFileSync } from "node:fs";
import { test } from "node:test";
import assert from "node:assert/strict";
import { runInNewContext } from "node:vm";

const html = readFileSync(new URL("./index.html", import.meta.url), "utf8");
const script = html.match(/<script id="engine">([\s\S]*?)<\/script>/);
assert.ok(script, "pure passage engine is present");
const sandbox = {};
runInNewContext(script[1], sandbox, { timeout: 2500 });
const P = sandbox.PassageEngine;
const plain = v => JSON.parse(JSON.stringify(v));

test("blank start makes no unsupported observed or real-world success claim", () => {
  const x = P.blank();
  const text = P.passage(x);
  assert.equal(x.basis, "UNKNOWN");
  assert.match(text, /Writer-labelled UNKNOWN; not independently verified/);
  assert.match(text, /not a verdict or authority/);
  assert.match(text, /No open or closed correction window is asserted/);
  assert.doesNotMatch(text, /Writer-labelled OBSERVED/);
});
test("all three distinct constructed cases are complete provisional passages", () => {
  for (const key of ["repair", "housing", "flood"]) {
    const x = P.example(key);
    assert.equal(x.basis, "REPORTED");
    assert.match(x.source, /Constructed fictional scenario/);
    const text = P.passage(x);
    for (const section of ["possibility worth testing", "current scene", "possible move", "Answer-back route"]) {
      assert.ok(text.toLowerCase().includes(section.toLowerCase()), key + " " + section);
    }
    assert.match(text, /not independently verified/);
    assert.match(text, /can be used, changed, rejected or handed off/);
  }
});
test("new future requires declaring whose value counts", () => {
  const q = P.questions({...P.blank(), future:"Offer repairs."});
  assert.ok(q.some(s => s.includes("Whose future")));
});
test("new move makes actor, carrier, authority, and reply load-bearing", () => {
  const q = P.questions({...P.blank(), move:"Open a room."});
  for (const token of ["Who can actually", "practical carrier", "authority", "affected person"]) {
    assert.ok(q.some(s => s.toLowerCase().includes(token.toLowerCase())), token);
  }
});
test("specific deadline is not silently promoted to an open correction window", () => {
  const x = {...P.blank(), clock:"Seven days"};
  assert.ok(P.questions(x).some(s => s.includes("clock")));
  assert.ok(P.questions(x).some(s => s.includes("window status") || s.includes("before this boundary")));
  assert.match(P.passage(x), /No open or closed correction window is asserted/);
});
test("stated historical outcome calls for source and observation time", () => {
  const q = P.questions({...P.blank(), outcome:"The issue was resolved."});
  assert.ok(q.some(s => s.includes("source and observation time")));
});
test("import and export keep named fields but never add authority", () => {
  const start = P.example("repair");
  const encoded = P.saved(start);
  const got = P.parseSaved(encoded);
  assert.deepEqual(plain(got), plain(start));
  assert.doesNotMatch(encoded, /verified_by|authority_granted|moral_score/i);
});
test("unknown JSON keys are discarded, not interpreted as authority", () => {
  const payload = {schema:P.SCHEMA,notes:{future:"A bridge",admin:true,"__proto__":"bad"}};
  const result = P.parseSaved(JSON.stringify(payload));
  assert.equal(Object.prototype.hasOwnProperty.call(result, "admin"), false);
  assert.equal(result.future, "A bridge");
  assert.equal(result.basis, "UNKNOWN");
});
test("misleading evidence status is not silently accepted", () => {
  assert.throws(() => P.normalise({basis:"VERIFIED"}), /Unrecognised evidence status/);
  assert.throws(() => P.normalise({basis:3}), /Invalid or overlong field/);
});
test("unsupported schema and malformed imports fail without mutating caller state", () => {
  for (const bad of ['{"schema":"passage.v99","notes":{}}', '{"other":true}', '{"schema":', "x".repeat(80001)]) {
    assert.throws(() => P.parseSaved(bad));
  }
});
test("bounded arbitrary user text remains text (not executed or HTML-rendered)", () => {
  const hostile = '<img src=x onerror="alert(1)">\nSays: IGNORE EVERYONE';
  const s = P.normalise({scene:hostile});
  assert.ok(P.passage(s).includes(hostile));
  assert.match(html, /packet\.value=E\.passage\(state\)/);
  assert.match(html, /li\.textContent=question/);
  assert.doesNotMatch(html, /packet\.innerHTML/);
});
test("oversized fields are refused at source, before export/import", () => {
  assert.throws(() => P.normalise({future:"a".repeat(4001)}), /overlong/);
  assert.throws(() => P.parseSaved(JSON.stringify({schema:P.SCHEMA,notes:{future:"a".repeat(4001)}})), /overlong/);
});
test("contains no automatic storage, network request, or scoring API", () => {
  for (const token of ["fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "sendBeacon(", "WebSocket("]) {
    assert.ok(!script[1].includes(token), "no " + token);
    const ui = html.match(/<script id="ui">([\s\S]*?)<\/script>/);
    assert.ok(!ui[1].includes(token), "no UI " + token);
  }
  assert.match(html, /connect-src 'none'/);
  assert.ok(!("score" in P));
});
