// Local test instrument only. Identical build bytes; ?nojs=1 tightens CSP.
// No production source, browser preference or installed service changes.
import { createPreviewServer } from '../../scripts/serve.mjs';
const server = await createPreviewServer();
server.prependListener('request', (req, res) => {
  if (new URL(req.url, 'http://localhost').searchParams.get('nojs') !== '1') return;
  const original = res.writeHead;
  res.writeHead = function(status, headers) {
    return original.call(this, status, {...headers,
      'Content-Security-Policy': headers['Content-Security-Policy'].replace("script-src 'self'", "script-src 'none'")});
  };
});
server.listen(8852, '127.0.0.1', () => console.log('Local: http://127.0.0.1:8852/'));
