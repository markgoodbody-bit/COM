import {readFile, writeFile} from 'node:fs/promises';
import path from 'node:path';

// Two editorial placements, not a classification of the works or their meaning.
// Canonical records and all viewing copies remain in the existing Works set.
export const ROOMS = [
  {page:'explore/index.html', key:'atkins', title:'Explore', work:'anna-atkins', bypass:'Go straight to the map', anchor:'reading-map'},
  {page:'explore/nodes/futures.html', key:'shen', title:'Reachable futures', work:'shen-zhou', bypass:'Go straight to the reading', anchor:'reading'},
];
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

export function addArtRoom(html, room, record, images) {
  if (html.includes('class="art-room')) throw Error('Art room already present');
  // Controlled static templates only: retain attributes instead of replacing
  // the reading renderer's body style or any pre-existing body class.
  const bodies = html.match(/<body\b[^>]*>/g) ?? [], mains = html.match(/<main\b[^>]*>/g) ?? [];
  if (bodies.length !== 1 || mains.length !== 1) throw Error('Expected one body/main reading template');
  const body = bodies[0], main = mains[0];
  const classes = [...body.matchAll(/\sclass=(['"])(.*?)\1/g)];
  if (classes.length > 1 || (/\sclass\s*=/.test(body) && classes.length !== 1) || /\sid\s*=/.test(main)) throw Error('Ambiguous reading template attributes');
  const wrappedBody = classes.length
    ? body.replace(classes[0][0], ' class=' + classes[0][1] + classes[0][2] + ' contextual-room' + classes[0][1])
    : body.replace(/>$/, ' class="contextual-room">');
  const variants = images[0].variants, largest = variants.at(-1);
  if (!variants.length || !record.alt || !record.credit || !record.rights) throw Error('Incomplete canonical work record');
  const srcset = variants.map(v => '/art/' + escape(v.file) + ' ' + v.width + 'w').join(', ');
  const mapAnchor = room.key === 'atkins' ? '#reading-map' : '/explore/#reading-map';
  const figure = `<figure><a class="room-image" href="/works/${room.work}/" aria-label="Read about ${escape(record.title)} by ${escape(record.creator)}"><img src="/art/${escape(largest.file)}" srcset="${srcset}" sizes="(max-width: 48rem) 100vw, 65vw" width="${largest.width}" height="${largest.height}" alt="${escape(record.alt)}" loading="eager" decoding="async"></a><figcaption><a href="/works/${room.work}/"><cite>${escape(record.title)}</cite></a> · ${escape(record.creator)}, ${escape(record.date)}</figcaption></figure>`;
  const entrance = `<a class="skip" href="#${room.anchor}">${room.bypass}</a><section class="art-room art-room-${room.key}" aria-label="${escape(room.title)} entrance"><div class="room-stage">${figure}</div><nav class="room-nav" aria-label="Bypass the artwork"><a href="#${room.anchor}">${room.bypass}</a><a href="/">Back to the opening</a></nav><div class="room-heading"><p>${escape(room.title)}</p><a href="#${room.anchor}">${room.key === 'atkins' ? 'Choose a reading' : 'Read the small account'} <span aria-hidden="true">↓</span></a></div><div class="room-credit"><p>${escape(record.institution)}. ${escape(record.credit)}. ${escape(record.rights)}. <a href="/works/${room.work}/">About the work, sources and viewing copies</a>.</p><p>This placement is our choice, not the artist's argument or an endorsement of this project. <a href="${mapAnchor}">Skip to the map</a>.</p></div></section>`;
  let result = html.replace(body, wrappedBody + entrance)
    .replace(main, main.replace(/>$/, ' id="reading">'));
  if (room.key === 'atkins') result = result.replace('<nav aria-label="Optional routes"', '<nav id="reading-map" aria-label="Optional routes"');
  return result;
}

export async function applyContextualArt(root, sourceRoot) {
  // The normal build verifies the full Works inventory before reaching here.
  for (const room of ROOMS) {
    const record = JSON.parse(await readFile(path.join(sourceRoot, 'art', room.key + '.json')));
    const images = JSON.parse(await readFile(path.join(sourceRoot, 'art', room.key + '-images.json')));
    const file = path.join(root, room.page);
    await writeFile(file, addArtRoom(await readFile(file, 'utf8'), room, record, images));
  }
}
