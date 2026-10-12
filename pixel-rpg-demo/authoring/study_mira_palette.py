"""Non-destructive shared-palette study for three Mira directions."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
OUT=ROOT/'pixel-rpg-demo/mosslight/model_review'
ids=['mira','mira-back','mira-side']
images=[Image.open(OUT/(name+'.png')).convert('RGBA') for name in ids]
arrays=[np.asarray(im) for im in images]
visible=np.concatenate([a[a[:,:,3]>0,:3] for a in arrays])
allowed=np.unique(visible,axis=0)
strip=Image.fromarray(visible.reshape(1,-1,3))
records=[]
for budget in (24,40):
    quant=strip.quantize(colors=budget,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    centers=np.array(quant.getpalette()[:budget*3]).reshape(-1,3)
    distance=((centers[:,None,:].astype(float)-allowed[None,:,:])**2).sum(2)
    colors=np.unique(allowed[distance.argmin(1)],axis=0)
    palette=Image.new('P',(1,1));flat=colors.ravel().tolist()
    # Repeat a real swatch in unused entries rather than introducing black.
    palette.putpalette(flat+colors[0].tolist()*(256-len(colors)))
    board=Image.new('RGB',(660,690),'#ded8c7');draw=ImageDraw.Draw(board)
    outputs=[]
    for index,(name,im,a) in enumerate(zip(ids,images,arrays)):
        candidate=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
        candidate.putalpha(im.getchannel('A'));b=np.asarray(candidate)
        assert np.array_equal(a[:,:,3],b[:,:,3]) and candidate.getbbox()==im.getbbox()
        assert len(np.unique(b[b[:,:,3]>0,:3],axis=0))<=budget
        dest=OUT/f'{name}-palette-{budget}.png';candidate.save(dest)
        draw.text((index*220+12,10),f'{name}: original',fill='#33352e')
        draw.text((index*220+12,350),f'shared {len(colors)} colors',fill='#33352e')
        for row,cell in enumerate((im,candidate)):
            zoom=cell.resize((192,288),Image.Resampling.NEAREST);board.paste(zoom,(index*220+14,40+row*340),zoom)
        outputs.append({'id':name,'source_sha256':hashlib.sha256((OUT/(name+'.png')).read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'original_colors':len(np.unique(a[a[:,:,3]>0,:3],axis=0))})
    board.save(BASE/f'mira-palette-{budget}-comparison.png')
    records.append({'budget':budget,'colors':colors.tolist(),'outputs':outputs})
(BASE/'mira-palette-study.json').write_text(json.dumps({'status':'comparison only; not promoted','alpha_and_bounds':'unchanged','records':records},indent=2),encoding='utf-8')
print('MIRA_PALETTE_STUDY_OK: shared ramps, preserved alpha and bounds; no production replacement')
