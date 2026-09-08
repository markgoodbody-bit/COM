import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, mkdtemp, mkdir, writeFile, rm, readdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { CAMP_FIRE } from './camp-fire.mjs';
import { copyArtwork } from './artwork.mjs';

test('art copier rejects a wrong parent or a corrupted derivative before publication', async () => {
  const temp = await mkdtemp(path.join(tmpdir(), 'psfh-art-fixture-'));
  const source = path.join(temp, 'input'), output = path.join(temp, 'output');
  try {
    await mkdir(path.join(source, 'art'), { recursive: true });
    await mkdir(output);
    for (const item of [CAMP_FIRE, ...CAMP_FIRE.responsive.variants]) {
      await writeFile(path.join(source, item.local_image.slice(1)), await readFile('public' + item.local_image));
    }
    const wrongParent = structuredClone(CAMP_FIRE);
    wrongParent.responsive.parent_sha256 = '0'.repeat(64);
    await assert.rejects(copyArtwork(source, output, wrongParent, 'camp-fire.json'), /parent mismatch/);
    await writeFile(path.join(source, 'art/camp-fire-720.jpg'), 'not the accepted derivative');
    await assert.rejects(copyArtwork(source, output, CAMP_FIRE, 'camp-fire.json'), /identity mismatch/);
    assert.deepEqual(await readdir(output), []);
  } finally {
    // Only the newly created owned fixture may be removed; never any app path.
    assert.equal(path.dirname(temp), path.resolve(tmpdir()));
    assert.ok(path.basename(temp).startsWith('psfh-art-fixture-'));
    await rm(temp, { recursive: true });
  }
});
