import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, cp, writeFile, unlink, readFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { verifyResources, copyResources } from './resources.mjs';

const source = path.resolve(import.meta.dirname, '../public/resources');
test('all copies, declarations, local dependency paths and directory navigation exist', async () => {
  const { files, inventory } = await verifyResources(source);
  assert.equal(inventory.projects.length, 2);
  assert.ok(inventory.snapshot_files.length >= 30, 'release sync must retain earlier snapshots as well as released snapshots');
  let copies = 0;
  for (const project of inventory.projects) {
    for (const file of project.files) {
      assert.ok(files.has(file.current.slice(11)));
      if (file.snapshot_mode === 'copy') {
        assert.ok(files.get(file.current.slice(11)).equals(files.get(file.snapshot.slice(11))));
      } else if (file.snapshot_mode === 'preserve') {
        assert.ok(file.snapshot);
        assert.ok(files.has(file.snapshot.slice(11)));
        assert.notEqual(file.sha256, file.snapshot_identity.sha256);
      } else {
        assert.equal(file.snapshot, null);
      }
      copies++;
    }
    for (const dep of project.dependencies.filter(d => d.kind === 'local')) {
      assert.ok(files.has(project.id + '/' + dep.target), dep.target);
    }
  }
  assert.equal(copies, 16);
  for (const [name, bytes] of files) if (name.endsWith('.html')) {
    const page = bytes.toString();
    assert.doesNotMatch(page, /<(script|iframe|form|object)\b/i);
    for (const [, href] of page.matchAll(/href="([^"]+)"/g)) {
      const url = new URL(href, 'https://pleasestartfromhere.com/resources/' + name);
      if (url.origin !== 'https://pleasestartfromhere.com' || !url.pathname.startsWith('/resources/')) continue;
      let target = url.pathname.slice(11);
      if (!target || target.endsWith('/')) target += 'index.html';
      assert.ok(files.has(target), name + ' -> ' + target);
    }
  }
});


test('D070 released snapshots remain byte-identical after D071 rights sync', async () => {
  const expected = new Map([
    ['snapshots/trace/8310d2531d3b2fe4e3b44c92d1d544a322f52bf4/README.md', 'a6f95cf2bac4558e4b5b56b0b38d6e498541d3d0'],
    ['snapshots/trace/8310d2531d3b2fe4e3b44c92d1d544a322f52bf4/TRACE-SPINE.md', '2e5afe78d0033d47582af9ffaa94f0d0e5a51bc7'],
    ['snapshots/trace/8310d2531d3b2fe4e3b44c92d1d544a322f52bf4/TRACE.md', 'e9c0a9906c663ac4f9887ee42f8595edc74d2f92'],
    ['snapshots/mechanical-ethics/25a9d793af1cded26dd2d766e1d1c08e1b30f652/README.md', '735e91055adbbc2a45faec6f7c7f36a83710e727'],
    ['snapshots/mechanical-ethics/25a9d793af1cded26dd2d766e1d1c08e1b30f652/MECHANICAL_ETHICS.md', 'e232a29c5b6492930ff5b94b005c948f67ba6067'],
    ['snapshots/mechanical-ethics/25a9d793af1cded26dd2d766e1d1c08e1b30f652/MECHANICAL_ETHICS.pdf', 'b7579079bbeb32912b8b280ce444e0b41d330a7f'],
  ]);
  const { files } = await verifyResources(source);
  const gitBlob = bytes => createHash('sha1')
    .update(Buffer.from('blob ' + bytes.length + '\0'))
    .update(bytes)
    .digest('hex');
  for (const [pathName, expectedBlob] of expected) {
    assert.ok(files.has(pathName), pathName);
    assert.equal(gitBlob(files.get(pathName)), expectedBlob, pathName);
  }
});

for (const kind of ['missing', 'changed', 'undeclared', 'inventory']) test('refuses ' + kind + ' input', async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'psfh-resource-test-'));
  await cp(source, root, { recursive: true });
  const target = path.join(root, 'trace/TRACE.md');
  if (kind === 'missing') await unlink(target);
  else if (kind === 'changed') await writeFile(target, 'changed');
  else if (kind === 'undeclared') await writeFile(path.join(root, 'extra.txt'), 'unreviewed');
  else await writeFile(path.join(root, 'inventory.json'), '{}');
  await assert.rejects(verifyResources(root));
});

test('normal copy preserves bytes and refuses changed fixed snapshot', async () => {
  const target = await mkdtemp(path.join(os.tmpdir(), 'psfh-resource-snapshot-test-'));
  await copyResources(source, target);
  await verifyResources(target);
  const { inventory } = await verifyResources(source);
  const snapshot = inventory.projects[0].files.find(file => file.snapshot_mode === 'copy').snapshot.slice(11);
  await writeFile(path.join(target, snapshot), 'different snapshot');
  await assert.rejects(copyResources(source, target), /snapshot replacement/);
  assert.equal((await readFile(path.join(target, snapshot))).toString(), 'different snapshot');
});
