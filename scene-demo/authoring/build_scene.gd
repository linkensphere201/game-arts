extends SceneTree
## M3.4.1: offline construction. The delivered scenes need no generator at runtime.
var rng := RandomNumberGenerator.new()
var landscape: Node3D
var meadow_noise := FastNoiseLite.new()
var placement_rng := RandomNumberGenerator.new()

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
	var instance: Node = load("res://sunward_coast/meshes/"+asset+".glb").instantiate()
	var mesh := first_mesh(instance)
	instance.free()
	return mesh

func attach(node: Node, parent: Node, label: String) -> void:
	node.name = label
	parent.add_child(node)

func own_children(node: Node, scene: Node) -> void:
	for c in node.get_children():
		c.owner = scene
		if c.scene_file_path.is_empty():
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
	placement_rng.seed = 1706
	meadow_noise.seed = 1706
	meadow_noise.frequency = 0.16
	landscape = Node3D.new()
	landscape.name = "SunwardCoast"
	root.add_child(landscape)
	build_library()
	landscape.set_script(load("res://sunward_coast/scripts/environment_controls.gd"))
	instance_prop("terrain","MeadowAndBeach",Vector3.ZERO,Vector3.ONE,landscape)
	var sea := PlaneMesh.new()
	sea.size = Vector2(1600,1600)
	var water := ShaderMaterial.new()
	water.shader = load("res://sunward_coast/materials/ocean.gdshader")
	ResourceSaver.save(water,"res://sunward_coast/materials/ocean.tres")
	sea.material = water
	prop(sea, "Sea", Vector3(0,0,-450), Vector3.ONE, landscape)
	var grass_mesh := asset_mesh("grass_tuft").duplicate() as ArrayMesh
	var grass_mat := ShaderMaterial.new()
	grass_mat.shader = load("res://sunward_coast/materials/grass.gdshader")
	grass_mat.set_shader_parameter("root_color",Color(0.16,0.30,0.07,1))
	grass_mat.set_shader_parameter("tip_color",Color(0.57,0.68,0.22,1))
	ResourceSaver.save(grass_mat, "res://sunward_coast/materials/grass.tres")
	for s in range(grass_mesh.get_surface_count()):
		grass_mesh.surface_set_material(s, grass_mat)
	ResourceSaver.save(grass_mesh,"res://sunward_coast/meshes/wind_grass.res")
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
				var patch := clampf(0.5+meadow_noise.get_noise_2d(x,z)*1.4,0.0,1.0)
				var edge_noise := meadow_noise.get_noise_2d(x*3.0,z*3.0)
				var verge := smoothstep(0.8,1.8+edge_noise*0.6,path_distance)
				var beach_edge := smoothstep(6.3,8.6+edge_noise,d)
				var density := lerpf(0.35,0.98,patch)*verge*beach_edge
				if placement_rng.randf() > density:
					continue
				var size := rng.randf_range(0.48,0.92)*lerpf(0.62,1.0,minf(verge,beach_edge))
				var t := Transform3D(Basis(Vector3.UP,rng.randf()*TAU).scaled(Vector3(size,size,size)),Vector3(x,height(x,z)-0.035,z))
				transforms.append(t)
				if rng.randf() < 0.055 and patch > 0.48 and d > 9.0:
					flower_transforms.append(t)
			grass_count += transforms.size()
			flower_count += flower_transforms.size()
			make_batch(grass_mesh,transforms,grasses,"Grass_%02d_%02d"%[gx,gz],true)
			make_batch(flower_mesh if gx%2==0 else asset_mesh("flower_blue"),flower_transforms,flowers,"Flowers_%02d_%02d"%[gx,gz],false)
	var trees := Node3D.new()
	attach(trees,landscape,"CoastalTrees")
	var tree_names := ["tree_windswept","coastal_tree","tree_sapling","coastal_tree","tree_windswept"]
	var locations := [Vector2(-12,4),Vector2(-15,9),Vector2(-10,13),Vector2(13,14),Vector2(16,18)]
	for i in range(locations.size()):
		var p: Vector2 = locations[i]
		var size := rng.randf_range(0.85,1.15)
		var tree := instance_prop(tree_names[i],"Tree_%02d"%i,Vector3(p.x,height(p.x,p.y),p.y),Vector3.ONE*size,trees)
		tree.rotation.y = rng.randf()*TAU
	var rocks := Node3D.new()
	attach(rocks,landscape,"LimestoneOutcrops")
	var rock_names := ["limestone","rock_flat","rock_tall"]
	var bush_names := ["shrub","shrub_low"]
	for i in range(22):
		var x := rng.randf_range(-19,19)
		var z := shore(x)+rng.randf_range(1.0,5.0)
		if i < 5:
			x = -12.0+rng.randf_range(-3,3)
			z = 4.0+rng.randf_range(-2,2)
		var s := rng.randf_range(0.35,1.0)
		var rock := instance_prop(rock_names[i%3],"Rock_%02d"%i,Vector3(x,height(x,z)-0.12,z),Vector3(s,s*rng.randf_range(0.7,1.2),s),rocks)
		rock.rotation.y = rng.randf()*TAU
	for i in range(12):
		var x := rng.randf_range(-18,18)
		var z := rng.randf_range(4,20)
		if absf(x-2.0-2.0*sin(z*0.17)) < 2.0:
			continue
		var s := rng.randf_range(0.55,0.95)
		instance_prop(bush_names[i%2],"Shrub_%02d"%i,Vector3(x,height(x,z)-0.05,z),Vector3.ONE*s,landscape)
	# Fixed focal point and small shoreline details; no expansion of the terrain.
	var bench := instance_prop("coastal_bench","RestingPlace",Vector3(-5,height(-5,0),0),Vector3.ONE,landscape)
	bench.rotation.y = 0.12
	for i in range(16):
		var x := -18.0+i*2.3
		var z := shore(x)+2.0+sin(i*1.7)*0.5
		instance_prop("pebbles","Pebbles_%02d"%i,Vector3(x,height(x,z)+0.015,z),Vector3.ONE*rng.randf_range(0.6,1.4),landscape)
	for i in range(3):
		var x := -13.0+i*12.0
		var z := shore(x)+3.0
		var wood := instance_prop("driftwood","Driftwood_%d"%i,Vector3(x,height(x,z),z),Vector3.ONE,landscape)
		wood.rotation.y = i*1.2
	for i in range(24):
		var x := rng.randf_range(-18,18)
		var z := shore(x)+6.7
		if absf(x-2.0-2.0*sin(z*0.17)) < 1.8: continue
		instance_prop("beach_reeds","Reeds_%02d"%i,Vector3(x,height(x,z),z),Vector3.ONE*0.8,landscape)
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
	save_scene(landscape,"res://sunward_coast/scenes/environment.tscn")
	var demo := Node3D.new()
	demo.name = "SunwardCoastDemo"
	demo.set_script(load("res://scripts/coast_demo.gd"))
	var scenery: Node = load("res://sunward_coast/scenes/environment.tscn").instantiate()
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
	build_gallery()
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
			batch.set_instance_color(i,Color(1.0,1.0,1.0).lerp(Color(0.8,0.91,0.72),clampf(0.5+meadow_noise.get_noise_2d(transforms[i].origin.x,transforms[i].origin.z),0.0,1.0)))
	var node := MultiMeshInstance3D.new()
	node.multimesh = batch
	node.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	attach(node,parent,label)


