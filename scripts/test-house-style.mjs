import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { sharedStyle } from './house-style.mjs';

test('head-only transformation preserves markup-like source payload', () => {
  const input = '<html><head><style>body{color:red}</style></head><body><pre>&lt;style&gt;text&lt;/style&gt;</pre></body></html>';
  const output = sharedStyle(input);
  assert.equal(output.split('</head>')[1], input.split('</head>')[1]);
  assert.equal(sharedStyle(output), output);
  assert.throws(() => sharedStyle('<body>no head</body>'));
});

test('unmodified HTML bodies and raw resources survive the first-contact and style build', async () => {
  const baseline = '50caedc89646b7337a86a5610cef24426b518cf3';
  const publishing = 'C:/Users/markg/Downloads/DEV/campfire-door-pages';
  let pages = 0, unchangedBodies = 0, editionOnlyBodies = 0, unchanged = 0;
  async function check(dir, prefix = '') {
    for (const entry of await readdir(dir, { withFileTypes: true })) {
      const relative = prefix + entry.name;
      if (entry.isDirectory()) { await check(dir + '/' + entry.name, relative + '/'); continue; }
      const actual = await readFile(dir + '/' + entry.name);
      const before = execFileSync('git', ['show', baseline + ':' + relative], { cwd: publishing, maxBuffer: 10 * 1024 * 1024 });
      if (relative.endsWith('.html')) {
        const html = actual.toString('utf8');
        // Only the root and appended reader history have substantive edits.
        // The four full source views change their wrapper edition, not payload.
        if (!['index.html', 'changes.html'].includes(relative)) {
          const normalize = text => text.replace('Site Preview 0.8</p>', 'Site Preview 0.7.2</p>');
          assert.equal(normalize(html.slice(html.indexOf('<body'))), before.toString('utf8').slice(before.toString('utf8').indexOf('<body')), relative);
          if (html.slice(html.indexOf('<body')) === before.toString('utf8').slice(before.toString('utf8').indexOf('<body'))) unchangedBodies++;
          else editionOnlyBodies++;
        }
        assert.match(html, /<link rel="stylesheet" href="\.?\/?style\.css">/, relative);
        assert.doesNotMatch(html.slice(0, html.indexOf('</head>')), /<style>/, relative);
        pages++;
      } else if (!['style.css', 'manifest.json', 'explore/map.json', 'changes.md'].includes(relative)) {
        assert.deepEqual(actual, before, relative); unchanged++;
      }
    }
  }
  await check('out');
  const manifest = JSON.parse(await readFile('out/manifest.json'));
  const sha = b => createHash('sha256').update(b).digest('hex');
  assert.equal(manifest.provenance.presentation.stylesheet_sha256, sha(await readFile('out/style.css')));
  const map = JSON.parse(await readFile('out/explore/map.json'));
  for (const item of map.resources) {
    const bytes = await readFile('out/explore/' + item.path);
    assert.equal(item.bytes, bytes.length, item.path); assert.equal(item.sha256, sha(bytes), item.path);
  }
  console.log({ checkedHtmlPages: pages, unchangedHtmlBodies: unchangedBodies, editionOnlyBodies, explicitlyEditedBodies: 2, unchangedOtherFiles: unchanged, mapEntries: map.resources.length });
});

test('declared light and dark text pairs meet the selected 4.5:1 floor', async () => {
  const css = await readFile('app/globals.css', 'utf8');
  const luminance = hex => {
    const channels = hex.match(/[0-9a-f]{2}/g).map(x => parseInt(x, 16) / 255).map(x => x <= .04045 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4);
    return channels[0] * .2126 + channels[1] * .7152 + channels[2] * .0722;
  };
  for (const block of [css.split('@media')[0], css.split('@media (prefers-color-scheme: dark)')[1].split('* {')[0]]) {
    const tokens = Object.fromEntries([...block.matchAll(/--([a-z]+): (#[0-9a-f]{6})/g)].map(m => [m[1], m[2]]));
    for (const background of ['background', 'surface', 'panel']) {
    for (const key of ['foreground', 'muted', 'accent', 'visited']) {
      const values = [luminance(tokens[key]), luminance(tokens[background])].sort((a, b) => a - b);
      const ratio = (values[1] + .05) / (values[0] + .05);
      assert.ok(ratio >= 4.5, key + ': ' + ratio);
      console.log(tokens[background], key, ratio.toFixed(3));
    }
    }
  }
  // Pair arithmetic is not browser, focus, reflow, spacing or WCAG verification.
});
