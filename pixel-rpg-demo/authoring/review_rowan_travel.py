"""Package actual Godot captures and quantify held-frame stance drift."""
from pathlib import Path
import json
import argparse
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
parser=argparse.ArgumentParser()
parser.add_argument('--weight',action='store_true')
parser.add_argument('--phased-arms',action='store_true')
args=parser.parse_args()
OUT=BASE/('weight-cycle/travel' if args.weight else 'support-cycle/travel')
if args.phased_arms:OUT=BASE/'phased-cycle/travel'
samples=json.loads((OUT/'samples.json').read_text())
assert len(samples)==64
frames=[Image.open(OUT/f'frame-{i:03d}.png').convert('RGB') for i in range(64)]
assert all(frame.size==(640,600) for frame in frames)
# GIF centiseconds: alternate 10/20ms durations while preserving total 1000ms.
durations=[round((i+1)*100/64)*10-round(i*100/64)*10 for i in range(64)]
frames[0].save(OUT/'comparison.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
board=Image.new('RGB',(1280,1200))
for slot,index in enumerate((0,12,24,31)):
    board.paste(frames[index],((slot%2)*640,(slot//2)*600))
board.save(OUT/'comparison.png')
poses=json.loads((BASE/'support-cycle/manifest.json').read_text())['frames']
traces=[]
for sample in samples:
    frame=sample['support_frame']
    pose=poses[frame]
    traces.append(dict(time=sample['time'],frame=frame,leg=pose['support'],
                       world_sole_y=sample['world_y']+pose['sole_y']))
spans=[]
for start in (0,16,32,48):
    values=[t['world_sole_y'] for t in traces[start:start+16]]
    spans.append(max(values)-min(values))
assert max(spans)>3, 'A discrete held frame must not be reported as continuous foot lock'
result=dict(traces=traces,stance_world_y_span=spans,
            status='sampled lock does not cancel within-frame sliding',
            observation='16 fps support sprite is held while actor moves at 65 px/s; a 64 Hz sample shows over 3 px drift per stance window',
            next_step='evaluate stance-relative pose timing and authored weight transfer; do not declare current walk accepted')
(OUT/'stance-review.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('TRAVEL_REVIEW_OK: actual captures packaged; stance spans',spans)
