extends SceneTree
func _initialize() -> void: call_deferred("build")
func own(node: Node,scene: Node) -> void:
	for child in node.get_children():
		child.owner=scene
		if child.scene_file_path.is_empty(): own(child,scene)
func build() -> void:
	for style in ["realistic","cartoon"]:
		var materials: Array[ShaderMaterial]=[]
		for role in ["bark","leaves"]:
			var mat := ShaderMaterial.new()
			mat.shader=load("res://tree_asset/materials/"+role+".gdshader")
			var prefix := "bark" if role=="bark" else "leaf"
			mat.set_shader_parameter("color_map",load("res://tree_asset/textures/"+prefix+"_"+style+"_albedo.png"))
			mat.set_shader_parameter("normal_map",load("res://tree_asset/textures/"+prefix+"_"+style+"_normal.png"))
			if role=="bark": mat.set_shader_parameter("roughness_map",load("res://tree_asset/textures/bark_"+style+"_roughness.png"))
			mat.set_shader_parameter("normal_strength",(.15 if style=="realistic" else .1) if role=="bark" else .25)
			ResourceSaver.save(mat,"res://tree_asset/materials/"+role+"_"+style+".tres")
			materials.append(mat)
		var tree := Node3D.new()
		tree.name="CoastalTree"
		tree.set_script(load("res://tree_asset/tree.gd"))
		tree.set("bark_material",materials[0])
		tree.set("leaf_material",materials[1])
		for lod in ["near","far"]:
			var model: Node3D=load("res://tree_asset/meshes/tree_"+lod+".glb").instantiate()
			model.name=lod.capitalize()
			tree.add_child(model)
		var body := StaticBody3D.new()
		body.name="TrunkCollision"
		tree.add_child(body)
		for index in range(4):
			var collision := CollisionShape3D.new()
			var shape := CylinderShape3D.new()
			shape.height=1.0
			shape.radius=[.3,.19,.14,.09][index]
			collision.shape=shape
			collision.position.y=index+.5
			body.add_child(collision)
		own(tree,tree)
		var packed := PackedScene.new()
		assert(packed.pack(tree)==OK)
		assert(ResourceSaver.save(packed,"res://tree_asset/tree_"+style+".tscn")==OK)
		tree.free()
	print("TREE_SCENES_BUILT")
	quit()
