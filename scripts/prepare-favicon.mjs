// One-time asset preparation using the already-installed Lucide/Sharp packages.
// Normal site builds copy the checked-in assets and do not invoke this script.
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Flame} from 'lucide-react';
import sharp from 'sharp';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';

const root = new URL('../', import.meta.url);
const license = (await readFile(new URL('../node_modules/lucide-react/LICENSE', import.meta.url), 'utf8')).split('\n---')[0].trim();
const glyph = renderToStaticMarkup(React.createElement(Flame, {size:24, fill:'#f4b544', stroke:'#f4b544', strokeWidth:1}));
const paths = glyph.slice(glyph.indexOf('>') + 1, glyph.lastIndexOf('</svg>'));
const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">\n<!-- Lucide Flame, lucide-react 1.31.0. ISC license: favicon-LICENSE.txt -->\n<rect width="24" height="24" rx="5" fill="#223235"/>\n<g fill="#f4b544" stroke="#f4b544" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">' + paths + '</g>\n</svg>\n';
await writeFile(new URL('public/favicon.svg', root), svg);
await writeFile(new URL('public/favicon-LICENSE.txt', root), 'PSFH browser-tab icon only. Not a licence for other site material.\n\nFlame geometry: Lucide Flame, lucide-react 1.31.0, https://lucide.dev\nPSFH adaptation: amber fill, dark rounded background.\n\n' + license + '\n');
const sizes = [16, 32, 48];
const images = await Promise.all(sizes.map(size => sharp(Buffer.from(svg)).resize(size,size).png().toBuffer()));
const header = Buffer.alloc(6 + 16 * sizes.length);
header.writeUInt16LE(1,2); header.writeUInt16LE(sizes.length,4);
let offset = header.length;
images.forEach((image,i) => {
  const p = 6 + i*16;
  header[p] = header[p+1] = sizes[i];
  header.writeUInt16LE(1,p+4); header.writeUInt16LE(32,p+6);
  header.writeUInt32LE(image.length,p+8); header.writeUInt32LE(offset,p+12);
  offset += image.length;
});
await writeFile(new URL('public/favicon.ico',root), Buffer.concat([header,...images]));
await mkdir(new URL('outputs/',root),{recursive:true});
await writeFile(new URL('outputs/favicon-32.png',root),images[1]);
console.log('Renderer:',JSON.stringify(sharp.versions));
for (const name of ['favicon.svg','favicon.ico','favicon-LICENSE.txt']) {
  const bytes = await readFile(new URL('public/'+name,root));
  console.log(name,bytes.length,createHash('sha256').update(bytes).digest('hex'));
}
