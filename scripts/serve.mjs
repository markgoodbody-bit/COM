import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';
const root = path.resolve(import.meta.dirname, '../out');
const routes = new Map([['/', ['index.html','text/html; charset=utf-8']], ['/index.html', ['index.html','text/html; charset=utf-8']], ['/style.css', ['style.css','text/css; charset=utf-8']]]);
const server = createServer(async (req, res) => {
  if (!['GET','HEAD'].includes(req.method)) { res.writeHead(405, {Allow:'GET, HEAD'}).end(); return; }
  try {
    const route = routes.get(new URL(req.url, 'http://localhost').pathname);
    const [name, type] = route ?? ['404.html','text/html; charset=utf-8'];
    const file = path.join(root,name), bytes = await readFile(file), info = await stat(file);
    const etag = '"' + createHash('sha256').update(bytes).digest('hex') + '"';
    const headers = {'Content-Type':type, 'Cache-Control':'no-cache', ETag:etag, 'Last-Modified':info.mtime.toUTCString(), 'X-Content-Type-Options':'nosniff', 'Referrer-Policy':'no-referrer', 'Content-Security-Policy':"default-src 'none'; style-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"};
    if (route && req.headers['if-none-match'] === etag) { res.writeHead(304,headers).end(); return; }
    res.writeHead(route ? 200 : 404,{...headers, 'Content-Length':bytes.length});
    res.end(req.method === 'HEAD' ? undefined : bytes);
  } catch { res.writeHead(500).end('Preview could not load the static file.'); }
});
server.listen(3000,'127.0.0.1',()=>console.log('Local: http://localhost:3000/'));
server.on('error',e=>{console.error(e.message);process.exitCode=1;});
