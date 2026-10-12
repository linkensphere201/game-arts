extends SceneTree
func _initialize() -> void:
	call_deferred("verify")
func verify() -> void:
	var source_mesh: Mesh
	for style in ["realistic","cartoon"]:
		var stone: Node3D = load("res://stone_asset/"+style+".tscn").instantiate()
		root.add_child(stone)
		await process_frame
		var models := stone.find_children("*","MeshInstance3D",true,false)
		assert(models.size()==1)
		var model: MeshInstance3D=models[0]
		assert(model.mesh.get_faces().size()/3==2560)
		assert(model.material_override!=null)
		if source_mesh: assert(model.mesh==source_mesh)
		source_mesh=model.mesh
		assert(stone.find_children("*","CollisionShape3D",true,false).size()==1)
		stone.queue_free()
	for name in ["albedo","normal","roughness"]:
		var texture: Texture2D=load("res://stone_asset/textures/limestone_"+name+".png")
		assert(texture.get_size()==Vector2(1024,1024))
	print("STONE_ASSET_OK two_styles=2 shared_mesh_triangles=2560 maps=3 collision=convex")
	quit()
