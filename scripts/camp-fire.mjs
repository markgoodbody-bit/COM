import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';

// One record supplies visible credit and the optional machine-readable source note.
export const CAMP_FIRE = {
  title: 'Camp Fire', artist: 'Winslow Homer', artist_dates: '1836–1910', date: '1880',
  medium: 'Oil on canvas', museum: 'The Metropolitan Museum of Art', accession: '27.181',
  credit: 'Gift of Josephine Pomeroy Hendrick, in the name of Henry Keney Pomeroy, 1927',
  object_url: 'https://www.metmuseum.org/art/collection/search/11112',
  image_url: 'https://images.metmuseum.org/CRDImages/ad/original/DT2829.jpg',
  rights: 'Public Domain; The Met Open Access (CC0)',
  rights_url: 'https://www.metmuseum.org/policies/image-resources',
  biography_url: 'https://www.metmuseum.org/essays/winslow-homer-1836-1910',
  biography_author: 'H. Barbara Weinberg', biography_date: '2004-10-01',
  local_image: '/art/camp-fire.jpg', width: 3801, height: 2368, bytes: 2350423,
  sha256: '7b02049468877e8e69b2faf183e7842ecb6577b08edc2a3f4a594d1bbeb577e1',
  transformation: 'None; original museum JPEG, displayed proportionally without cropping.',
  responsive_variants: [
    { local_image: '/art/camp-fire-720.jpg', width: 720, height: 449, bytes: 57147, sha256: '1790607240f010723618dd1e0aed49a3c806ac0bbf3fe4d8b5bde69450658577' },
    { local_image: '/art/camp-fire-1440.jpg', width: 1440, height: 897, bytes: 255138, sha256: 'ffaf089763a9f82319b72f18a6359f6efd1a1ef680cd917b7f135926a04bf9a1' },
  ],
  responsive_transformation: 'Downscaled from the pinned original with ImageMagick 6.9.11-60, auto-orient, metadata stripped, Lanczos resize; JPEG quality 85 (720w) and 86 (1440w). No crop or generative alteration.',
  alt: 'Two men beside a woodland campfire, one reclining beneath a branch shelter and one seated upright, with sparks rising above the flames.',
  inspected_on: '2026-09-08',
  boundary: 'Museum sources identify the artwork and artist, not endorsement of this project. Image rights do not change rights in TRACE, Mechanical Ethics or other site material.',
};

export async function copyCampFire(sourceRoot, outRoot) {
  const image = await readFile(path.join(sourceRoot, 'art/camp-fire.jpg'));
  if (image.length !== CAMP_FIRE.bytes || createHash('sha256').update(image).digest('hex') !== CAMP_FIRE.sha256) {
    throw Error('Camp Fire image changed: reacquire and review provenance before updating its identity');
  }
  await mkdir(path.join(outRoot, 'art'), { recursive: true });
  await writeFile(path.join(outRoot, 'art/camp-fire.jpg'), image);
  for (const variant of CAMP_FIRE.responsive_variants) {
    const relative = variant.local_image.replace(/^\//, '');
    const bytes = await readFile(path.join(sourceRoot, relative));
    if (bytes.length !== variant.bytes || createHash('sha256').update(bytes).digest('hex') !== variant.sha256) {
      throw Error('Camp Fire responsive image changed: ' + relative);
    }
    await writeFile(path.join(outRoot, relative), bytes);
  }
  await writeFile(path.join(outRoot, 'art/camp-fire.json'), JSON.stringify(CAMP_FIRE, null, 2) + '\n');
}
