"""Build a labeled same-brief comparison; no generative image edits."""
from pathlib import Path
import json, statistics
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'production/pixel-rpg/animagine-comparison'
assets=[a for a in json.loads((ROOT/'pixel-rpg-demo/authoring/model-wave-01.json').read_text())['assets'] if a['category']=='character']
canvas=Image.new('RGB',(1600,1400),'#e7e2d6');d=ImageDraw.Draw(canvas)
records=[]
for i,a in enumerate(assets):
 ident=a['id'];x=(i%4)*400;y=(i//4)*350
 for j,(label,path) in enumerate([('DreamShaper a1',ROOT/f'production/pixel-rpg/model-wave-01/originals/{ident}-a1.png'),('Animagine Opt',OUT/(ident+'.png'))]):
  im=ImageOps.contain(Image.open(path).convert('RGB'),(192,300))
  canvas.paste(im,(x+j*200+(200-im.width)//2,y));d.text((x+j*200+5,y+305),label,fill='#222222')
 d.text((x+5,y+327),ident,fill='#222222')
 records.append(json.loads((OUT/(ident+'.json')).read_text()))
canvas.save(OUT/'dreamshaper-vs-animagine.png')
summary={'count':len(records),'all_success':all(r['state']=='success' for r in records),'first_seconds':records[0]['elapsed_seconds'],'warm_median_seconds':statistics.median(r['elapsed_seconds'] for r in records[1:]),'peak_device_vram_mib':max(r['peak_device_vram_mib'] for r in records),'total_generation_seconds':sum(r['elapsed_seconds'] for r in records),'note':'Device-wide VRAM. Same briefs/seeds, different prompt formatting, sampling settings and resolutions; original a1 provenance may include reference conditioning. Not an isolated model benchmark.'}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))
