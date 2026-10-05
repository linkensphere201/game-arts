extends SceneTree
## M3.4.1: offline construction. The delivered scenes need no generator at runtime.
var rng := RandomNumberGenerator.new()
var landscape: Node3D

func shore(x: float) -> float:
	return -7.0 + 2.5*sin(x*0.13) + 1.1*sin(x*0.31)

func height(x: float, z: float) -> float:
	var d := z-shore(x)
	return -1.8+3.2*smoothstep(-4.0,7.0,d)+smoothstep(4.0,15.0,d)*(0.65+0.55*sin(x*0.12+z*0.07)+0.35*cos(z*0.15-x*0.06))

func first_mesh(n: Node) -> Mesh:
	if n is MeshInstance3D:
		return n.mesh
	for c in n.get_children():
		var found := first_mesh(c)
		if found != null:
			return found
	return null

func asset_mesh(asset: String) -> Mesh:
	var instance: Node = load("res://assets/"+asset+".glb").instantiate()
	var mesh := first_mesh(instance)
	instance.free()
	return mesh

func attach(node: Node, parent: Node, label: String) -> void:
	node.name = label
	parent.add_child(node)

func own_children(node: Node, scene: Node) -> void:
	for c in node.get_children():
		c.owner = scene
		own_children(c, scene)

func save_scene(node: Node, path: String) -> void:
	own_children(node, node)
	var packed := PackedScene.new()
	assert(packed.pack(node) == OK)
	assert(ResourceSaver.save(packed, path) == OK)

func prop(mesh: Mesh, label: String, at: Vector3, scale_factor: Vector3, parent: Node) -> MeshInstance3D:
	var n := MeshInstance3D.new()
	n.mesh = mesh
	n.position = at
	n.scale = scale_factor
	attach(n, parent, label)
	return n

func _initialize() -> void:
	call_deferred("build")

