// Disposable LOCAL layout harness. Never part of the publishing output.
import { cp, mkdtemp, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { createPreviewServer } from '../../scripts/serve.mjs';

const source = path.resolve(import.meta.dirname, '../../out');
const root = await mkdtemp(path.join(tmpdir(), 'psfh-layout-'));
console.log('Disposable directory:', root);
await cp(source, root, { recursive: true });
const html = await readFile(path.join(root, 'index.html'), 'utf8');
const variants = {
  'scrim55': '.hero-heading::before { background: rgba(0,0,0,.55); }',
  'text200': ':root { font-size: 200% !important; }',
  'text200-scrim55': ':root { font-size: 200% !important; } .hero-heading::before { background: rgba(0,0,0,.55); }',
};
for (const [name, css] of Object.entries(variants)) {
  await writeFile(path.join(root, name + '.html'), html.replace('</head>', '<style>' + css + '</style></head>'));
}
const server = await createPreviewServer(root);
server.listen(3001, '127.0.0.1', () => console.log('LOCAL ONLY: http://localhost:3001/ ; /scrim55.html ; /text200.html ; /text200-scrim55.html'));
async function cleanup() {
  server.close();
  const resolved = path.resolve(root);
  if (path.dirname(resolved) !== path.resolve(tmpdir()) || !path.basename(resolved).startsWith('psfh-layout-')) throw new Error('Unexpected cleanup target');
  await rm(resolved, { recursive: true });
  console.log('Removed disposable layout copy; maintained source unchanged.');
}
process.once('SIGINT', async () => { await cleanup(); process.exit(0); });
process.once('SIGTERM', async () => { await cleanup(); process.exit(0); });
