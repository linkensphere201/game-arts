"""Convert three model-derived lid states with one transform and palette."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
OUT=ROOT/'pixel-rpg-demo/mosslight/model_chest';OUT.mkdir(exist_ok=True)
paths=['chest-752003.png','chest-half-762001.png','chest-open-762003.png']
reference=Image.open(ROOT/'pixel-rpg-demo/mosslight/model_review/chest.png').convert('RGBA')
a=np.asarray(reference);colors=sorted(set(map(tuple,a[a[:,:,3]>0,:3].tolist())))
palette=Image.new('P',(1,1));palette.putpalette([v for c in colors for v in c]+[0]*(768-len(colors)*3))
frames=[];records=[]
for name,path in zip(['closed','half','open'],paths):
    source=BASE/path;im=Image.open(source).convert('RGB');rgb=np.asarray(im).astype(int)
    white=(rgb.min(2)>233)&(rgb.max(2)-rgb.min(2)<28)
    # White is backdrop, including the narrow opening around support brackets.
    im=im.convert('RGBA');im.putalpha(Image.fromarray((~white*255).astype('uint8')))
    im=im.crop((72,36,440,412)).resize((50,51),Image.Resampling.LANCZOS)
    alpha=im.getchannel('A').point(lambda x:255 if x>=128 else 0)
    im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
    frame=Image.new('RGBA',(64,64));frame.alpha_composite(im,(7,9));frame.save(OUT/(name+'.png'))
    assert frame.getbbox()[3]==60 and set(np.unique(np.asarray(frame)[:,:,3]))=={0,255}
    frames.append(frame);records.append({'state':name,'source':path,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256((OUT/(name+'.png')).read_bytes()).hexdigest()})
for frame in frames[1:]:assert np.array_equal(np.asarray(frame)[39:],np.asarray(frames[0])[39:])
board=Image.new('RGB',(768,280),'#ded8c7');d=ImageDraw.Draw(board)
for i,frame in enumerate(frames):
    d.text((i*256+12,5),['Closed','Half','Open'][i],fill='#33352e');zoom=frame.resize((256,256),Image.Resampling.NEAREST);board.paste(zoom,(i*256,24),zoom)
board.save(BASE/'chest-motion-review.png')
preview=[frames[i].resize((256,256),Image.Resampling.NEAREST) for i in [0,1,2,2,1,0]]
preview[0].save(BASE/'chest-motion.gif',save_all=True,append_images=preview[1:],duration=[700,160,180,700,160,180],loop=0,disposal=2)
(BASE/'chest-motion.json').write_text(json.dumps({'frames':records,'cell':[64,64],'anchor':[32,60],'unchanged_body_rows':[39,63],'status':'three-pose opening study; art approval pending'},indent=2))
print('CHEST_EXPORT_OK: three poses, identical lower body, binary alpha, shared palette and anchor')
