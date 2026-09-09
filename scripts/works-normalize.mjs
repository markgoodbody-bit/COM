import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';

const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const requireValue = (ok, message) => { if (!ok) throw new Error(message); };

const routes = [
  'works/index.html',
  'works/harriet-powers/index.html',
  'works/johannes-vermeer/index.html',
  'works/anna-atkins/index.html',
  'works/shen-zhou/index.html',
  'works/edmonia-lewis/index.html',
];

function normalize(route, html) {
  const before = html;
  html = html
    .replace(/\s*<meta name="robots" content="noindex,nofollow">/g, '')
    .replace(/\s*<meta name="robots" content="noindex">/g, '')
    .replaceAll('Unpublished work-page proposal', 'Works')
    .replaceAll('Unpublished work-page preview', 'Works')
    .replaceAll(' · Unpublished preview', '')
    .replaceAll('Please Start From Here · Unpublished collection preview', 'Please Start From Here')
    .replaceAll('This is a local review collection, not a published edition. The works are not endorsements of this project.', 'These works and their makers are not endorsements of this project.');

  requireValue(!/\bUnpublished\b/.test(html), `Proposal-state label remains in ${route}`);
  requireValue(!/<meta name="robots" content="noindex/.test(html), `Proposal noindex remains in ${route}`);
  requireValue(html.includes('Please Start From Here'), `Site identity lost in ${route}`);
  requireValue(!/<(?:script|form|iframe)\b/i.test(html), `Active content introduced in ${route}`);

  if (route === 'works/index.html') {
    requireValue(html.includes('Five works selected for this preview.'), 'Shelf count/selection wording lost');
    requireValue(html.includes('not a ranking or representative canon'), 'Shelf selection aperture ceiling lost');
    requireValue(html.includes('These works and their makers are not endorsements of this project.'), 'Shelf endorsement boundary lost');
  }
  if (route.endsWith('harriet-powers/index.html')) {
    requireValue(html.includes("The maker's recorded account") && html.includes('Our response · PSFH'), 'Powers maker/project separation lost');
    requireValue(html.indexOf("The maker's recorded account") < html.indexOf('Our response · PSFH'), 'Powers maker account no longer precedes project response');
  }
  if (route.endsWith('johannes-vermeer/index.html')) {
    requireValue(!html.includes('Our response · PSFH'), 'Vermeer project response introduced');
    requireValue(html.includes('tier acquired for this preview, not a limit on what the museum offers'), 'Vermeer source-tier disclosure lost');
  }
  requireValue(before !== html, `Expected proposal wrapper normalization did not occur for ${route}`);
  return html;
}

export async function normalizeWorks(outRoot) {
  const observations = {};
  for (const route of routes) {
    const file = path.join(outRoot, route);
    const beforeBytes = await readFile(file);
    const after = normalize(route, beforeBytes.toString('utf8'));
    const afterBytes = Buffer.from(after, 'utf8');
    await writeFile(file, afterBytes);
    observations[route] = {
      input_bytes: beforeBytes.length,
      input_sha256: sha(beforeBytes),
      output_bytes: afterBytes.length,
      output_sha256: sha(afterBytes),
    };
  }
  return observations;
}
