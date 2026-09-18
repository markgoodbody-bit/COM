// Normal builds are offline: verify the reviewed inventory and every declared file.
import { readFile, readdir, lstat, mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';

export const INVENTORY_SHA256 = '5fafbf3658e7e73f647aa47d5235008899b59ef99ac2849d6129e1f687257dda';
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
function safe(relative) {
  if (!/^[a-zA-Z0-9._/-]+$/.test(relative) || relative.split('/').some(p => ['', '.', '..'].includes(p))) throw new Error('Unsafe resource path');
  return relative;
}
export async function verifyResources(root) {
  const raw = await readFile(path.join(root, 'inventory.json'));
  if (sha(raw) !== INVENTORY_SHA256) throw new Error('Resource inventory changed: review before updating pin');
  const inventory = JSON.parse(raw);
  const expected = new Map();
  for (const project of inventory.projects) for (const file of project.files) {
    if (!file.current.startsWith('/resources/')) throw new Error('Resource prefix mismatch');
    expected.set(safe(file.current.slice('/resources/'.length)), file);
    if (file.snapshot) {
      if (!file.snapshot.startsWith('/resources/')) throw new Error('Resource prefix mismatch');
      const snapshotRule = file.snapshot_identity || file;
      expected.set(safe(file.snapshot.slice('/resources/'.length)), snapshotRule);
    }
  }
  for (const file of [...inventory.generated_files, ...inventory.snapshot_files]) {
    const previous = expected.get(file.path);
    if (previous && (previous.sha256 !== file.sha256 || previous.bytes !== file.bytes)) throw new Error('Conflicting resource declaration');
    if (!previous) expected.set(safe(file.path), file);
  }
  const files = new Map([['inventory.json', raw]]);
  async function walk(relative = '') {
    if (!(await lstat(path.join(root, relative))).isDirectory()) throw new Error('Resource directory missing');
    for (const entry of await readdir(path.join(root, relative), { withFileTypes: true })) {
      const child = relative ? relative + '/' + entry.name : entry.name;
      safe(child);
      if (entry.isDirectory()) await walk(child);
      else if (entry.isFile()) {
        const bytes = await readFile(path.join(root, child));
        if (child === 'inventory.json') continue;
        const rule = expected.get(child);
        if (!rule || bytes.length !== rule.bytes || sha(bytes) !== rule.sha256) throw new Error('Resource identity mismatch: ' + child);
        if (rule.git_blob_sha1 && createHash('sha1').update(Buffer.from(`blob ${bytes.length}\0`)).update(bytes).digest('hex') !== rule.git_blob_sha1) throw new Error('Git body mismatch: ' + child);
        files.set(child, bytes);
      } else throw new Error('Resource symlink/nonregular entry refused: ' + child);
    }
  }
  await walk();
  if (files.size !== expected.size + 1) throw new Error('Missing resource file');
  return { files, inventory };
}

export async function copyResources(source, destination) {
  const { files } = await verifyResources(source);
  // Validate the entire source before writing; do not overwrite a fixed edition.
  for (const [relative, bytes] of files) if (relative.startsWith('snapshots/')) {
    try {
      const target = path.join(destination, relative);
      if (!(await lstat(target)).isFile() || !(await readFile(target)).equals(bytes)) throw new Error('Refusing snapshot replacement: ' + relative);
    } catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  for (const [relative, bytes] of files) {
    await mkdir(path.dirname(path.join(destination, relative)), { recursive: true });
    await writeFile(path.join(destination, relative), bytes);
  }
  await verifyResources(destination); // catches stale undeclared output too
  return files.size;
}
