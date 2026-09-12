export const SITE_EDITION = '0.8.21';

// Editorial revision date, never a build-clock/checkout/linked-project freshness.
export function assertRevisionDate(manifest, history) {
  const match = history.match(/^### D\d+\r?\n\s*\r?\n(\d{1,2} [A-Za-z]+ \d{4}) —/m);
  if (!match) throw Error('Latest deliberate history date missing');
  const declared = new Date(match[1] + ' 00:00:00 UTC');
  if (!Number.isFinite(declared.getTime()) || manifest.updated !== declared.toISOString().slice(0,10)) {
    throw Error('Manifest updated must match latest deliberate history date');
  }
}
