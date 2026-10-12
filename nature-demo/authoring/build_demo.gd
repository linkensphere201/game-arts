extends SceneTree
func _initialize() -> void: call_deferred("build")
func mesh_in(node: Node) -> Mesh:
	if node is MeshInstance3D: return node.mesh
	for child in node.get_children():
		var mesh := mesh_in(child)
		if mesh: return mesh
	return null
func own(node: Node, scene: Node) -> void:
	for child in node.get_children():
		child.owner=scene
		if child.scene_file_path.is_empty(): own(child,scene)
func save(node: Node,path: String) -> void:
	own(node,node)
	var packed := PackedScene.new()
	assert(packed.pack(node)==OK)
	assert(ResourceSaver.save(packed,path)==OK)
func wrapper(asset: String, model_name: String, style: String, mat: Material, collision: bool) -> void:
	var node := Node3D.new()
	node.name=model_name+"_"+style
	node.set_script(load("res://"+asset+("/patch.gd" if collision else "/clump.gd")))
	node.set("material",mat)
	var mesh_name := model_name+"_"+style+"_v2" if style=="realistic" else model_name
	var model: Node3D=load("res://"+asset+"/meshes/"+mesh_name+".glb").instantiate()
	node.add_child(model)
	if collision:
		var body := StaticBody3D.new()
		node.add_child(body)
		var shape := CollisionShape3D.new()
		shape.shape=mesh_in(model).create_trimesh_shape()
		body.add_child(shape)
	save(node,"res://"+asset+"/"+model_name+"_"+style+".tscn")
	node.free()
