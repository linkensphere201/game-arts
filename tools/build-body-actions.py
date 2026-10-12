"""M5.2.9.6: audit and author the first white-body action set.

Blender -b -P tools/build-body-actions.py -- RIG_REVIEW_BLEND OUT
All motion is baked on the supplied deform rig; no runtime IK dependency.
"""
import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix

source,out=map(Path,sys.argv[sys.argv.index('--')+1:]);out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(source))
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
rig=bpy.data.objects['StandardBodyRig'];body=bpy.data.objects['Standard_adult_body'];scene=bpy.context.scene
rig.animation_data_clear()
for m in body.modifiers:
    if m.type=='ARMATURE':m.use_deform_preserve_volume=False
# Keep the deltoid cap supported by the clavicle when the humerus twists.
# This changes weights only on the copied authoring body, never its approved shape.
shoulder_adjustments=0
for side in ['l','r']:
    upper=body.vertex_groups['upperarm_'+side];clavicle=body.vertex_groups['clavicle_'+side]
    joint=rig.data.bones['upperarm_'+side].head_local
    for vertex in body.data.vertices:
        distance=(vertex.co-joint).length
        if distance>=.115:continue
        weight=next((g.weight for g in vertex.groups if g.group==upper.index),0)
        if weight<=0:continue
        transfer=weight*.85*(1-distance/.115)**2
        existing=next((g.weight for g in vertex.groups if g.group==clavicle.index),0)
        upper.add([vertex.index],weight-transfer,'REPLACE');clavicle.add([vertex.index],existing+transfer,'REPLACE')
        shoulder_adjustments+=1
deform={b.name for b in rig.data.bones if b.use_deform}
group_names={g.index:g.name for g in body.vertex_groups};bodygroup=body.vertex_groups['body'].index
visible=[v for v in body.data.vertices if any(g.group==bodygroup and g.weight>.5 for g in v.groups)]
weights=[sum(g.weight for g in v.groups if group_names[g.group] in deform) for v in visible]
symmetry=[]
for b in rig.data.bones:
    if b.name.endswith('_l'):
        r=rig.data.bones[b.name[:-2]+'_r'];mirror=Vector((-b.head_local.x,b.head_local.y,b.head_local.z))
        symmetry.append((mirror-r.head_local).length)
audit={'bones':len(rig.data.bones),'visible_vertices':len(visible),'unweighted':sum(w<1e-6 for w in weights),
       'weight_sum_range':[min(weights),max(weights)],'max_rest_symmetry_error_m':max(symmetry),
       'skin_mode':'linear, matching glTF/Godot','shoulder_weight_vertices_adjusted':shoulder_adjustments,
       'zero_length_bones':[b.name for b in rig.data.bones if b.length<1e-6]}
assert audit['bones']==53 and audit['unweighted']==0 and not audit['zero_length_bones'],audit
assert max(symmetry)<.015,audit
(out/'rig-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf8')
print('RIG_AUDIT_PASS',json.dumps(audit),flush=True)

FPS=30;scene.render.fps=FPS
def clamp(x,a=0,b=1):return max(a,min(b,x))
def smooth(x):x=clamp(x);return x*x*(3-2*x)
def envelope(t,points):
    for (a,x),(b,y) in zip(points,points[1:]):
        if t<=b:return x+(y-x)*smooth((t-a)/(b-a))
    return points[-1][1]
def reset():
    for p in rig.pose.bones:
        p.location=(0,0,0);p.rotation_mode='QUATERNION';p.rotation_quaternion=(1,0,0,0);p.scale=(1,1,1)
def rotate(name,axis,degrees,add=False):
    p=rig.pose.bones[name];q=Quaternion(p.bone.matrix_local.to_quaternion().inverted()@Vector(axis),math.radians(degrees))
    p.rotation_quaternion=q@p.rotation_quaternion if add else q
def move_world(name,delta):
    p=rig.pose.bones[name];p.location=p.bone.matrix_local.to_3x3().inverted()@Vector(delta)
def pose_matrix(name,head,direction,rootq):
    bone=rig.data.bones[name];restq=rootq@bone.matrix_local.to_quaternion()
    q=(restq@Vector((0,1,0))).rotation_difference(direction.normalized())@restq
    rig.pose.bones[name].matrix=Matrix.Translation(head)@q.to_matrix().to_4x4()
    bpy.context.view_layer.update()

