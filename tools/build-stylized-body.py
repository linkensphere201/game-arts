"""M5.2.9.2.1: non-destructive static manga proportion study.

Blender -b -P SCRIPT -- SOURCE_BODY_BLEND OUTPUT_DIR
The new mesh has Basis/Style shape keys; original source is never saved over.
No animation compatibility is implied by this proportion-only deliverable.
"""
import sys, math, json, hashlib
from pathlib import Path
import bpy
from mathutils import Vector

source, out = map(Path, sys.argv[sys.argv.index('--') + 1:])
out.mkdir(parents=True, exist_ok=True)
before = hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
original = bpy.data.objects['Standard_adult_body']
deps = bpy.context.evaluated_depsgraph_get()
mesh = bpy.data.meshes.new_from_object(original.evaluated_get(deps), depsgraph=deps)
body = bpy.data.objects.new('Stylized_body_PROPORTIONS_ONLY', mesh)
bpy.context.collection.objects.link(body)
body.matrix_world = original.matrix_world.copy()
original.hide_render = True
original.hide_set(True)
body.shape_key_add(name='Basis')
style = body.shape_key_add(name='Manga_6_25_heads')
height = max(v.co.z for v in mesh.vertices)
# Chin plane is an explicitly authored visual landmark, not an automatic
# anatomical segmentation or an official Nintendo measurement.
chin = 1.344
target_chin = height - height / 6.25
anchors = [(0, 0), (.065, .065), (.451, .475), (.816, .842),
           (.96, .982), (1.145, 1.133), (1.245, 1.205),
           (chin, target_chin), (height, height)]

def smooth(a, b, value):
    t = min(1., max(0., (value-a)/(b-a)))
    return t*t*(3-2*t)

def vertical(z):
    for (a, x), (b, y) in zip(anchors, anchors[1:]):
        if z <= b:
            return x + (z-a)/(b-a)*(y-x)
    return z

for v, dst in zip(mesh.vertices, style.data):
    x, y, z = v.co
    head = smooth(1.27, chin + .025, z)
    central = 1-smooth(.13, .25, abs(x))
    waist = math.exp(-((z-.97)/.105)**2)*central
    chest = math.exp(-((z-1.135)/.105)**2)*central
    neck = math.exp(-((z-1.30)/.045)**2)*central
    jaw = math.exp(-((z-1.375)/.042)**2)*head
    # Preserve limb centerlines while slimming thighs/calves locally.
    leg = (1-smooth(.72, .83, z))*smooth(.08, .19, z)
    axis = .179 + min(1., max(0., (z-.065)/.751))*(.097-.179)
    sx = abs(x)
    sx = axis+(sx-axis)*(1-.10*leg)
    sx *= 1-.10*waist-.035*chest-.10*neck+.18*head-.075*jaw
    dst.co = (math.copysign(sx, x),
              y*(1-.075*waist-.07*chest-.10*neck+.12*head), vertical(z))
style.value = 1
for p in mesh.polygons:
    p.use_smooth = True
scene = bpy.context.scene
scene.render.resolution_x = 600
scene.render.resolution_y = 800
scene.cycles.samples = 24
camera = scene.camera
camera.data.ortho_scale = height*1.14
center = Vector((0, 0, height*.5))

def render(name, position):
    camera.location = center+Vector(position)
    camera.rotation_euler = (center-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath = str(out/(name+'.png'))
    bpy.ops.render.render(write_still=True)

style.value = 0
render('original-front', (0,-5,0))
style.value = 1
for name, pos in [('front',(0,-5,0)), ('side',(5,0,0)),
                  ('three-quarter',(3,-5,0)), ('game-view',(3,-5,4)),
                  ('back',(0,5,0))]:
    render(name,pos)
camera.location = center+Vector((0,-5,0))
camera.rotation_euler = (center-camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.wm.save_as_mainfile(filepath=str(out/'stylized-base-body.blend'))
assert before == hashlib.sha256(source.read_bytes()).hexdigest()
assert len(mesh.vertices) == 13380
assert all(math.isfinite(c) for v in style.data for c in v.co)
report = {'task':'M5.2.9.2.1','source':str(source),'source_sha256':before,
          'vertices':len(mesh.vertices),'height_m':height,
          'authored_chin_plane_before_m':chin,'authored_chin_plane_after_m':target_chin,
          'head_ratio_at_authored_landmark':height/(height-target_chin),
          'vertical_anchors':anchors,'scope':'Static proportions, no rig or animation adaptation',
          'notes':'Original preserved; evaluated helper-free topology and UV retained. Shape-key slider supports A/B. Facial design remains provisional.'}
(out/'proportions.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('STYLIZED_BODY_OK',json.dumps(report),flush=True)
