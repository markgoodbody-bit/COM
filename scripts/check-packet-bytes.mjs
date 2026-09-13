import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const sourceRel = 'public/packet.md';
const builtRel = 'out/packet.md';

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function report(label, bytes) {
  console.log(`${label}: ${bytes.length} bytes; SHA-256 ${sha256(bytes)}`);
}

const committed = execFileSync('git', ['show', `HEAD:${sourceRel}`], {
  cwd: root,
  encoding: null,
  maxBuffer: 1024 * 1024,
});
const working = await readFile(path.join(root, sourceRel));
const built = await readFile(path.join(root, builtRel));

report('repository packet', committed);
report('working packet', working);
report('built packet', built);

if (committed.includes(0x0d)) {
  throw new Error('Committed project packet contains CR bytes; expected LF byte identity');
}
if (!committed.equals(working)) {
  throw new Error('Repository packet bytes differ from checked-out public/packet.md');
}
if (!working.equals(built)) {
  throw new Error('Checked-out project packet bytes differ from out/packet.md');
}

console.log('Project packet exact-byte check: repository == working == built');