ankles={s:rig.data.bones['foot_'+s].head_local.copy() for s in ['l','r']}
lengths={s:(rig.data.bones['thigh_'+s].length,rig.data.bones['calf_'+s].length) for s in ankles}
rootrest=rig.data.bones['Root'].head_local.copy()
arm_scales={s:(rig.data.bones['upperarm_'+s].length+rig.data.bones['lowerarm_'+s].length)/.45140553035690667 for s in ankles}
def solve_leg(side,ankle,rootq):
    hip=rig.pose.bones['thigh_'+side].head.copy();a,b=lengths[side]
    delta=ankle-hip;distance=delta.length;d=clamp(distance,abs(a-b)+1e-5,a+b-1e-5);axis=delta.normalized()
    along=(a*a-b*b+d*d)/(2*d);height=math.sqrt(max(0,a*a-along*along))
    forward=rootq@Vector((0,-1,0));bend=(forward-axis*forward.dot(axis)).normalized()
    knee=hip+axis*along+bend*height
    solved=hip+axis*d
    pose_matrix('thigh_'+side,hip,knee-hip,rootq)
    pose_matrix('calf_'+side,knee,solved-knee,rootq)
    q=rootq@rig.data.bones['foot_'+side].matrix_local.to_quaternion()
    rig.pose.bones['foot_'+side].matrix=Matrix.Translation(solved)@q.to_matrix().to_4x4()
    bpy.context.view_layer.update()
    return abs(distance-d)

def solve_arm(side,wrist,rootq):
    upper=rig.data.bones['upperarm_'+side];lower=rig.data.bones['lowerarm_'+side]
    shoulder=rig.pose.bones[upper.name].head.copy();delta=wrist-shoulder
    a,b=upper.length,lower.length;d=clamp(delta.length,abs(a-b)+1e-5,a+b-1e-5);axis=delta.normalized()
    along=(a*a-b*b+d*d)/(2*d);height=math.sqrt(max(0,a*a-along*along))
    preference=Vector((.3 if side=='l' else -.3,1,-.2))
    bend=(preference-axis*preference.dot(axis)).normalized()
    elbow=shoulder+axis*along+bend*height
    end=shoulder+axis*d
    rest_upper=(upper.tail_local-upper.head_local).normalized()
    rest_lower=(lower.tail_local-lower.head_local).normalized()
    rest_normal=rest_upper.cross(rest_lower).normalized()
    normal=(elbow-shoulder).cross(end-elbow).normalized()
    # Preserve the elbow's bend plane, not just each bone's longitudinal axis.
    # Independent shortest-arc rotations can introduce unwanted humeral twist.
    for bone,head,direction,rest_direction in [(upper,shoulder,elbow-shoulder,rest_upper),(lower,elbow,end-elbow,rest_lower)]:
        y=direction.normalized()
        desired=Matrix((normal,y,normal.cross(y))).transposed()
        rest=Matrix((rest_normal,rest_direction,rest_normal.cross(rest_direction))).transposed()
        q=(desired@rest.transposed()).to_quaternion()@bone.matrix_local.to_quaternion()
        rig.pose.bones[bone.name].matrix=Matrix.Translation(head)@q.to_matrix().to_4x4()
        bpy.context.view_layer.update()
    return abs(delta.length-d)

clips=[('Idle',3.2,True),('Walk',1.2,True),('TurnLeft',1.2,False),('TurnRight',1.2,False),
       ('Run',.8,True),('Jump',1.5,False),('AttackLeft',1.1,False),('AttackRight',1.1,False),
       ('HitLight',1.1,False),('HitHeavy',3.0,False)]
actions=[];manifest={'fps':FPS,'forward':'Blender -Y; Godot +Z','arm_target_scales':arm_scales,'clips':[]}

