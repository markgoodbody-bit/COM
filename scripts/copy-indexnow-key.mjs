import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const key = '352408ff99c5e8531fe80000b491b08b';
const filename = `${key}.txt`;
const source = await readFile(path.join(root, 'public', filename));
const expected = `${key}\n`;
if (source.toString('utf8') !== expected) throw new Error('IndexNow key file does not contain the expected key.');
await writeFile(path.join(root, 'out', filename), source);
console.log(`IndexNow ownership key copied: ${filename}`);
