import { readFileSync } from 'node:fs';
import { copyArtwork } from './artwork.mjs';

const responsive = JSON.parse(readFileSync(new URL('../public/art/camp-fire-responsive.json', import.meta.url), 'utf8'));

// One record supplies visible credit and the optional machine-readable source note.
export const CAMP_FIRE = {
  id: 'camp-fire',
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
  transformation: 'The original museum JPEG is retained unchanged. Display uses the separately recorded proportional viewing copies.',
  responsive,
  visible_credit: 'Camp Fire, 1880, by Winslow Homer. The Metropolitan Museum of Art. Public domain, Open Access.',
  artist_route: '/#winslow-homer',
  why_this_spoke_to_us: 'The fire offers a shared place, but the two people occupy it differently. That spoke to us as an invitation to begin together without assuming the same view. This is our reading, not a claim about Homer\u2019s intention.',
  interpretation_author: 'PSFH project, drafted by Codex',
  alt: 'Two men beside a woodland campfire, one reclining beneath a branch shelter and one seated upright, with sparks rising above the flames.',
  inspected_on: '2026-09-08',
  retrieved_on: '2026-09-08',
  boundary: 'Museum sources identify the artwork and artist, not endorsement of this project. Image rights do not change rights in TRACE, Mechanical Ethics or other site material.',
};

export async function copyCampFire(sourceRoot, outRoot) {
  await copyArtwork(sourceRoot, outRoot, CAMP_FIRE, 'camp-fire.json');
}