func build() -> void:
	var grass_settings: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://grass_asset/style-settings.json"))
	for style in (["realistic"] if "--realistic-only" in OS.get_cmdline_user_args() else ["realistic","cartoon"]):
		var ground := ShaderMaterial.new()
		ground.shader=load("res://ground_asset/materials/"+("ground_realistic.gdshader" if style=="realistic" else "ground.gdshader"))
		if style=="realistic":
			var ground_settings: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://ground_asset/style-settings.json"))
			for key in ["turf_bias","edge_breakup","wetness","normal_strength"]:
				ground.set_shader_parameter(key,float(ground_settings[key]))
		for layer in ["turf","soil","sand"]:
			for channel in ["albedo","normal","roughness"]:
				ground.set_shader_parameter(layer+"_"+("color" if channel=="albedo" else channel),load("res://ground_asset/textures/"+layer+"_"+style+"_"+channel+".png"))
		if style=="cartoon": ground.set_shader_parameter("normal_strength",0.25)
		ResourceSaver.save(ground,"res://ground_asset/materials/"+style+".tres")
		wrapper("ground_asset","ground_patch",style,ground,true)
		for variant in ["short","medium","dry"]:
			var grass := ShaderMaterial.new()
			grass.shader=load("res://grass_asset/materials/grass.gdshader")
			if style=="realistic": grass.set_shader_parameter("wind_strength",float(grass_settings["wind_strength"]))
			grass.set_shader_parameter("color_map",load("res://grass_asset/textures/blade_"+style+"_albedo.png"))
			grass.set_shader_parameter("normal_map",load("res://grass_asset/textures/blade_"+style+"_normal.png"))
			if variant=="dry": grass.set_shader_parameter("tint",Color(1.2,1.05,0.72) if style=="realistic" else Color(1.25,0.85,0.45))
			ResourceSaver.save(grass,"res://grass_asset/materials/"+variant+"_"+style+".tres")
			wrapper("grass_asset","grass_"+variant,style,grass,false)
	var demo := Node3D.new()
	demo.name="NatureStudy"
	root.add_child(demo)
	demo.set_script(load("res://demo.gd"))
	for index in range(2):
		var style := "realistic" if index==0 else "cartoon"
		var patch: Node3D=load("res://ground_asset/ground_patch_"+style+".tscn").instantiate()
		patch.name=style.capitalize()
		patch.position.x=-2.5 if index==0 else 2.5
		demo.add_child(patch)
		if ResourceLoader.exists("res://tree_asset/tree_"+style+".tscn"):
			var tree: Node3D=load("res://tree_asset/tree_"+style+".tscn").instantiate()
			tree.name="Tree"+str(index)
			tree.position=patch.position+Vector3(-.8,0,-.8)
			demo.add_child(tree)
		var plants := Node3D.new()
		plants.name="Plants"
		demo.add_child(plants)
		plants.position=patch.position
		var rng := RandomNumberGenerator.new()
		rng.seed=387
		# Four spatial chunks per patch, each sharing three mesh/material variants.
		for chunk in range(4):
			for v in range(3):
				var variant: String=["short","medium","dry"][v]
				var suffix := "_realistic_v2" if style=="realistic" else ""
				var instance: Node=load("res://grass_asset/meshes/grass_"+variant+suffix+".glb").instantiate()
				var mesh := mesh_in(instance)
				instance.free()
				var transforms: Array[Transform3D]=[]
				for i in range(int(grass_settings["scatter_attempts"][v]) if style=="realistic" else 80):
					var x := -1.95+(chunk%2)*2+rng.randf()*1.9
					var z := -1.95+(chunk/2)*2+rng.randf()*1.9
					var edge := absf(x+0.25*sin(z*2))
					var size := 1.0
					if style=="realistic":
						var verge := smoothstep(.12,.65,edge)
						var colony := .55+.25*sin(x*4.1+sin(z*3.2))+.2*sin(z*5.7-x*2.0)
						var density := verge*(.45+.55*colony)*(1.0-smoothstep(.65,1.15,z))
						if rng.randf()>density: continue
						if v==1 and (verge<.5 or rng.randf()>float(grass_settings["tall_probability"])): continue
						if v==2 and rng.randf()>float(grass_settings["dry_probability"]): continue
						size=rng.randf_range(.65,1.1)*lerpf(.3,1.0,verge)
					else:
						if z>0.9 or edge<0.42 or rng.randf()>0.6: continue
						if v==2 and rng.randf()>0.16: continue
						size=rng.randf_range(.65,1.1)
					transforms.append(Transform3D(Basis(Vector3.UP,rng.randf()*TAU).scaled(Vector3.ONE*size),Vector3(x,-0.002,z)))
				if transforms.is_empty(): continue
				var multimesh := MultiMesh.new()
				multimesh.transform_format=MultiMesh.TRANSFORM_3D
				multimesh.mesh=mesh
				multimesh.instance_count=transforms.size()
				for i in transforms.size(): multimesh.set_instance_transform(i,transforms[i])
				var batch := MultiMeshInstance3D.new()
				batch.multimesh=multimesh
				batch.material_override=load("res://grass_asset/materials/"+variant+"_"+style+".tres")
				batch.cast_shadow=GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
				batch.visibility_range_end=25
				batch.visibility_range_end_margin=3
				plants.add_child(batch)
		var label := Label3D.new()
		label.name="Caption"+str(index)
		label.text=style.to_upper()
		label.position=patch.position+Vector3(0,.05,2.25)
		label.rotation_degrees.x=-70
		label.font_size=48
		label.pixel_size=.006
		demo.add_child(label)
	var floor_node := MeshInstance3D.new()
	var plane := PlaneMesh.new()
	plane.size=Vector2(200,200)
	var mat := StandardMaterial3D.new()
	mat.albedo_color=Color(.15,.18,.20)
	plane.material=mat
	floor_node.mesh=plane
	floor_node.position.y=-.04
	demo.add_child(floor_node)
	var sun := DirectionalLight3D.new()
	sun.name="Sun"
	sun.rotation_degrees=Vector3(-42,-30,0)
	sun.shadow_enabled=true
	sun.light_energy=1.25
	demo.add_child(sun)
	var world := WorldEnvironment.new()
	world.environment=Environment.new()
	world.environment.background_mode=Environment.BG_COLOR
	world.environment.background_color=Color(.15,.20,.25)
	world.environment.ambient_light_source=Environment.AMBIENT_SOURCE_COLOR
	world.environment.ambient_light_color=Color(.76,.84,1)
	world.environment.ambient_light_energy=.7
	world.environment.tonemap_mode=Environment.TONE_MAPPER_ACES
	world.environment.ssao_enabled=false
	demo.add_child(world)
	var camera := Camera3D.new()
	camera.name="Camera"
	demo.add_child(camera)
	await process_frame
	save(demo,"res://demo.tscn")
	print("NATURE_DEMO_BUILT")
	quit()
