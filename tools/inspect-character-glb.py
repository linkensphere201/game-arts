"""Non-destructive Blender GLB inspection. Run with blender -b -t 4 -P SCRIPT -- INPUT OUTPUT."""
import sys, json, hashlib, math
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector

source, destination = map(Path, sys.argv[sys.argv.index('--') + 1:])
destination.mkdir(parents=True, exist_ok=True)
report_path = destination / 'inspection.json'
if report_path.exists():
    raise RuntimeError('Choose a fresh output directory to preserve prior inspection.')
digest = hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(source))
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
report = {'source': str(source), 'sha256_before': digest, 'objects': [], 'images': [],
          'limitations': 'Raw vertex connectivity can include UV/normal seams. It cannot establish anatomical adhesion or deformation quality.'}
points = []
for obj in meshes:
    mesh = obj.data
    print('INSPECT', obj.name, len(mesh.vertices), len(mesh.polygons), flush=True)
    coords = np.empty(len(mesh.vertices) * 3, dtype=np.float32)
    mesh.vertices.foreach_get('co', coords)
    edges = np.empty(len(mesh.edges) * 2, dtype=np.int32)
    mesh.edges.foreach_get('vertices', edges)
    # Union by size; inspect raw components without altering mesh data.
    parent = list(range(len(mesh.vertices)))
    sizes = [1] * len(parent)
    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for a, b in edges.reshape(-1, 2):
        a, b = root(int(a)), root(int(b))
        if a != b:
            if sizes[a] < sizes[b]: a, b = b, a
            parent[b] = a
            sizes[a] += sizes[b]
    components = sorted((sizes[i] for i in range(len(parent)) if parent[i] == i), reverse=True)
    mesh.calc_loop_triangles()
    report['objects'].append({'name': obj.name, 'vertices': len(mesh.vertices),
        'triangles': len(mesh.loop_triangles), 'raw_components': len(components),
        'largest_components_vertices': components[:20],
        'vertex_groups': len(obj.vertex_groups), 'modifiers': [m.type for m in obj.modifiers]})
    points.extend(obj.matrix_world @ Vector(c) for c in obj.bound_box)
    del parent, sizes, edges, coords
for img in bpy.data.images:
    report['images'].append({'name': img.name, 'size': list(img.size)})
low = Vector(tuple(min(p[i] for p in points) for i in range(3)))
high = Vector(tuple(max(p[i] for p in points) for i in range(3)))
center = (low + high) / 2
height = high.z - low.z
report['world_bounds'] = [list(low), list(high)]
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 12
scene.cycles.use_denoising = True
scene.render.resolution_x = 640
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.world = bpy.data.worlds.new('Inspection world')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value = 0.7
scene.view_settings.view_transform = 'Standard'
bpy.ops.object.camera_add()
camera = bpy.context.object
camera.data.type = 'ORTHO'
camera.data.ortho_scale = height * 1.15
scene.camera = camera
bpy.ops.object.light_add(type='AREA', location=center + Vector((0, -height*2, height*2)))
light = bpy.context.object
light.data.energy = 100
light.data.shape = 'DISK'
light.data.size = height * 3
light.rotation_euler = (center-light.location).to_track_quat('-Z','Y').to_euler()
for name, angle in [('front',0),('right',90),('back',180),('left',270),('oblique',35)]:
    radians = math.radians(angle)
    camera.location = center + Vector((math.sin(radians)*height*3, -math.cos(radians)*height*3, height*.04))
    camera.rotation_euler = (center-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath = str(destination / (name + '.png'))
    print('RENDER', name, flush=True)
    bpy.ops.render.render(write_still=True)
report['sha256_after'] = hashlib.sha256(source.read_bytes()).hexdigest()
assert report['sha256_after'] == digest
report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
print('INSPECTION_COMPLETE', report_path, flush=True)