func instance_prop(asset_name: String, label: String, at: Vector3, size: Vector3, parent: Node) -> Node3D:
	var instance: Node3D = load("res://sunward_coast/props/"+asset_name+".tscn").instantiate()
	instance.position = at
	instance.scale = size
	attach(instance,parent,label)
	return instance

func build_library() -> void:
	var ground_material := ShaderMaterial.new()
	ground_material.shader = load("res://sunward_coast/materials/ground.gdshader")
	ResourceSaver.save(ground_material,"res://sunward_coast/materials/ground.tres")
	for asset_name in prop_names()+["terrain"]:
		var wrapper := Node3D.new()
		wrapper.name = asset_name
		wrapper.set_script(load("res://sunward_coast/scripts/prop.gd"))
		var model: Node3D = load("res://sunward_coast/meshes/"+asset_name+".glb").instantiate()
		model.name = "Model"
		wrapper.add_child(model)
		if asset_name == "terrain": wrapper.set("surface_override",ground_material)
		var collision: Shape3D
		var collision_position := Vector3.ZERO
		if asset_name == "terrain" or asset_name in ["limestone","rock_flat","rock_tall"]:
			collision = first_mesh(model).create_trimesh_shape()
		elif asset_name.begins_with("tree") or asset_name == "coastal_tree":
			var cylinder := CylinderShape3D.new()
			cylinder.height = 2.0 if asset_name=="tree_sapling" else 3.2
			cylinder.radius = 0.28
			collision_position.y = cylinder.height*0.5
			collision = cylinder
		elif asset_name == "coastal_bench":
			var box := BoxShape3D.new()
			box.size = Vector3(2.0,1.3,0.65)
			collision_position.y = 0.65
			collision = box
		if collision != null:
			var body := StaticBody3D.new()
			attach(body,wrapper,"Collision")
			var shape := CollisionShape3D.new()
			shape.shape = collision
			shape.position = collision_position
			attach(shape,body,"Shape")
		save_scene(wrapper,"res://sunward_coast/props/"+asset_name+".tscn")
		wrapper.free()

