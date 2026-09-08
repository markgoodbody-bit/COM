import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, cp, writeFile, unlink, readFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { verifyResources, copyResources } from './resources.mjs';

const source = path.resolve(import.meta.dirname, '../public/resources');
test('all copies, declarations, local dependency paths and directory navigation exist', async () => {
  const { files, inventory } = await verifyResources(source);
  assert.equal(files.size, 33);
  let copies = 0;
  for (const project of inventory.projects) {
    for (const file of project.files) {
      assert.ok(files.get(file.current.slice(11)).equals(files.get(file.snapshot.slice(11))));
      copies++;
    }
    for (const dep of project.dependencies.filter(d => d.kind === 'local')) {
      assert.ok(files.has(project.id + '/' + dep.target), dep.target);
      assert.ok(files.has('snapshots/' + project.id + '/' + project.commit + '/' + dep.target));
    }
  }
  assert.equal(copies, 14);
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
  const snapshot = inventory.projects[0].files[0].snapshot.slice(11);
  await writeFile(path.join(target, snapshot), 'different snapshot');
  await assert.rejects(copyResources(source, target), /snapshot replacement/);
  assert.equal((await readFile(path.join(target, snapshot))).toString(), 'different snapshot');
});
