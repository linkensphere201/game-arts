"""Verify isolated calibrated trajectories in final pixel space; not art acceptance."""
from pathlib import Path
import argparse,hashlib,json,re
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
controller=(ROOT/'pixel-rpg-demo/mosslight/model_character.gd').read_text()
match=re.search(r'velocity = input\*\(([\d.]+) if running else ([\d.]+)\)',controller)
assert match
speeds={'run':float(match[1]),'walk':float(match[2])}
parser=argparse.ArgumentParser();parser.add_argument('--bounded',action='store_true');args=parser.parse_args()
seen=set();count=0;worst=0.;maximum_stretch=0.;minimum_ratio=1.
prefix='bounded' if args.bounded else 'calibrated'
for folder in (prefix+'-axial',prefix+'-nw',prefix+'-sw'):
    out=BASE/folder;m=json.loads((out/'manifest.json').read_text());assert m['runtime_stride']
    for source in m['sources'].values():
        assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256']
    for direction in m['directions']:
        seen.add(direction);p=m['projection'][direction]
        def screen(sole):
            sy=p['source_y'];ty=p['target_y'];y=sole[1]
            j=int(np.clip(np.searchsorted(sy,y)-1,0,len(sy)-2))
            return np.array([sole[0]*p['horizontal_scale'],ty[j]+(y-sy[j])*(ty[j+1]-ty[j])/(sy[j+1]-sy[j])])
        forward=np.array(p['forward']);assert abs(np.linalg.norm(forward)-1)<1e-9
        for action in ('walk','run'):
            dt=1/m['calibrated_fps'][action]
            poses=[q for q in m['poses'] if q['direction']==direction and q['action']==action]
            for pose in poses:
                im=Image.open(out/f'{direction}-{action}-{pose["frame"]}-source.png');box=im.getbbox()
                assert box and 0<box[0]<box[2]<im.width and 0<box[1]<box[3]<im.height,'Clipped raw pose'
                if args.bounded:
                    for leg in pose['legs']:
                        h,k,a=[np.array(leg[n]) for n in ('hip','knee','ankle')]
                        assert np.isfinite([*h,*k,*a]).all() and a[1]>h[1]
                        maximum_stretch=max(maximum_stretch,*leg['segment_ratios'])
                        minimum_ratio=min(minimum_ratio,*leg['segment_ratios'])
                        assert max(leg['segment_ratios'])<1.04,'Excessive elongation'
            for leg in range(2):
                for a,b in zip(poses,poses[1:]):
                    la,lb=a['legs'][leg],b['legs'][leg]
                    if la['swing'] or lb['swing'] or la['flight']>1e-6 or lb['flight']>1e-6:continue
                    wa=forward*speeds[action]*dt*a['frame']+screen(la['sole'])
                    wb=forward*speeds[action]*dt*b['frame']+screen(lb['sole'])
                    error=float(np.linalg.norm(wb-wa));worst=max(worst,error);count+=1
                    assert error<1e-6,(direction,action,a['frame'],error)
assert seen=={'S','N','SE','NE','SW','NW'} and count>=60
print(f'PROJECTED_GAIT_OK: six headings, {count} grounded intervals, max XY error {worst:.8f}px; isolated trials only')
if args.bounded:print(f'PROJECTED_LENGTH_OK: maximum ratio {maximum_stretch:.4f}; minimum projected ratio {minimum_ratio:.4f}; foreshortening still needs visual review')
