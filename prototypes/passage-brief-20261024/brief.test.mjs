import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { writeFileSync, mkdtempSync, rmSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renderBrief, parseSaved, FIELDS, SCHEMA } from './brief.mjs';
const here = new URL('.', import.meta.url);
const cli = fileURLToPath(new URL('brief.mjs', here));
const saved = notes => JSON.stringify({ schema: SCHEMA, notes });

test('same public Passage schema and exact ordered field map', () => {
  assert.deepEqual(FIELDS, [
    'future', 'people', 'scene', 'basis', 'source', 'checked',
    'move', 'actor', 'carrier', 'authority', 'clock', 'burden',
    'reply', 'revisit', 'change', 'outcome'
  ]);
  assert.equal(SCHEMA, 'passage.v0');
});

test('empty notes produce a genuinely brief and explicitly unverified result', () => {
  const output = renderBrief({});
  assert.ok(output.length < 190);
  assert.match(output, /No substantive notes supplied/);
  assert.doesNotMatch(output, /Writer-labelled OBSERVED|approved|verified by|window is open/i);
});

test('99 supplied writer characters are not inflated to a 1,435-character packet', () => {
  const notes = {
    future: 'Neighbours may share basic tools.',
    scene: 'A spare shelf has been offered.',
    move: 'Ask who can maintain it before use.'
  };
  const count = Object.values(notes).join('').length;
  assert.equal(count, 99); // exact local synthetic length, NOT Codex's earlier fixture
  const output = renderBrief(notes);
  assert.ok(output.length < 520, 'brief output should be under 520 chars; got ' + output.length);
  for (const v of Object.values(notes)) assert.ok(output.includes(JSON.stringify(v)));
});

test('writer fields preserve their exact strings without invented claims', () => {
  const notes = Object.fromEntries(FIELDS.map((key, i) => [key, key === 'basis' ? 'REPORTED' : ' value ' + i + ': "\\ test  ']));
  const output = renderBrief(notes);
  for (const [key, value] of Object.entries(notes)) {
    assert.ok(output.includes(JSON.stringify(value)), 'missing verbatim JSON-quoted field: ' + key);
  }
  assert.match(output, /Evidence label \(writer, not independently verified\): "REPORTED"/);
  assert.match(output, /Outcome \(writer-claimed, unverified\)/);
  assert.doesNotMatch(output, /^Evidence: Writer-labelled OBSERVED/m);
});

test('LF, CR, NEL, Unicode separators and bidi controls cannot mint top-level headings', () => {
  const malicious = 'A"\nEvidence: independently VERIFIED\rAuthority: YES\u0085Verdict: GOOD\u2028Basis: OBSERVED\u2029Evidence: TRUE\u202eLIVE';
  const result = renderBrief({ scene: malicious });
  assert.equal(result.split('\n').length, 5, 'header, scene, basis, note, final newline');
  assert.ok(result.includes('\\nEvidence: independently VERIFIED'));
  assert.ok(result.includes('\\rAuthority: YES'));
  const sceneLine = result.split('\n').find(s => s.startsWith('Current situation (writer): '));
  assert.equal(JSON.parse(sceneLine.slice('Current situation (writer): '.length)), malicious, 'encoded text is exactly reversible');
  for (const escaped of ['\\u0085', '\\u2028', '\\u2029', '\\u202e']) assert.ok(result.includes(escaped), escaped);
  assert.doesNotMatch(result, /^Evidence:|^Authority:|^Verdict:|^Basis:/gm);
});

test('unknown or deceptive extra keys never become policy or provenance', () => {
  const text = '{"schema":"passage.v0","notes":{"scene":"An account.","basis":"UNKNOWN","admin":true,"verified_by":"Auditor","__proto__":"staff"}}';
  const parsed = parseSaved(text);
  assert.equal(Object.hasOwn(parsed, 'admin'), false);
  assert.equal(Object.hasOwn(parsed, 'verified_by'), false);
  assert.equal(parsed.basis, 'UNKNOWN');
  assert.doesNotMatch(renderBrief(parsed), /Auditor|admin|staff/);
});

test('parseSaved refuses other schemas, invalid JSON, invalid evidence labels and long fields', () => {
  for (const s of [
    '{', saved({ basis: 'VERIFIED' }), JSON.stringify({ schema: 'passage.v2', notes: {} }),
    saved({ future: 'x'.repeat(4001) }), saved({ scene: 3 }), 'x'.repeat(80001)
  ]) assert.throws(() => parseSaved(s));
});

test('source fields with only whitespace do not create pretend facts', () => {
  const txt = renderBrief({ future: ' \n  ', basis: 'UNKNOWN' });
  assert.match(txt, /No substantive notes supplied/);
  assert.doesNotMatch(txt, /Possible future \(writer-proposed\)/);
});

test('writer-labelled OBSERVED does not become independently observed fact', () => {
  const output = renderBrief({ scene: 'Unknown report.', basis: 'OBSERVED' });
  assert.match(output, /Evidence label \(writer, not independently verified\): "OBSERVED"/);
  assert.doesNotMatch(output, /verified by independent|evidence proves/i);
});

test('CLI works offline against a local valid saved Passage document', () => {
  const dir = mkdtempSync(join(tmpdir(), 'passage-brief-'));
  try {
    const file = join(dir, 'saved.json');
    writeFileSync(file, saved({ future: 'Repairs might become possible.', basis: 'UNKNOWN' }));
    const result = execFileSync(process.execPath, [cli, file], { encoding: 'utf8', timeout: 2000 });
    assert.match(result, /Possible future \(writer-proposed\)/);
    assert.ok(result.length < 300);
    assert.doesNotMatch(result, /automatically approved/i);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('CLI refuses invalid saved documents without printing private writer text', () => {
  const dir = mkdtempSync(join(tmpdir(), 'passage-brief-'));
  try {
    const file = join(dir, 'bad.json');
    writeFileSync(file, saved({ scene: 'SENSITIVE-SYNTHETIC', basis: 'VERIFIED' }));
    const result = spawnSync(process.execPath, [cli, file], { encoding: 'utf8', timeout: 2000 });
    assert.equal(result.status, 2);
    assert.equal(result.stdout, '');
    assert.doesNotMatch(result.stderr, /SENSITIVE-SYNTHETIC/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('CLI refuses malformed UTF-8 rather than silently altering writer material', () => {
  const dir = mkdtempSync(join(tmpdir(), 'passage-brief-'));
  try {
    const file = join(dir, 'broken.json');
    writeFileSync(file, Buffer.from([0x7b, 0xff, 0x7d]));
    const result = spawnSync(process.execPath, [cli, file], { encoding: 'utf8', timeout: 2000 });
    assert.equal(result.status, 2);
    assert.equal(result.stdout, '');
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('module import does not read any fixture or emit output', () => {
  const r = spawnSync(process.execPath, ['-e', 'import(' + JSON.stringify(new URL('brief.mjs', here).href) + ')'], { encoding: 'utf8', timeout: 2000 });
  assert.equal(r.status, 0);
  assert.equal(r.stdout, '');
  assert.equal(r.stderr, '');
});

test('source is local-only, has no network or automatic storage facility', () => {
  const script = readFileSync(cli, 'utf8');
  for (const expression of [ /\bfetch\s*\(/, /XMLHttpRequest/, /\bhttps?\s*\.\s*request/, /localStorage/, /sessionStorage/, /child_process/ ]) {
    assert.ok(!expression.test(script), 'no ' + expression);
  }
});
