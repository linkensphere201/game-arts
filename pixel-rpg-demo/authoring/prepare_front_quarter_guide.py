"""Owned front illustration rearranged into an SE layout for local model redrawing."""
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
src=Image.open(ROOT/'production/pixel-rpg/model-sprite-study/segmented-source.png').convert('RGBA')
# Remove disconnected extraction residue from the original front illustration.
rgba=np.asarray(src)
labels,_=ndimage.label(rgba[:,:,3]>128)
counts=np.bincount(labels.ravel());counts[0]=0
src.putalpha(Image.fromarray(((labels==counts.argmax())*255).astype('uint8')))
# Narrow the far half and lift it slightly to suggest the elevated front-quarter projection.
# This layout transform is not a claim that a 2D warp creates a finished new view.
yy,xx=np.mgrid[:768,:512].astype(float)
dx=xx-270
sx=256+np.where(dx<0,dx/.82,dx/.60)
sy=yy+np.clip(dx/8,-12,12)
rgba=np.asarray(src,dtype=float);rgba[:,:,:3]*=rgba[:,:,3:4]/255
sample=np.stack([ndimage.map_coordinates(rgba[:,:,c],[sy,sx],order=1,mode='constant') for c in range(4)],axis=2)
a=sample[:,:,3:4]/255
sample[:,:,:3]=np.divide(sample[:,:,:3],a,out=np.zeros_like(sample[:,:,:3]),where=a>0)
guide=Image.fromarray(np.clip(sample,0,255).astype('uint8'))
# Shift the face area toward the facing side, leaving the rear bob mass in place.
head=src.crop((170,95,350,248)).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
head=head.resize((151,153),Image.Resampling.LANCZOS)
guide.alpha_composite(head,(196,95))
guide.save(OUT/'rowan-SE-layout.png')
print('SE_LAYOUT_GUIDE_ONLY: model source pixels, projected far half; needs model redraw')
