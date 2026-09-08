import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { createPreviewServer } from './serve.mjs';

const root = path.resolve(import.meta.dirname, '../out');
test('actual build files and directory indexes are delivered, without enabling writes', async () => {
  const server = await createPreviewServer(root);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = 'http://127.0.0.1:' + server.address().port;
  try {
    let checked = 0;
    async function check(directory, prefix = '') {
      for (const item of await readdir(directory, { withFileTypes: true })) {
        if (item.isDirectory()) { await check(path.join(directory, item.name), prefix + item.name + '/'); continue; }
        const expected = await readFile(path.join(directory, item.name));
        const response = await fetch(base + '/' + prefix + item.name);
        assert.equal(response.status, 200, prefix + item.name);
        assert.deepEqual(Buffer.from(await response.arrayBuffer()), expected);
        if (item.name === 'index.html') {
          const alias = await fetch(base + '/' + prefix);
          assert.equal(alias.status, 200);
          assert.deepEqual(Buffer.from(await alias.arrayBuffer()), expected);
        }
        checked++;
      }
    }
    await check(root);
    assert.ok(checked > 0);
    const head = await fetch(base + '/discussion/', { method: 'HEAD' });
    assert.equal(head.status, 200); assert.equal(await head.text(), '');
    assert.equal((await fetch(base + '/discussion/', { headers: { 'If-None-Match': head.headers.get('etag') } })).status, 304);
    assert.match(head.headers.get('content-security-policy'), /style-src 'self' 'unsafe-inline'/);
    assert.match(head.headers.get('content-security-policy'), /default-src 'none'/);
    assert.equal((await fetch(base + '/discussion/', { method: 'POST', body: 'not a contribution' })).status, 405);
    for (const url of ['/scripts/serve.mjs', '/.env', '/%2e%2e/package.json', '/unknown/', '/resources/%2e%2e/%2e%2e/package.json']) {
      const absent = await fetch(base + url);
      assert.equal(absent.status, 404, url);
      assert.deepEqual(Buffer.from(await absent.arrayBuffer()), await readFile(path.join(root, '404.html')));
    }
    assert.equal((await fetch(base + '/bad%ZZ')).status, 400);
    const pdf = await fetch(base + '/resources/mechanical-ethics/MECHANICAL_ETHICS.pdf', { method: 'HEAD' });
    assert.equal(pdf.headers.get('content-type'), 'application/pdf');
    console.log('Exact preview build files checked:', checked);
  } finally { await new Promise(resolve => server.close(resolve)); }
});
