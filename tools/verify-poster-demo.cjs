/* Regression checks for independent text edits and lossless layer composition. */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');
const {compose} = require('./compose-poster.cjs');
const root = path.resolve(__dirname,'..');
const base = path.join(root,'.local/poster-cover/svg-demo');
async function read(dir,file) {return fs.readFile(path.join(base,dir,file));}
async function rgba(buffer) {return sharp(buffer).ensureAlpha().raw().toBuffer();}
(async()=>{
  const a = JSON.parse(await read('v1','manifest.json'));
  const b = JSON.parse(await read('v2','manifest.json'));
  assert.equal(a.backgroundSha256,b.backgroundSha256);
  assert.deepEqual(await read('v1','background.png'),await read('v2','background.png'));
  let unchanged=0;
  for(const l of a.layers) {
    const other = b.layers.find(x=>x.id===l.id);
    if(l.id==='price') {assert.notEqual(l.pngSha256,other.pngSha256); continue;}
    assert.equal(l.pngSha256,other.pngSha256); assert.equal(l.svgSha256,other.svgSha256); unchanged++;
  }
  const oldImage=await rgba(await read('v1','poster.png')), newImage=await rgba(await read('v2','poster.png'));
  const oldPrice=await rgba(await read('v1','layers/price.png')), newPrice=await rgba(await read('v2','layers/price.png'));
  const background=await rgba(await read('v1','background.png'));
  const layerPixels=await Promise.all(a.layers.map(async l=>rgba(await read('v1','layers/'+l.id+'.png'))));
  let changed=0, preserved=0;
  for(let i=0;i<oldImage.length;i+=4) {
    const delta=!oldImage.subarray(i,i+4).equals(newImage.subarray(i,i+4));
    if(delta) {changed++; assert(oldPrice[i+3]||newPrice[i+3],'Non-price pixels changed');}
    if(layerPixels.every(p=>p[i+3]===0)) {
      assert(oldImage.subarray(i,i+4).equals(background.subarray(i,i+4)),'Background pixels changed'); preserved++;
    }
  }
  assert(changed>0 && preserved>0);
  const composite=await sharp(await read('v1','background.png')).composite(await Promise.all(a.layers.map(async l=>({input:await read('v1','layers/'+l.id+'.png'),left:0,top:0})))).png().toBuffer();
  assert.deepEqual(await rgba(composite),oldImage);
  const layout = path.join(root,'production/poster-demo/layout.json');
  const wrap = await compose(layout,path.join(base,'wrap-check'),{title:'把清爽的夏天装进杯里'});
  assert(wrap.layers.find(l=>l.id==='title').lines.length>1,'Automatic wrap was not exercised');
  await assert.rejects(()=>compose(layout,path.join(base,'overflow-check'),{title:'夏'.repeat(100)}),/overflow/);
  await sharp(await read('v2','poster.svg')).png().toFile(path.join(base,'v2','poster-svg-preview.png'));
  const report={passed:true,unchangedTextLayers:unchanged,changedPixels:changed,
    backgroundPixelsPreserved:preserved,checks:['source hash','non-price layer hashes','price-only pixel changes',
    'background pixel preservation','recomposition','automatic Chinese wrapping','overflow rejection','complete SVG raster export']};
  await fs.writeFile(path.join(base,'verification.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report));
})().catch(e=>{console.error(e);process.exitCode=1;});