func prop_names() -> Array[String]:
	return ["coastal_tree","tree_windswept","tree_sapling","shrub","shrub_low","limestone","rock_flat","rock_tall","grass_tuft","grass_short","daisy","flower_blue","coastal_bench","driftwood","pebbles","beach_reeds"]

func build_gallery() -> void:
	var gallery := Node3D.new()
	gallery.name = "CoastalComponentGallery"
	root.add_child(gallery)
	var names := prop_names()
	for i in range(names.size()):
		var at := Vector3((i%4)*6-9,0,(i/4)*5-8)
		instance_prop(names[i],names[i],at,Vector3.ONE,gallery)
		var label := Label3D.new()
		label.text = names[i]
		label.position = at+Vector3(0,0.2,1.3)
		label.rotation_degrees.x = -60
		label.font_size = 36
		label.pixel_size = 0.008
		attach(label,gallery,"Label_%d"%i)
	var floor_mesh := PlaneMesh.new()
	floor_mesh.size = Vector2(28,25)
	var floor_mat := StandardMaterial3D.new()
	floor_mat.albedo_color = Color(0.27,0.3,0.24)
	floor_mesh.material = floor_mat
	prop(floor_mesh,"Floor",Vector3(0,-0.03,0),Vector3.ONE,gallery)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-45,-30,0)
	sun.shadow_enabled = true
	attach(sun,gallery,"Sun")
	var camera := Camera3D.new()
	camera.position = Vector3(17,23,27)
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 31
	attach(camera,gallery,"Camera")
	camera.look_at(Vector3(0,1,0))
	var world := WorldEnvironment.new()
	world.environment = Environment.new()
	world.environment.background_mode = Environment.BG_COLOR
	world.environment.background_color = Color(0.12,0.17,0.2)
	world.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	world.environment.ambient_light_color = Color(0.7,0.8,0.9)
	world.environment.ambient_light_energy = 0.5
	attach(world,gallery,"World")
	save_scene(gallery,"res://sunward_coast/scenes/gallery.tscn")
	gallery.queue_free()
