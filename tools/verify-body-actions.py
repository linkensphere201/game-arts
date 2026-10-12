"""Check baked action intent and contact markers; not an artistic-quality test."""
import json,math,sys
from pathlib import Path
out=Path(sys.argv[1]);data=json.loads((out/'actions.json').read_text());results={}
distance=lambda a,b:math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
for clip in data['clips']:
    samples=clip['samples'];name=clip['name']
    error=max(distance(s['actual_feet'][side],s['targets'][side]) for s in samples for side in ['l','r'])
    assert error<.0001,(name,error)
    assert max(s['reach_error'] for s in samples)<.0001,name
    metrics={'max_ankle_target_error_m':error,'duration':clip['duration']}
    if name=='Idle':
        movement=max(distance(s['actual_feet'][side],samples[0]['actual_feet'][side]) for s in samples for side in ['l','r'])
        assert movement<.0001,movement
        assert max(s['breath'] for s in samples)>.99
        metrics['foot_drift_m']=movement
    if clip['loop']:
        assert max(distance(samples[0]['actual_feet'][side],samples[-1]['actual_feet'][side]) for side in ['l','r'])<.0001,name
    if name in ['Walk','Run']:
        drifts=[]
        for side in ['l','r']:
            previous=None
            for sample in samples:
                if not sample['contact'][side]:previous=None;continue
                p=list(sample['actual_feet'][side]);p[1]-=sample['speed']*(sample['frame']-1)/data['fps']
                # Exclude periodic replant discontinuity at clip endpoint.
                if previous and distance(p,previous)<.1:drifts.append(distance(p,previous))
                previous=p
        assert max(drifts,default=0)<.0001,(name,max(drifts))
        metrics['max_adjacent_stance_marker_drift_m']=max(drifts,default=0)
        metrics['travel_speed_m_s']=samples[0]['speed']
    if name.startswith('Turn'):
        assert abs(abs(samples[-1]['yaw'])-math.pi/2)<1e-6
        metrics['turn_degrees']=math.degrees(samples[-1]['yaw'])
    if name=='Jump':
        peak=max(s['root'][2] for s in samples)
        assert peak>.3 and abs(samples[-1]['root'][2])<1e-6
        metrics['root_jump_height_m']=peak
    if name.startswith('Hit'):
        steps=0
        for side in ['l','r']:
            contact=True
            for sample in samples:
                now=sample['contact'][side]
                if contact and not now:steps+=1
                contact=now
        assert steps==(5 if name=='HitHeavy' else 1),(name,steps)
        metrics['step_lifts']=steps;metrics['root_retreat_m']=samples[-1]['root'][1]
    results[name]=metrics
(out/'motion-verification.json').write_text(json.dumps(results,indent=2),encoding='utf8')
print('BODY_ACTION_INTENT_OK',json.dumps(results))