func build() -> void:
	rng.seed = 731
	landscape = Node3D.new()
	landscape.name = "SunwardCoast"
	root.add_child(landscape)
	var terrain := prop(asset_mesh("terrain"), "MeadowAndBeach", Vector3.ZERO, Vector3.ONE, landscape)
	var ground_material := terrain.mesh.surface_get_material(0).duplicate() as StandardMaterial3D
	ground_material.vertex_color_use_as_albedo = true
	terrain.material_override = ground_material
	var ground := StaticBody3D.new()
	attach(ground, terrain, "GroundCollision")
	var shape := CollisionShape3D.new()
	shape.shape = terrain.mesh.create_trimesh_shape()
	attach(shape, ground, "Shape")
	var sea := PlaneMesh.new()
	sea.size = Vector2(1600,1600)
	var water := ShaderMaterial.new()
	water.shader = load("res://materials/ocean.gdshader")
	ResourceSaver.save(water,"res://materials/ocean.tres")
	sea.material = water
	prop(sea, "Sea", Vector3(0,0,-450), Vector3.ONE, landscape)
	var grass_mesh := asset_mesh("grass_tuft").duplicate() as ArrayMesh
	var grass_mat := ShaderMaterial.new()
	grass_mat.shader = load("res://materials/grass.gdshader")
	grass_mat.set_shader_parameter("root_color",Color(0.16,0.30,0.07,1))
	grass_mat.set_shader_parameter("tip_color",Color(0.57,0.68,0.22,1))
	ResourceSaver.save(grass_mat, "res://materials/grass.tres")
	for s in range(grass_mesh.get_surface_count()):
		grass_mesh.surface_set_material(s, grass_mat)
	ResourceSaver.save(grass_mesh,"res://assets/wind_grass.res")
	var grasses := Node3D.new()
	attach(grasses,landscape,"GrassPatches")
	var flower_mesh := asset_mesh("daisy")
	var flowers := Node3D.new()
	attach(flowers,landscape,"Wildflowers")
	var grass_count := 0
	var flower_count := 0
	for gx in range(5):
		for gz in range(4):
			var transforms: Array[Transform3D] = []
			var flower_transforms: Array[Transform3D] = []
			for i in range(720):
				var x := -19.8+gx*7.9+rng.randf()*7.9
				var z := -6.0+gz*6.9+rng.randf()*6.9
				var d := z-shore(x)
				var path_distance := absf(x-2.0-2.0*sin(z*0.17))
				if d < 6.5 or path_distance < 0.85 or rng.randf() < 0.08:
					continue
				var size := rng.randf_range(0.4,0.85)
				var t := Transform3D(Basis(Vector3.UP,rng.randf()*TAU).scaled(Vector3(size,size,size)),Vector3(x,height(x,z)-0.035,z))
				transforms.append(t)
				if rng.randf() < 0.025 and d > 9.0:
					flower_transforms.append(t)
			grass_count += transforms.size()
			flower_count += flower_transforms.size()
			make_batch(grass_mesh,transforms,grasses,"Grass_%02d_%02d"%[gx,gz],true)
			make_batch(flower_mesh,flower_transforms,flowers,"Flowers_%02d_%02d"%[gx,gz],false)
	var trees := Node3D.new()
	attach(trees,landscape,"CoastalTrees")
	var tree_mesh := asset_mesh("coastal_tree")
	var locations := [Vector2(-12,4),Vector2(-15,9),Vector2(-10,13),Vector2(13,14),Vector2(16,18)]
	for i in range(locations.size()):
		var p: Vector2 = locations[i]
		var size := rng.randf_range(0.85,1.15)
		var tree := prop(tree_mesh,"Tree_%02d"%i,Vector3(p.x,height(p.x,p.y),p.y),Vector3.ONE*size,trees)
		tree.rotation.y = rng.randf()*TAU
		var body := StaticBody3D.new()
		attach(body,tree,"TrunkCollision")
		var collider := CollisionShape3D.new()
		var cylinder := CylinderShape3D.new()
		cylinder.height = 3.2
		cylinder.radius = 0.3
		collider.shape = cylinder
		collider.position.y = 1.6
		attach(collider,body,"Shape")
	var rocks := Node3D.new()
	attach(rocks,landscape,"LimestoneOutcrops")
	var rock_mesh := asset_mesh("limestone")
	var bush_mesh := asset_mesh("shrub")
	for i in range(22):
		var x := rng.randf_range(-19,19)
		var z := shore(x)+rng.randf_range(1.0,5.0)
		if i < 5:
			x = -12.0+rng.randf_range(-3,3)
			z = 4.0+rng.randf_range(-2,2)
		var s := rng.randf_range(0.35,1.0)
		var rock := prop(rock_mesh,"Rock_%02d"%i,Vector3(x,height(x,z)-0.12,z),Vector3(s,s*rng.randf_range(0.7,1.2),s),rocks)
		rock.rotation.y = rng.randf()*TAU
		rock.create_trimesh_collision()
	for i in range(12):
		var x := rng.randf_range(-18,18)
		var z := rng.randf_range(4,20)
		if absf(x-2.0-2.0*sin(z*0.17)) < 2.0:
			continue
		var s := rng.randf_range(0.55,0.95)
		prop(bush_mesh,"Shrub_%02d"%i,Vector3(x,height(x,z)-0.05,z),Vector3.ONE*s,landscape)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-38,-36,0)
	sun.light_color = Color(1.0,0.91,0.73)
	sun.light_energy = 0.95
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 160.0
	attach(sun,landscape,"AfternoonSun")
	var world := WorldEnvironment.new()
	var env := Environment.new()
	var sky := Sky.new()
	var sky_mat := ProceduralSkyMaterial.new()
	sky_mat.sky_top_color = Color("5699c5")
	sky_mat.sky_horizon_color = Color("d0e2d8")
	sky_mat.ground_horizon_color = Color("d0e2d8")
	sky_mat.ground_bottom_color = Color("9d9770")
	sky.sky_material = sky_mat
	env.background_mode = Environment.BG_SKY
	env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color("bbd6df")
	env.ambient_light_energy = 0.35
	env.tonemap_mode = Environment.TONE_MAPPER_ACES
	env.fog_enabled = true
	env.fog_light_color = Color("b9d9d6")
	env.fog_density = 0.0016
	world.environment = env
	attach(world,landscape,"SkyAndAtmosphere")
	await process_frame
	await process_frame
	save_scene(landscape,"res://levels/coast_environment.tscn")
	var demo := Node3D.new()
	demo.name = "SunwardCoastDemo"
	demo.set_script(load("res://scripts/coast_demo.gd"))
	var scenery: Node = load("res://levels/coast_environment.tscn").instantiate()
	demo.add_child(scenery)
	scenery.owner = demo
	var camera := Camera3D.new()
	camera.name = "Camera"
	camera.far = 1400
	camera.fov = 62
	demo.add_child(camera)
	camera.owner = demo
	var packed := PackedScene.new()
	assert(packed.pack(demo) == OK)
	assert(ResourceSaver.save(packed,"res://levels/coast.tscn") == OK)
	demo.free()
	print("COAST_BUILD_OK grass=%d flowers=%d trees=%d"%[grass_count,flower_count,locations.size()])
	landscape.queue_free()
	await process_frame
	await process_frame
	quit()

func make_batch(mesh: Mesh, transforms: Array[Transform3D], parent: Node, label: String, tint: bool) -> void:
	if transforms.is_empty():
		return
	var batch := MultiMesh.new()
	batch.transform_format = MultiMesh.TRANSFORM_3D
	batch.use_colors = tint
	batch.mesh = mesh
	batch.instance_count = transforms.size()
	for i in range(transforms.size()):
		batch.set_instance_transform(i,transforms[i])
		if tint:
			batch.set_instance_color(i,Color(rng.randf_range(0.85,1.15),rng.randf_range(0.9,1.12),1))
	var node := MultiMeshInstance3D.new()
	node.multimesh = batch
	node.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	attach(node,parent,label)
