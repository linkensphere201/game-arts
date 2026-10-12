extends SceneTree
func _initialize() -> void:
	call_deferred("build")
func mesh_in(node: Node) -> Mesh:
	if node is MeshInstance3D: return node.mesh
	for child in node.get_children():
		var mesh := mesh_in(child)
		if mesh: return mesh
	return null
func own(node: Node, scene: Node) -> void:
	for child in node.get_children():
		child.owner = scene
		if child.scene_file_path.is_empty(): own(child, scene)
func save(node: Node, path: String) -> void:
	own(node,node)
	var packed := PackedScene.new()
	assert(packed.pack(node)==OK)
	assert(ResourceSaver.save(packed,path)==OK)
func build() -> void:
	var realistic := StandardMaterial3D.new()
	realistic.albedo_texture = load("res://stone_asset/textures/limestone_albedo.png")
	realistic.normal_enabled = true
	realistic.normal_scale = 0.35
	realistic.normal_texture = load("res://stone_asset/textures/limestone_normal.png")
	realistic.roughness_texture = load("res://stone_asset/textures/limestone_roughness.png")
	realistic.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_RED
	ResourceSaver.save(realistic,"res://stone_asset/materials/realistic.tres")
	var cartoon := ShaderMaterial.new()
	cartoon.shader = load("res://stone_asset/materials/cartoon.gdshader")
	cartoon.set_shader_parameter("albedo_map", realistic.albedo_texture)
	cartoon.set_shader_parameter("normal_map", realistic.normal_texture)
	cartoon.set_shader_parameter("roughness_map", realistic.roughness_texture)
	ResourceSaver.save(cartoon,"res://stone_asset/materials/cartoon.tres")
	for style in ["realistic","cartoon"]:
		var wrapper := Node3D.new()
		wrapper.name = "Stone_"+style
		wrapper.set_script(load("res://stone_asset/stone.gd"))
		wrapper.set("material",realistic if style=="realistic" else cartoon)
		var model: Node = load("res://stone_asset/meshes/limestone.glb").instantiate()
		wrapper.add_child(model)
		var body := StaticBody3D.new()
		body.name = "Collision"
		wrapper.add_child(body)
		var shape := CollisionShape3D.new()
		shape.shape = mesh_in(model).create_convex_shape()
		body.add_child(shape)
		save(wrapper,"res://stone_asset/"+style+".tscn")
		wrapper.free()
	var demo := Node3D.new()
	demo.name = "StoneStudy"
	root.add_child(demo)
	demo.set_script(load("res://demo.gd"))
	var names := ["ORIGINAL / 80 TRIANGLES", "GEOMETRY / NO TEXTURE", "REALISTIC / PBR", "CARTOON / STYLIZED"]
	for i in range(4):
		var stone: Node3D
		if i==0: stone=load("res://reference/limestone_original.glb").instantiate()
		elif i==1:
			stone=load("res://stone_asset/meshes/limestone.glb").instantiate()
			var plain := StandardMaterial3D.new()
			plain.albedo_color = Color(0.48,0.46,0.42)
			for node in stone.find_children("*","MeshInstance3D",true,false): node.material_override=plain
		else: stone=load("res://stone_asset/"+("realistic" if i==2 else "cartoon")+".tscn").instantiate()
		stone.position.x = (i-1.5)*3.4
		stone.name = "Sample%d"%i
		demo.add_child(stone)
		var label := Label3D.new()
		label.text = names[i]
		label.name = "Caption%d"%i
		label.position = Vector3(stone.position.x, -0.22, 1.25)
		label.rotation_degrees.x = -55
		label.font_size=36
		label.pixel_size=.0035
		demo.add_child(label)
	var floor_mesh := PlaneMesh.new()
	floor_mesh.size = Vector2(200,200)
	var floor_mat := StandardMaterial3D.new()
	floor_mat.albedo_color = Color(.18,.20,.22)
	floor_mesh.material = floor_mat
	var floor_node := MeshInstance3D.new()
	floor_node.mesh=floor_mesh
	floor_node.position.y=-.25
	demo.add_child(floor_node)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees=Vector3(-42,-28,0)
	sun.shadow_enabled=true
	sun.light_energy=1.0
	demo.add_child(sun)
	var world := WorldEnvironment.new()
	world.environment=Environment.new()
	world.environment.background_mode=Environment.BG_COLOR
	world.environment.background_color=Color(.065,.08,.1)
	world.environment.ambient_light_source=Environment.AMBIENT_SOURCE_COLOR
	world.environment.ambient_light_color=Color(.72,.8,1)
	world.environment.ambient_light_energy=.3
	world.environment.tonemap_mode=Environment.TONE_MAPPER_ACES
	world.environment.ssao_enabled=true
	demo.add_child(world)
	var camera := Camera3D.new()
	camera.name="Camera"
	demo.add_child(camera)
	save(demo,"res://demo.tscn")
	print("STONE_DEMO_BUILT")
	quit()
