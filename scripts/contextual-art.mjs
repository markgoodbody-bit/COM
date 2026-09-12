import {readFile, writeFile} from 'node:fs/promises';
import path from 'node:path';

// Editorial placements, not a classification of the works or their meaning.
// Canonical records and all viewing copies remain in the existing Works set.
export const ROOMS = [
  {page:'explore/index.html', key:'atkins', title:'Explore', work:'anna-atkins', bypass:'Go straight to the map', anchor:'reading-map', mode:'legacy', record:'atkins', images:'atkins-images'},
  {page:'explore/nodes/futures.html', key:'shen', title:'Reachable futures', work:'shen-zhou', bypass:'Go straight to the reading', anchor:'reading', mode:'legacy', record:'shen', images:'shen-images'},
  {page:'explore/nodes/aperture.html', key:'vermeer', title:'Partial views', work:'johannes-vermeer', bypass:'Go straight to the reading', anchor:'reading', mode:'direct', record:'vermeer'},
  {page:'explore/nodes/significance.html', key:'powers', title:'Significance', work:'harriet-powers', bypass:'Go straight to the reading', anchor:'reading', mode:'responsive', record:'harriet-powers', images:'harriet-powers-responsive'},
  {page:'explore/nodes/hardening.html', key:'lewis', title:'Hardening', work:'edmonia-lewis', bypass:'Go straight to the reading', anchor:'reading', mode:'views', record:'lewis', images:'lewis-images'},
];
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const decodeAttr = value => String(value).replaceAll('&#x27;', "'").replaceAll('&#39;', "'").replaceAll('&quot;', '"').replaceAll('&amp;', '&');

function firstWorkAlt(html) {
  const matches = [...String(html).matchAll(/<img\b[^>]*\balt="([^"]+)"/g)];
  if (matches.length < 1) throw Error('Canonical Works page has no image alt');
  return decodeAttr(matches[0][1]);
}

function variantFigure(room, variants, alt, label = null, pair = false) {
  if (!Array.isArray(variants) || !variants.length || !alt) throw Error('Incomplete contextual-art image presentation');
  const largest = variants.at(-1);
  if (!largest?.file || !largest?.width || !largest?.height) throw Error('Incomplete contextual-art image variant');
  const srcset = variants.length > 1 ? ` srcset="${variants.map(v => '/art/' + escape(v.file) + ' ' + v.width + 'w').join(', ')}"` : '';
  const sizes = pair ? '(max-width: 48rem) 100vw, 50vw' : '(max-width: 48rem) 100vw, 65vw';
  const caption = label
    ? `<figcaption>${escape(label)}</figcaption>`
    : `<figcaption><a href="/works/${room.work}/"><cite>${escape(room.recordTitle)}</cite></a> · ${escape(room.recordCreator)}, ${escape(room.recordDate)}</figcaption>`;
  return `<figure><a class="room-image" href="/works/${room.work}/" aria-label="Read about ${escape(room.recordTitle)} by ${escape(room.recordCreator)}"><img src="/art/${escape(largest.file)}"${srcset} sizes="${sizes}" width="${largest.width}" height="${largest.height}" alt="${escape(alt)}" loading="eager" decoding="async"></a>${caption}</figure>`;
}

function legacyPresentation(room, record, images) {
  const variants = images[0].variants, largest = variants.at(-1);
  if (!variants.length || !record.alt || !record.credit || !record.rights) throw Error('Incomplete canonical work record');
  const srcset = variants.map(v => '/art/' + escape(v.file) + ' ' + v.width + 'w').join(', ');
  const figure = `<figure><a class="room-image" href="/works/${room.work}/" aria-label="Read about ${escape(record.title)} by ${escape(record.creator)}"><img src="/art/${escape(largest.file)}" srcset="${srcset}" sizes="(max-width: 48rem) 100vw, 65vw" width="${largest.width}" height="${largest.height}" alt="${escape(record.alt)}" loading="eager" decoding="async"></a><figcaption><a href="/works/${room.work}/"><cite>${escape(record.title)}</cite></a> · ${escape(record.creator)}, ${escape(record.date)}</figcaption></figure>`;
  return {stage: figure, stageClass:'room-stage', stageStyle:'', credit:`${record.institution}. ${record.credit}. ${record.rights}.`};
}

