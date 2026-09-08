import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';

// A small byte-identity copier shared by accepted artworks, not an art taxonomy.
export async function copyArtwork(sourceRoot, outRoot, record, recordName) {
  const inputs = [record, ...record.responsive.variants];
  if (record.responsive.parent_sha256 !== record.sha256 ||
      record.responsive.parent_local_image !== record.local_image) throw Error('Art derivative parent mismatch');
  const pending = [];
  for (const item of inputs) {
    if (!/^\/art\/[a-z0-9-]+\.jpg$/.test(item.local_image)) throw Error('Unsupported artwork path');
    const bytes = await readFile(path.join(sourceRoot, item.local_image.slice(1)));
    if (bytes.length !== item.bytes || createHash('sha256').update(bytes).digest('hex') !== item.sha256) {
      throw Error('Artwork identity mismatch: ' + item.local_image);
    }
    pending.push([item.local_image.slice(1), bytes]);
  }
  if (!/^[a-z0-9-]+\.json$/.test(recordName)) throw Error('Unsupported artwork record path');
  await mkdir(path.join(outRoot, 'art'), { recursive: true });
  for (const [name, bytes] of pending) await writeFile(path.join(outRoot, name), bytes);
  await writeFile(path.join(outRoot, 'art', recordName), JSON.stringify(record, null, 2) + '\n');
}

export const artworkSrcSet = record => record.responsive.variants
  .map(item => `${item.local_image} ${item.width}w`).join(', ');

// Full-width hero in an 86rem border-box with clamped1rem/4vw/4rem side padding.
// Conservative at intermediate widths; browser selection is checked separately.
export const HOMER_SIZES = '(max-width: 25rem) calc(100vw - 2rem), (max-width: 86rem) 92vw, 78rem';
