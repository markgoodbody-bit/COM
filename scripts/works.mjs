// Normal, offline source build. No proposal builder or network acquisition.
import { readFile, lstat, readdir, mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';

export const WORKS = JSON.parse(await readFile(new URL('./WORKS_COPIES.json', import.meta.url)));
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const safe = route => /^(works|art)\/[a-zA-Z0-9._/-]+$/.test(route)
  && !route.split('/').some(part => ['', '.', '..'].includes(part))
  && !route.startsWith('art/camp-fire');

async function regular(root, route) {
  const pieces = route.split('/');
  for (let i = 1; i <= pieces.length; i++) {
    const item = await lstat(path.join(root, ...pieces.slice(0, i)));
    if (item.isSymbolicLink() || (i < pieces.length ? !item.isDirectory() : !item.isFile())) {
      throw Error('Nonregular works source: ' + route);
    }
  }
  return readFile(path.join(root, route));
}

export async function verifyWorks(root) {
  const files = new Map();
  for (const [route, expected] of Object.entries(WORKS.files)) {
    if (!safe(route)) throw Error('Unsafe works route: ' + route);
    const bytes = await regular(root, route);
    if (bytes.length !== expected.bytes || sha(bytes) !== expected.sha256) {
      throw Error('Works identity mismatch: ' + route);
    }
    files.set(route, bytes);
  }
  // Stale or accidentally added work pages must not silently join the shelf.
  async function walk(relative) {
    for (const entry of await readdir(path.join(root, relative), { withFileTypes: true })) {
      const route = relative + '/' + entry.name;
      if (entry.isDirectory()) await walk(route);
      else if (!entry.isFile() || !files.has(route)) throw Error('Undeclared works source: ' + route);
    }
  }
  await walk('works');
  return files;
}

export async function copyWorks(source, destination) {
  const files = await verifyWorks(source); // All custody checks before any copy.
  for (const [route, bytes] of files) {
    await mkdir(path.dirname(path.join(destination, route)), { recursive: true });
    await writeFile(path.join(destination, route), bytes);
  }
  await verifyWorks(destination);
  return files.size;
}