function contextualPresentation(room, record, images, workHtml) {
  const describedRoom = {...room, recordTitle:record.title, recordCreator:record.creator, recordDate:record.date};
  if (!record.title || !record.creator || !record.date || !record.institution) throw Error('Incomplete contextual-art work record');

  let figures;
  if (room.mode === 'direct') {
    const file = String(record.file ?? '').replace(/^\/art\//, '');
    if (!file || !record.width || !record.height) throw Error('Incomplete direct contextual-art image');
    figures = [variantFigure(describedRoom, [{file, width:record.width, height:record.height}], firstWorkAlt(workHtml))];
  } else if (room.mode === 'responsive') {
    if (!images?.variants) throw Error('Missing responsive contextual-art record');
    figures = [variantFigure(describedRoom, images.variants, firstWorkAlt(workHtml))];
  } else if (room.mode === 'views') {
    if (!Array.isArray(images) || images.length < 2 || !Array.isArray(record.alts) || record.alts.length !== images.length) throw Error('Incomplete multi-view contextual-art record');
    figures = images.map((view, index) => {
      const label = `Museum view ${index + 1}${view.source?.view_id ? ' · ' + view.source.view_id : ''}`;
      return variantFigure(describedRoom, view.variants, record.alts[index], label, true);
    });
  } else {
    throw Error('Unknown contextual-art presentation mode');
  }

  const rights = typeof record.rights === 'string' ? record.rights : (record.rights?.designation ?? record.rights?.label ?? '');
  let credit = record.visible_credit || [record.institution, record.credit, rights].filter(Boolean).join('. ') + '.';
  if (record.visible_credit && rights && !record.visible_credit.includes(rights)) credit += ` ${rights}.`;
  const paired = figures.length > 1;
  return {
    stage:figures.join(''),
    stageClass:paired ? 'room-stage room-stage-pair' : 'room-stage',
    // Auto-fit preserves Lewis's canonical two-view presentation on wide screens
    // and stacks the two independent museum photographs on narrow ones.
    stageStyle:paired ? 'display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,28rem),1fr));gap:1px;align-items:start' : '',
    credit,
  };
}

export function addArtRoom(html, room, record, images, workHtml = '') {
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
  const presentation = room.mode === 'legacy' ? legacyPresentation(room, record, images) : contextualPresentation(room, record, images, workHtml);
  const mapAnchor = room.key === 'atkins' ? '#reading-map' : '/explore/#reading-map';
  const stageStyle = presentation.stageStyle ? ` style="${presentation.stageStyle}"` : '';
  const entrance = `<a class="skip" href="#${room.anchor}">${room.bypass}</a><section class="art-room art-room-${room.key}" aria-label="${escape(room.title)} entrance"><div class="${presentation.stageClass}"${stageStyle}>${presentation.stage}</div><nav class="room-nav" aria-label="Bypass the artwork"><a href="#${room.anchor}">${room.bypass}</a><a href="/">Back to the opening</a></nav><div class="room-heading"><p>${escape(room.title)}</p><a href="#${room.anchor}">${room.key === 'atkins' ? 'Choose a reading' : 'Read the small account'} <span aria-hidden="true">↓</span></a></div><div class="room-credit"><p>${escape(presentation.credit)} <a href="/works/${room.work}/">About the work, sources and viewing copies</a>.</p><p>This placement is our choice, not the artist's argument or an endorsement of this project. <a href="${mapAnchor}">Skip to the map</a>.</p></div></section>`;
  let result = html.replace(body, wrappedBody + entrance)
    .replace(main, main.replace(/>$/, ' id="reading">'));
  if (room.key === 'atkins') result = result.replace('<nav aria-label="Optional routes"', '<nav id="reading-map" aria-label="Optional routes"');
  return result;
}

export async function applyContextualArt(root, sourceRoot) {
  // The normal build verifies the full Works inventory before reaching here.
  for (const room of ROOMS) {
    const record = JSON.parse(await readFile(path.join(sourceRoot, 'art', room.record + '.json')));
    const images = room.images ? JSON.parse(await readFile(path.join(sourceRoot, 'art', room.images + '.json'))) : null;
    const workHtml = room.mode === 'legacy' ? '' : await readFile(path.join(sourceRoot, 'works', room.work, 'index.html'), 'utf8');
    const file = path.join(root, room.page);
    await writeFile(file, addArtRoom(await readFile(file, 'utf8'), room, record, images, workHtml));
  }
}