def motion(name,t,duration):
    reset();u=t/duration;root=Vector((0,0,0));yaw=0.;drop=-.025
    feet={s:Vector((ankles[s].x*.78,ankles[s].y,ankles[s].z)) for s in ankles}
    contact={s:True for s in ankles};speed=0.;breath=0.
    for s,sign in [('l',1),('r',-1)]:
        rotate('upperarm_'+s,(0,1,0),sign*32)
        rotate('lowerarm_'+s,(1,0,0),25)
    if name=='Idle':
        breath=(1-math.cos(2*math.pi*u))*.5
        rig.pose.bones['spine_03'].scale=(1+.009*breath,1+.003*breath,1+.009*breath)
        rotate('spine_02',(1,0,0),-.35*breath)
    elif name in ['Walk','Run']:
        run=name=='Run';duty=.4 if run else .6;stride=.54 if run else .42;lift=.16 if run else .065
        speed=stride/(duty*duration)
        drop=-.095 if run else -.040
        if run:drop+=.025*math.cos(4*math.pi*u)
        rotate('spine_02',(1,0,0),10 if run else 2)
        for s,phaseoffset in [('l',0),('r',.5)]:
            phase=(u+phaseoffset)%1
            if phase<duty:
                feet[s].y+=-stride/2+stride*phase/duty
            else:
                swing=(phase-duty)/(1-duty)
                feet[s].y+=stride/2-stride*smooth(swing)
                feet[s].z+=lift*math.sin(math.pi*swing)**1.5;contact[s]=False
            rotate('upperarm_'+s,(1,0,0),(28 if run else 16)*math.cos(2*math.pi*(u+phaseoffset)),True)
            rotate('lowerarm_'+s,(1,0,0),-48 if run else 10)
    elif name.startswith('Turn'):
        sign=1 if name=='TurnLeft' else -1;yaw=sign*math.pi/2*smooth(u)
        for s,lo,hi in [('l',.05,.48),('r',.50,.95)]:
            local=clamp((u-lo)/(hi-lo));angle=sign*math.pi/2*smooth(local)
            feet[s]=Quaternion((0,0,1),angle)@feet[s]
            feet[s].z+=.055*math.sin(math.pi*local);contact[s]=not(lo<u<hi)
    elif name=='Jump':
        crouch=envelope(u,[(0,0),(.18,1),(.3,0),(.72,0),(.83,.7),(1,0)])
        flight=clamp((u-.28)/.44);air=.34*4*flight*(1-flight)
        drop-=.13*crouch;root.z=air
        for s in feet:
            feet[s].z+=air+.055*math.sin(math.pi*flight)
            contact[s]=not(.28<u<.72)
            rotate('upperarm_'+s,(1,0,0),-60*math.sin(math.pi*flight)+25*crouch,True)
            rotate('lowerarm_'+s,(1,0,0),25-50*math.sin(math.pi*flight))
    elif name.startswith('Attack'):
        s='l' if name=='AttackLeft' else 'r';sign=1 if s=='l' else -1
        wind=envelope(u,[(0,0),(.24,1),(.45,0),(1,0)])
        strike=envelope(u,[(0,0),(.25,0),(.43,1),(.58,1),(1,0)])
        rotate('spine_02',(0,0,1),sign*(12*wind-16*strike))
        rotate('spine_03',(1,0,0),7*strike)
        rotate('clavicle_'+s,(0,1,0),-sign*14*wind)
        rotate('upperarm_'+s,(1,0,0),-82*wind-60*strike,True)
        rotate('upperarm_'+s,(0,1,0),-sign*10*wind,True)
        rotate('lowerarm_'+s,(1,0,0),25-65*wind-20*strike)
        for finger in ['index','middle','ring','pinky']:
            for segment in ['01','02','03']:
                p=rig.pose.bones[f'{finger}_{segment}_{s}'];p.rotation_quaternion=Quaternion((1,0,0),math.radians(45*(wind+strike)))
    elif name in ['HitLight','HitHeavy']:
        heavy=name=='HitHeavy';count=5 if heavy else 1;length=.24 if heavy else .16
        start=.22 if heavy else .20;end=duration-.35;progress=clamp((t-start)/(end-start))*count
        recoil=envelope(u,[(0,0),(.08,1),(.22,.55),(.75,.25),(1,0)])
        rotate('spine_02',(1,0,0),-18*recoil if heavy else -10*recoil)
        rotate('head',(1,0,0),-9*recoil)
        drop-=.05*recoil
        positions={'l':0.,'r':0.}
        for step in range(count):
            s='l' if step%2==0 else 'r';local=clamp(progress-step)
            previous=positions[s];target=(step+1)*length
            positions[s]=previous+(target-previous)*smooth(local)
            if 0<local<1:feet[s].z+=.06*math.sin(math.pi*local);contact[s]=False
        for s in feet:
            feet[s].y+=positions[s]
            rotate('upperarm_'+s,(1,0,0),-30*recoil,True)
            rotate('lowerarm_'+s,(1,0,0),25-55*recoil)
        root.y=(positions['l']+positions['r'])/2
    rootq=Quaternion((0,0,1),yaw)
    rotate('Root',(0,0,1),math.degrees(yaw));move_world('Root',root)
    move_world('pelvis',(0,0,drop));bpy.context.view_layer.update()
    error=0.
    for s in feet:error=max(error,solve_leg(s,feet[s],rootq))
    if name in ['Walk','Run']:
        for s,offset in [('l',0),('r',.5)]:
            run=name=='Run';phase=2*math.pi*(u+offset)
            shoulder=rig.pose.bones['upperarm_'+s].head.copy()
            wrist=shoulder+Vector((.025 if s=='l' else -.025,
                -.12+.17*math.cos(phase) if run else -.03+.12*math.cos(phase),
                -.25 if run else -.41))*arm_scales[s]
            error=max(error,solve_arm(s,wrist,rootq))
    elif name.startswith('Attack'):
        s='l' if name=='AttackLeft' else 'r';sign=1 if s=='l' else -1
        shoulder=rig.pose.bones['upperarm_'+s].head.copy()
        neutral=Vector((sign*.025,-.03,-.41))
        wrist=shoulder+(neutral+(Vector((sign*.04,-.08,.25))-neutral)*wind+(Vector((-sign*.035,-.36,-.03))-neutral)*strike)*arm_scales[s]
        error=max(error,solve_arm(s,wrist,rootq))
    return {'root':list(root),'yaw':yaw,'targets':{s:list(v) for s,v in feet.items()},'contact':contact,'speed':speed,'reach_error':error,'breath':breath}

