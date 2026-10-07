/* Local SVG text layers and CPU composition. No generation service is called. */
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
// On Windows use compose-poster.ps1 to configure Fontconfig before Node starts.
const sharp = require('sharp');
const assert = require('node:assert/strict');
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const hash = b => crypto.createHash('sha256').update(b).digest('hex');

function svg(w, h, body) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${body}</svg>`;
}

async function compose(layoutFile, output, overrides = {}) {
  const started = performance.now();
  const layout = JSON.parse(await fs.readFile(layoutFile, 'utf8'));
  assert.equal(layout.schema_version, 1);
  const {width: w, height: h} = layout.canvas;
  assert(Number.isInteger(w) && Number.isInteger(h) && w > 0 && h > 0 && w <= 4096 && h <= 4096);
  assert(Array.isArray(layout.layers) && layout.layers.length > 0);
  const fontBuffer = await fs.readFile(layout.font.file);
  const boldBuffer = layout.font.boldFile ? await fs.readFile(layout.font.boldFile) : null;
  const backgroundPath = path.resolve(path.dirname(layoutFile), layout.background);
  const background = await fs.readFile(backgroundPath);
  const bm = await sharp(background).metadata();
  assert.equal(bm.format, 'png');
  assert.equal(bm.width, w, 'Background must match canvas: do not silently stretch');
  assert.equal(bm.height, h);
  const ids = new Set(layout.layers.map(l => l.id));
  assert.equal(ids.size, layout.layers.length, 'Duplicate layer IDs');
  for (const key of Object.keys(overrides)) assert(ids.has(key), `Unknown text layer: ${key}`);
  await fs.mkdir(path.join(output, 'layers'), {recursive: true});
  await fs.writeFile(path.join(output, 'background.png'), background);
  const rendered = [], bodies = [], layers = [];
  const widthCache = new Map();
  async function measure(text, size, weight) {
    if (!text) return 0;
    if (!text.trim()) return text.length * size * 0.35;
    const key = JSON.stringify([text, size, weight]);
    if (!widthCache.has(key)) {
      const image = sharp({text: {text: esc(text), font: `${layout.font.family} ${weight === 700 ? 'Bold ' : ''}${size}`,
        fontfile: weight === 700 && layout.font.boldFile ? layout.font.boldFile : layout.font.file, dpi: 72, rgba: true}});
      widthCache.set(key, (await image.metadata()).width);
    }
    return widthCache.get(key);
  }
  async function wrap(text, size, weight, maxWidth) {
    const lines = [];
    for (const paragraph of text.split('\n')) {
      let line = '';
      for (const {segment} of new Intl.Segmenter('zh', {granularity: 'grapheme'}).segment(paragraph)) {
        assert(await measure(segment, size, weight) <= maxWidth, 'Glyph exceeds line width');
        if (line && await measure(line + segment, size, weight) > maxWidth) {
          lines.push(line); line = segment;
        } else line += segment;
      }
      lines.push(line);
    }
    return lines;
  }
  for (const original of layout.layers) {
    const l = {...original, text: overrides[original.id] ?? original.text};
    assert(/^[a-z][a-z0-9_]*$/.test(l.id));
    assert(typeof l.text === 'string' && l.text.length > 0 && l.text.length <= 2000);
    for (const key of ['x','y','width','height','fontSize','minFontSize','lineHeight']) assert(Number.isFinite(l[key]));
    assert(l.x >= 0 && l.y >= 0 && l.width > 0 && l.height > 0 && l.x+l.width <= w && l.y+l.height <= h);
    assert(l.minFontSize > 0 && l.fontSize >= l.minFontSize && l.lineHeight >= l.fontSize);
    assert(/^#[0-9a-f]{6}$/i.test(l.fill));
    assert(l.weight === undefined || [400,700].includes(l.weight));
    const weight = l.weight || 400;
    let lines, size = l.fontSize, spacing;
    for (; size >= l.minFontSize; size--) {
      spacing = l.lineHeight * size / l.fontSize;
      lines = await wrap(l.text, size, weight, l.width);
      if (lines.length * spacing <= l.height) break;
    }
    assert(size >= l.minFontSize, `Text overflow in ${l.id}; enlarge box or shorten copy`);
    const body = `<g id="${l.id}"><text font-family="${esc(layout.font.family)}" font-size="${size}" font-weight="${weight}" fill="${l.fill}">` +
      lines.map((line,i) => `<tspan x="${l.x}" y="${l.y+size+i*spacing}">${esc(line)}</tspan>`).join('') + '</text></g>';
    const source = svg(w,h,body);
    const png = await sharp(Buffer.from(source)).png().toBuffer();
    const {data,info} = await sharp(png).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    let visible = 0;
    for (let y=0;y<h;y++) for(let x=0;x<w;x++) if(data[(y*w+x)*info.channels+3]) {
      visible++;
      assert(x>=l.x-1 && x<l.x+l.width+1 && y>=l.y-1 && y<l.y+l.height+1, `Rendered ink outside box: ${l.id}`);
    }
    assert(visible > 0 && visible < w*h, `Invalid transparent text layer: ${l.id}`);
    await fs.writeFile(path.join(output, 'layers', l.id+'.svg'),source);
    await fs.writeFile(path.join(output, 'layers', l.id+'.png'),png);
    rendered.push({input:png,left:0,top:0}); bodies.push(body);
    layers.push({...l, resolvedFontSize:size, lines, svgSha256:hash(Buffer.from(source)), pngSha256:hash(png)});
  }
  const poster = await sharp(background).composite(rendered).png().toBuffer();
  await fs.writeFile(path.join(output,'poster.png'),poster);
  const fullSVG = svg(w,h,`<image width="${w}" height="${h}" href="data:image/png;base64,${background.toString('base64')}"/>`+bodies.join(''));
  await fs.writeFile(path.join(output,'poster.svg'),fullSVG);
  const savedLayout = {...layout, background:'background.png', layers:layers.map(({svgSha256,pngSha256,...l})=>l)};
  await fs.writeFile(path.join(output,'layout.json'),JSON.stringify(savedLayout,null,2));
  assert.equal(hash(await fs.readFile(backgroundPath)),hash(background),'Source background was modified');
  const manifest = {schema_version:1,backgroundSha256:hash(background),fontFile:layout.font.file,
    fontSha256:hash(fontBuffer),boldFontSha256:boldBuffer ? hash(boldBuffer) : null,
    renderer:sharp.versions,elapsedSeconds:(performance.now()-started)/1000,
    canvas:layout.canvas,layers,posterSha256:hash(poster)};
  await fs.writeFile(path.join(output,'manifest.json'),JSON.stringify(manifest,null,2));
  return manifest;
}

module.exports = {compose};
if (require.main === module) {
  const [layout,output,id,text] = process.argv.slice(2);
  if (!layout || !output || (id && text === undefined)) {
    console.error('Usage: node tools/compose-poster.cjs layout.json output-directory [layer-id replacement-text]');
    process.exitCode=1;
  } else compose(path.resolve(layout),path.resolve(output),id ? {[id]:text} : {})
    .then(m=>console.log(JSON.stringify({output:path.resolve(output),seconds:m.elapsedSeconds,layers:m.layers.length})))
    .catch(e=>{console.error(e);process.exitCode=1;});
}
