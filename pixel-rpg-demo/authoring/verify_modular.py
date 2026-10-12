from pathlib import Path
import importlib.util,json
from PIL import Image
path=Path(__file__).with_name('build_modular_characters.py')
spec=importlib.util.spec_from_file_location('modular_art',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
fail=[]
def bounds(im,label):
 b=im.getbbox()
 if not b or b[0]<=0 or b[1]<=0 or b[2]>=48 or b[3]>=64:fail.append((label,b))
for r in m.SPEC['presets']:
 for action,clip in m.SPEC['animations'].items():
  im=Image.open(m.OUT/f"{r['id']}_{action}.png").convert('RGBA');n=clip['frames'];assert im.size==(48*n,512)
  for row,direction in enumerate(m.SPEC['directions']):
   cells=[im.crop((i*48,row*64,(i+1)*48,(row+1)*64)) for i in range(n)]
   for f,c in enumerate(cells):bounds(c,(r['id'],action,direction,f))
   unique=len({c.tobytes() for c in cells})
   if unique<(2 if action=='idle' else 6):fail.append(('duplicate poses',r['id'],action,direction,unique))
 for direction in m.SPEC['directions']:
  assert m.render(r,direction,2,'walk').tobytes()!=m.render(r,direction,2,'run').tobytes()
for category in ['hair','face','headgear','outfit','hair_color','cloth_color']:
 variants=[]
 for i in range(12):
  r=m.recipe(0,headgear=-1,species=0);r[category]=i
  variants.append(m.render(r).tobytes())
  for direction in m.SPEC['directions']:
   for f in range(8):bounds(m.render(r,direction,f,'run'),(category,i,direction,f))
 assert len(set(variants))==12,category
assert len({m.render(m.recipe(0,species=i)).tobytes() for i in range(5)})==5
assert 0<m.shadow().getchannel('A').getextrema()[1]<255
assert len({m.render(m.recipe(0,body_type=i)).tobytes() for i in range(5)})==5
for species in range(5):
 for body_type in range(5):
  for gear in range(12):
   r=m.recipe(0,species=species,body_type=body_type,headgear=gear)
   for direction in m.SPEC['directions']:
    for f in [1,3,5,7]:bounds(m.render(r,direction,f,'run'),('combined',species,body_type,gear,direction,f))
print('MODULAR_PIXEL_QA failures=',fail[:30], 'total=',len(fail))
assert not fail