for name,duration,loop in clips:
    rig.animation_data_create();action=bpy.data.actions.new(name);rig.animation_data.action=action
    frame_count=round(duration*FPS);samples=[]
    for i in range(frame_count+1):
        # Do not evaluate an older action between solving and keying this frame.
        sample=motion(name,i/FPS,duration)
        for p in rig.pose.bones:
            for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(prop,frame=i+1)
        sample['frame']=i+1
        sample['actual_feet']={s:list(rig.pose.bones['foot_'+s].head) for s in ankles}
        samples.append(sample)
    action.use_fake_user=True;actions.append(action)
    manifest['clips'].append({'name':name,'duration':duration,'loop':loop,'frames':frame_count+1,'samples':samples,
        'root_motion':name.startswith('Turn') or name.startswith('Hit') or name=='Jump'})
    print('ACTION_BUILT',name,'max reach error',max(s['reach_error'] for s in samples),flush=True)

# Preserve editable body and animation source; no clothing, no source mutation.
rig.animation_data.action=None
for action in actions:
    track=rig.animation_data.nla_tracks.new();track.name=action.name;track.strips.new(action.name,1,action);track.mute=True
rig.animation_data.action=actions[0];scene.frame_set(1);scene.frame_end=96
bpy.ops.wm.save_as_mainfile(filepath=str(out/'body-actions.blend'))

# Export copies with fixed base shape, helper mask applied before armature evaluation.
dup=body.copy();dup.data=body.data.copy();scene.collection.objects.link(dup);dup.name='GameBody'
bpy.context.view_layer.objects.active=dup
for mod in dup.modifiers:
    if mod.type=='ARMATURE':mod.show_viewport=False
if dup.data.shape_keys:bpy.ops.object.shape_key_remove(all=True,apply_mix=True)
for mod in list(dup.modifiers):
    if mod.type=='MASK':bpy.ops.object.modifier_apply(modifier=mod.name)
for mod in dup.modifiers:
    if mod.type=='ARMATURE':mod.show_viewport=True
# Explicitly normalize the four largest deform weights, matching game-engine limits.
for v in dup.data.vertices:
    influences=sorted([(g.weight,g.group) for g in v.groups if group_names.get(g.group) in deform],reverse=True)
    total=sum(w for w,g in influences[:4])
    for w,g in influences:dup.vertex_groups[g].remove([v.index])
    for w,g in influences[:4]:dup.vertex_groups[g].add([v.index],w/total,'REPLACE')
bpy.ops.object.select_all(action='DESELECT');dup.select_set(True);rig.select_set(True)
rig.animation_data.action=None
for track in rig.animation_data.nla_tracks:track.mute=False
bpy.ops.export_scene.gltf(filepath=str(out/'body-actions.glb'),export_format='GLB',use_selection=True,export_animations=True,
    export_animation_mode='NLA_TRACKS',export_anim_slide_to_zero=True,export_apply=False,export_morph=False)
for track in rig.animation_data.nla_tracks:track.mute=True
body.hide_render=True;rig.animation_data.action=actions[0]
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.cycles.samples=16
scene.camera.data.ortho_scale=2.1
for name,duration,loop in clips:
    rig.animation_data.action=bpy.data.actions[name];scene.frame_set(1+round(duration*FPS*.4))
    center=rig.pose.bones['pelvis'].head+Vector((0,0,-.04))
    scene.camera.location=center+Vector((3,-5,.7));scene.camera.rotation_euler=(center-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
(out/'actions.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print('BODY_ACTIONS_COMPLETE',flush=True)
