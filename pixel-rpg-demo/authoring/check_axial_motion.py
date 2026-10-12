"""Verify actual front/back exported cells and provenance, not perceptual animation quality."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--nw',action='store_true');parser.add_argument('--sw',action='store_true');args=parser.parse_args();assert not(args.nw and args.sw)
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'/('nw-motion' if args.nw else 'sw-motion' if args.sw else 'axial-motion')
m=json.loads((OUT/'manifest.json').read_text())
for source in m['sources'].values():
 assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256']
unique=set()
for name,digest in m['sheet_sha256'].items():
 path=OUT/(name+'.png');assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
 sheet=Image.open(path);assert sheet.mode=='RGBA' and sheet.size==(768,128)
 for i in range(8):
  cell=sheet.crop((i*96,0,(i+1)*96,128));box=cell.getbbox()
  assert box and 0<box[0]<box[2]<96 and 0<box[1]<box[3]<128,(name,i,box)
  assert set(np.unique(np.asarray(cell.getchannel('A'))))=={0,255}
  h=hashlib.sha256(cell.tobytes()).hexdigest();assert h not in unique,(name,i,'duplicate');unique.add(h)
assert set(m['directions'])==({'NW'} if args.nw else {'SW'} if args.sw else {'S','SE','NE','N'})
assert len(unique)==16*len(m['directions'])
for direction in m['directions']:
 for action in ['walk','run']:
  poses=[p for p in m['poses'] if p['direction']==direction and p['action']==action]
  assert len(poses)==8
  assert any(p['legs'][0]['lift']>0 for p in poses) and any(p['legs'][1]['lift']>0 for p in poses)
  for p in poses:
   assert not(p['legs'][0]['swing'] and p['legs'][1]['swing'])
  assert any(p['legs'][0]['flight']>0 for p in poses)==(action=='run')
print('PROJECTED_EXPORT_QA_OK:',len(unique),'unique bounded RGBA cells, source/sheet hashes, alternating recovery and run flight')

# Check non-collinear projected joints, not only the requested bend parameter.
for direction in (['NW'] if args.nw else ['SW'] if args.sw else ['S','SE','NE']):
 angles={}
 for action in ['walk','run']:
  values=[]
  for pose in m['poses']:
   if pose['direction']!=direction or pose['action']!=action:continue
   assert len(pose['arms'])==(1 if direction in ['NE','NW'] else 2)
   for arm in pose['arms']:
    shoulder,elbow,wrist=[np.array(arm[k]) for k in ['shoulder','elbow','wrist']]
    u=elbow-shoulder;v=wrist-elbow
    assert np.isfinite([*u,*v]).all() and np.linalg.norm(u)>15 and np.linalg.norm(v)>15
    values.append(float(np.degrees(np.arccos(np.clip(np.dot(u,v)/(np.linalg.norm(u)*np.linalg.norm(v)),-1,1)))))
  angles[action]=np.mean(values)
 assert angles['run']>angles['walk']+3,(direction,angles)
print('PROJECTED_ELBOW_QA_OK: finite articulated joints; run bends exceed walk')
