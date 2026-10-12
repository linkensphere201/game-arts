"""M3.6.2: one editable weathered limestone with baked PBR maps.
Run in Blender. Generated art stays local; no downloaded materials required.
"""
from pathlib import Path
import json
import math
import os
import tempfile
import bpy
from mathutils import Vector, noise

ROOT = Path(__file__).resolve().parents[2]
scratch = ROOT / '.local/rock-bake-temp'
scratch.mkdir(exist_ok=True)
os.environ['TEMP'] = str(scratch)
os.environ['TMP'] = str(scratch)
tempfile.tempdir = str(scratch)
OUT = ROOT / 'rock-demo/stone_asset/meshes'
OUT.mkdir(parents=True, exist_ok=True)
TEX = OUT.parent / 'textures'
TEX.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 8
scene.render.bake.margin = 12

# Continuous displacement and broad fracture cuts, not independent random vertices.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=6, radius=1)
high = bpy.context.object
high.name = 'Limestone_high_bake_source'
for v in high.data.vertices:
    p = v.co.copy()
    q = Vector((p.x*1.14, p.y*.91, p.z*.86))
    broad = noise.noise_vector(p*2.3 + Vector((4.1, 8.7, 2.3)))
    q += broad*.17
    # Sedimentary ledges and chipped surfaces are visible in the silhouette.
    q.z += .035*math.sin(q.x*9+q.y*3) + .025*noise.noise(p*15)
    cuts = [(Vector((.8,.3,.5)).normalized(),.83),
            (Vector((-.4,.8,.4)).normalized(),.82),
            (Vector((.15,-.5,.9)).normalized(),.85)]
    for normal, distance in cuts:
        excess = q.dot(normal)-distance
        if excess > 0: q -= normal*excess*.9
    q += p*(.013*noise.noise(p*32)+.006*noise.noise(p*73))
    q.x *= 1.12
    q.z = max(q.z, -.67) + .67
    v.co = q
for face in high.data.polygons: face.use_smooth = True
high.data.update()

mat = bpy.data.materials.new('Weathered limestone procedural master')
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
bsdf = nodes.get('Principled BSDF')
coord = nodes.new('ShaderNodeTexCoord')
def tex(scale, detail=3):
    n = nodes.new('ShaderNodeTexNoise')
    n.inputs['Scale'].default_value = scale
    n.inputs['Detail'].default_value = detail
    n.inputs['Roughness'].default_value = .72
    links.new(coord.outputs['Object'], n.inputs['Vector'])
    return n
broad, grain, pores = tex(2.8,4), tex(32,3), tex(145,2)
ramp = nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position = .23
ramp.color_ramp.elements[0].color = (.105,.095,.077,1)
ramp.color_ramp.elements[1].position = .78
ramp.color_ramp.elements[1].color = (.46,.42,.34,1)
middle = ramp.color_ramp.elements.new(.5)
middle.color = (.27,.25,.21,1)
links.new(broad.outputs['Fac'], ramp.inputs[0])
mix = nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'
mix.inputs[0].default_value = .32
links.new(ramp.outputs[0],mix.inputs[1]);links.new(grain.outputs['Fac'],mix.inputs[2])
links.new(mix.outputs[0],bsdf.inputs['Base Color'])
rough = nodes.new('ShaderNodeMapRange')
rough.inputs['From Min'].default_value = .2
rough.inputs['From Max'].default_value = .8
rough.inputs['To Min'].default_value = .65
rough.inputs['To Max'].default_value = .96
links.new(grain.outputs['Fac'],rough.inputs['Value'])
links.new(rough.outputs[0],bsdf.inputs['Roughness'])
bump = nodes.new('ShaderNodeBump')
bump.inputs['Strength'].default_value = .5
bump.inputs['Distance'].default_value = .028
links.new(grain.outputs['Fac'],bump.inputs['Height'])
fine = nodes.new('ShaderNodeBump')
fine.inputs['Strength'].default_value = .35
fine.inputs['Distance'].default_value = .006
links.new(pores.outputs['Fac'],fine.inputs['Height'])
links.new(bump.outputs['Normal'],fine.inputs['Normal'])
links.new(fine.outputs['Normal'],bsdf.inputs['Normal'])
high.data.materials.append(mat)

low = high.copy(); low.data = high.data.copy()
bpy.context.collection.objects.link(low)
low.name = 'limestone'
bpy.context.view_layer.objects.active = low
high.select_set(False);low.select_set(True)
dec = low.modifiers.new('Game silhouette budget','DECIMATE');dec.ratio = .125
bpy.ops.object.modifier_apply(modifier=dec.name)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(70),island_margin=.025)
bpy.ops.object.mode_set(mode='OBJECT')
target_mat = bpy.data.materials.new('Limestone baked PBR');target_mat.use_nodes = True
low.data.materials.clear();low.data.materials.append(target_mat)
target = target_mat.node_tree.nodes.new('ShaderNodeTexImage')
target_mat.node_tree.nodes.active = target
scene.render.bake.use_selected_to_active = True
scene.render.bake.cage_extrusion = .12
scene.render.bake.max_ray_distance = .25
high.select_set(True)
images = {}
for kind in ['albedo','normal','roughness']:
    img = bpy.data.images.new('limestone_'+kind, width=1024, height=1024, alpha=False)
    img.colorspace_settings.name = 'sRGB' if kind=='albedo' else 'Non-Color'
    target.image = img
    if kind=='albedo':
        scene.render.bake.use_pass_direct = False
        scene.render.bake.use_pass_indirect = False
        scene.render.bake.use_pass_color = True
        bpy.ops.object.bake(type='DIFFUSE')
    elif kind=='normal':
        scene.render.bake.normal_space = 'TANGENT'
        bpy.ops.object.bake(type='NORMAL')
    else:
        bpy.ops.object.bake(type='ROUGHNESS')
    img.filepath_raw = str(TEX / ('limestone_'+kind+'.png'))
    img.file_format = 'PNG';img.save();images[kind]=img
    print('BAKED',kind,flush=True)

nodes = target_mat.node_tree.nodes;links = target_mat.node_tree.links
principled = nodes.get('Principled BSDF')
target.image = images['albedo'];links.new(target.outputs['Color'],principled.inputs['Base Color'])
normal_tex = nodes.new('ShaderNodeTexImage');normal_tex.image=images['normal']
normal = nodes.new('ShaderNodeNormalMap')
links.new(normal_tex.outputs['Color'],normal.inputs['Color'])
links.new(normal.outputs['Normal'],principled.inputs['Normal'])
rough_tex=nodes.new('ShaderNodeTexImage');rough_tex.image=images['roughness']
links.new(rough_tex.outputs['Color'],principled.inputs['Roughness'])
target_mat.use_backface_culling = True
bpy.ops.object.select_all(action='DESELECT');low.select_set(True)
bpy.context.view_layer.objects.active=low
bpy.ops.export_scene.gltf(filepath=str(OUT/'limestone.glb'),export_format='GLB',use_selection=True,export_yup=True,export_tangents=True,export_materials='NONE')
high.hide_render=True;high.hide_set(True)
for image in images.values(): image.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art-source/environment/limestone-study.blend'))
record={'name':'limestone','vertices':len(low.data.vertices),'triangles':sum(len(p.vertices)-2 for p in low.data.polygons),
        'dimensions_m':[round(float(v),3) for v in low.dimensions], 'high_source_triangles':len(high.data.polygons),
        'textures':'1024x1024 albedo, tangent normal (OpenGL), roughness; geometry-only GLB + separate PNG'}
(OUT/'inventory.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print('ROCK_STUDY_OK',json.dumps(record),flush=True)
