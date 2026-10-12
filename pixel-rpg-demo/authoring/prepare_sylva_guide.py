"""Adapt the prior elf illustration into a constrained local-model identity guide."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01'
im=Image.open(BASE/'originals/ch_sylva-a1.png').convert('RGB');a=np.asarray(im).copy();rgb=a.astype(float);y,x=np.mgrid[:a.shape[0],:a.shape[1]]
hair=(rgb[:,:,1]>rgb[:,:,0]+12)&(rgb[:,:,2]>rgb[:,:,0]+10)&(rgb[:,:,1]>125)&((y<282)|((x<157)&(y<457))|((x>335)&(y<520)))
v=rgb[:,:,1];gold=np.stack([np.clip(v*1.05+22,0,255),np.clip(v*.88+10,0,255),np.clip(v*.53+8,0,255)],axis=2);a[hair]=gold[hair].astype('uint8');im=Image.fromarray(a);d=ImageDraw.Draw(im)
# Replace the thin spear-like held object with a short crystal staff layout.
d.polygon([(36,643),(120,490),(138,485),(99,563),(60,642)],fill='white')
d.line([(100,642),(167,336)],fill='#594331',width=11)
d.line([(102,635),(167,339)],fill='#9c7850',width=5)
d.polygon([(173,298),(190,327),(169,358),(149,331)],fill='#62b4a4',outline='#356b64',width=3)
im.save(BASE/'guided/sylva-layout.png')
