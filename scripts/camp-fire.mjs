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
  await writeFile(path.join(outRoot, 'art/camp-fire.json'), JSON.stringify(CAMP_FIRE, null, 2) + '\n');
}
