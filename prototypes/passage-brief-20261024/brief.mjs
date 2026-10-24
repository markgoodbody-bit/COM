/**
 * Optional read-only short-text projection for Passage v0 saved notes.
 * Noncanonical source study, not an evidence authenticator or advice engine.
 * Uses the public Passage v0 field list and schema at COM@dad08b0845ad.
 */
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const SCHEMA = 'passage.v0';
export const FIELDS = Object.freeze([
  'future', 'people', 'scene', 'basis', 'source', 'checked',
  'move', 'actor', 'carrier', 'authority', 'clock', 'burden',
  'reply', 'revisit', 'change', 'outcome'
]);
const BASES = new Set(['UNKNOWN', 'REPORTED', 'OBSERVED', 'INFERRED', 'DISPUTED']);
const MAX_FIELD_UNITS = 4000;
const MAX_JSON_BYTES = 80000;

export function normalise(notes) {
  if (!notes || typeof notes !== 'object' || Array.isArray(notes)) {
    throw new TypeError('Expected Passage notes object.');
  }
  const out = Object.fromEntries(FIELDS.map(k => [k, k === 'basis' ? 'UNKNOWN' : '']));
  for (const k of FIELDS) {
    if (!Object.hasOwn(notes, k)) continue;
    if (typeof notes[k] !== 'string' || notes[k].length > MAX_FIELD_UNITS) {
      throw new TypeError('Invalid or overlong field: ' + k);
    }
    out[k] = notes[k];
  }
  if (!BASES.has(out.basis)) throw new TypeError('Unrecognised writer evidence label.');
  return out;
}

export function parseSaved(raw) {
  if (typeof raw !== 'string' || Buffer.byteLength(raw, 'utf8') > MAX_JSON_BYTES) {
    throw new TypeError('Invalid or oversized local Passage JSON.');
  }
  let parsed;
  try { parsed = JSON.parse(raw); }
  catch { throw new TypeError('Invalid JSON.'); }
  if (!parsed || parsed.schema !== SCHEMA || !Object.hasOwn(parsed, 'notes')) {
    throw new TypeError('Expected Passage v0 saved JSON.');
  }
  return normalise(parsed.notes);
}

// A quoted field occupies one physical line. Escape line/paragraph separators,
// NEL, C1/DEL and bidi formatting controls that JSON.stringify leaves literal.
// In particular, user text cannot mint a top-level Evidence/Verified heading.
function quote(value) {
  return JSON.stringify(value).replace(/[\u007f-\u009f\u2028-\u202e\u2066-\u2069]/g,
    character => '\\u' + character.charCodeAt(0).toString(16).padStart(4, '0'));
}

const LABELS = Object.freeze({
  future: 'Possible future (writer-proposed)',
  people: 'Affected scope (writer)',
  scene: 'Current situation (writer)',
  source: 'Source (writer)',
  checked: 'Source time (writer)',
  move: 'Possible move (writer)',
  actor: 'Actor (writer)',
  carrier: 'Practical carrier (writer)',
  authority: 'Authority or refusal (writer)',
  clock: 'Clock or boundary (writer)',
  burden: 'Burden (writer)',
  reply: 'Answer-back route (writer)',
  revisit: 'Revisit trigger (writer)',
  change: 'What could change this (writer)',
  outcome: 'Outcome (writer-claimed, unverified)'
});

export function renderBrief(input) {
  const notes = normalise(input);
  const lines = ["PASSAGE / BRIEF — writer's provisional notes"];
  let supplied = 0;
  for (const key of FIELDS) {
    if (key === 'basis') {
      if (notes.scene.trim() || notes.basis !== 'UNKNOWN') {
        lines.push('Evidence label (writer, not independently verified): ' + quote(notes.basis));
      }
      continue;
    }
    if (!notes[key].trim()) continue;
    supplied += 1;
    lines.push(LABELS[key] + ': ' + quote(notes[key]));
  }
  if (supplied === 0 && notes.basis === 'UNKNOWN') {
    lines.push('No substantive notes supplied.');
  }
  lines.push('Unverified; no permission to act is conferred. Prefer stronger domain methods when available.');
  return lines.join('\n') + '\n';
}

// Explicit local-file CLI; importing the module performs no IO or side effects.
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.length !== 3) {
    process.stderr.write('Usage: node brief.mjs <passage-v0-saved.json>\n');
    process.exitCode = 2;
  } else {
    try {
      const bytes = readFileSync(process.argv[2]);
      if (bytes.length > MAX_JSON_BYTES) throw new TypeError('Saved JSON exceeds 80 KB.');
      const raw = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
      process.stdout.write(renderBrief(parseSaved(raw)));
    } catch (err) {
      process.stderr.write('Brief projection refused: ' + err.message + '\n');
      process.exitCode = 2;
    }
  }
}
