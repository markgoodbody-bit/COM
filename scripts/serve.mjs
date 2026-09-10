import { createServer } from 'node:http';
import { readFile, lstat, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const types = new Map([
  ['.html', 'text/html; charset=utf-8'], ['.css', 'text/css; charset=utf-8'],
  ['.md', 'text/markdown; charset=utf-8'], ['.txt', 'text/plain; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'], ['.xml', 'application/xml; charset=utf-8'],
  ['.pdf', 'application/pdf'], ['.png', 'image/png'], ['.svg', 'image/svg+xml'],
  ['.jpg', 'image/jpeg'],
  ['.ico', 'image/x-icon'],
  ['.js', 'text/javascript; charset=utf-8'],
]);

// Serve a frozen inventory of this build, never a path derived from a request.
// npm run dev rebuilds first. Restart after rebuilding to load the new inventory.
export async function createPreviewServer(root = path.resolve(import.meta.dirname, '../out')) {
  const routes = new Map();
  async function collect(directory, prefix = '') {
    if ((await lstat(directory)).isSymbolicLink()) throw new Error('Preview refuses linked directories');
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      if (entry.name.startsWith('.')) continue;
      const file = path.join(directory, entry.name);
      const relative = prefix + entry.name;
      if (entry.isSymbolicLink()) throw new Error('Preview refuses linked entries');
      if (entry.isDirectory()) { await collect(file, relative + '/'); continue; }
      if (!entry.isFile()) throw new Error('Preview refuses non-file entries');
      const type = types.get(path.extname(entry.name));
      if (!type) throw new Error('Unrecognised public artifact type: ' + relative);
      const bytes = await readFile(file), info = await lstat(file);
      const item = { bytes, type, modified: info.mtime.toUTCString(),
        etag: '"' + createHash('sha256').update(bytes).digest('hex') + '"' };
      routes.set('/' + relative, item);
      if (entry.name === 'index.html') routes.set('/' + prefix, item);
    }
  }
  await collect(root);
  if (!routes.has('/') || !routes.has('/404.html')) throw new Error('Build lacks root or error page');
  return createServer((req, res) => {
    if (!['GET', 'HEAD'].includes(req.method)) {
      res.writeHead(405, { Allow: 'GET, HEAD' }).end(); return;
    }
    let route;
    try { route = routes.get(decodeURIComponent(new URL(req.url, 'http://localhost').pathname)); }
    catch { res.writeHead(400).end('Invalid path.'); return; }
    const item = route ?? routes.get('/404.html');
    const headers = {
      'Content-Type': item.type, 'Cache-Control': 'no-cache', ETag: item.etag,
      'Last-Modified': item.modified, 'X-Content-Type-Options': 'nosniff',
      'Referrer-Policy': 'no-referrer',
      // Local navigation enhancement only; no network or form submission.
      'Content-Security-Policy': "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
    };
    if (route && req.headers['if-none-match'] === item.etag) {
      res.writeHead(304, headers).end(); return;
    }
    res.writeHead(route ? 200 : 404, { ...headers, 'Content-Length': item.bytes.length });
    res.end(req.method === 'HEAD' ? undefined : item.bytes);
  });
}

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  const server = await createPreviewServer();
  server.listen(3000, '127.0.0.1', () => console.log('Local: http://localhost:3000/ (build snapshot; restart after rebuilding)'));
  server.on('error', error => { console.error(error.message); process.exitCode = 1; });
}
