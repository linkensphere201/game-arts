"""Report transition discontinuity proxies, never equate them with art approval."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
SPRITES=ROOT/'pixel-rpg-demo/mosslight/model_review'
SEQUENCES={
'abrupt':['neutral','left-half','left-arm','left-half','neutral','right-half','right-arm','right-half'],
'intermediate':['neutral','left-arm-half','left-arm','left-arm-half','neutral','right-arm-half','right-arm','right-arm-half']}
SEQUENCES['color_transfer']=[pose+'-stable' if 'arm' in pose else pose for pose in SEQUENCES['intermediate']]
report={}
for name,sequence in SEQUENCES.items():
    arrays=[np.asarray(Image.open(SPRITES/f'neris-walk-{pose}.png').convert('RGBA'))[43:92] for pose in sequence]
    changed=[int(np.any(a!=arrays[(i+1)%8],axis=2).sum()) for i,a in enumerate(arrays)]
    silhouette=[int((a[:,:,3]!=arrays[(i+1)%8][:,:,3]).sum()) for i,a in enumerate(arrays)]
    report[name]={'upper_body_changed_pixels_per_transition':changed,'max':max(changed),'mean':sum(changed)/8,'silhouette_change':silhouette,'silhouette_max':max(silhouette)}
report['scope']='Pixel-change proxy only; does not prove natural gait or visual acceptance.'
(OUT/'neris-arm-transition-metrics.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
