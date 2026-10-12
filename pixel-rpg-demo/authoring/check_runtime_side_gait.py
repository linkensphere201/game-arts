"""Check sampled stance world-X against actual controller speed and exported clip timing.

This verifies the horizontal contact trajectory, not sub-frame raster smoothness,
vertical contact/flight timing, collision response or diagonal foot locking.
"""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
runtime=json.loads((BASE/'unified-motion/manifest.json').read_text())
controller=(ROOT/'pixel-rpg-demo/mosslight/model_character.gd').read_text()
speed_match=re.search(r'velocity = input\*\(([\d.]+) if running else ([\d.]+)\)',controller)
assert speed_match,'Controller speed changed; adapt the gait check to its actual speed source'
speeds={'run':float(speed_match[1]),'walk':float(speed_match[2])}
worst=0.;count=0
for heading,folder,sign in [('E',BASE/'motion',1),('W',BASE/'left-motion/rig',-1)]:
    motion=json.loads((folder/'motion.json').read_text())
    scale=motion['runtime_calibration']['horizontal_scale']
    for action in ('walk','run'):
        clip=next(c for c in runtime['animations'] if c['name']==action+'_'+heading)
        dt=1/clip['fps'];assert clip['frames']==8
        poses=[p for p in motion['poses'] if p['action']==action]
        for leg in range(2):
            for a,b in zip(poses,poses[1:]):
                la,lb=a['legs'][leg],b['legs'][leg]
                if la['swing'] or lb['swing'] or la['lift']>1e-6 or lb['lift']>1e-6:continue
                # A fixed foot has the same world coordinate after the body advances.
                wa=sign*(a['frame']*dt*speeds[action]+la['ankle'][0]*scale)
                wb=sign*(b['frame']*dt*speeds[action]+lb['ankle'][0]*scale)
                residual=abs(wb-wa);worst=max(worst,residual);count+=1
                assert residual<1e-6,(heading,action,a['frame'],residual)
assert count>=16
print(f'SIDE_RUNTIME_GAIT_OK: {count} sampled grounded intervals, world-X residual {worst:.8f}px; E/W only')
