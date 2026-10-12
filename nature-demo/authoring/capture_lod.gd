extends SceneTree
func _initialize() -> void: call_deferred("capture")
func capture() -> void:
	var demo: Node=load("res://demo.tscn").instantiate()
	root.add_child(demo)
	demo.set_view(4)
	# Same camera and fixed wind phase, only representation changes.
	var tree: Node3D=demo.get_node("Tree0")
	tree._bark.set_shader_parameter("wind_time_override",0.0)
	tree._leaves.set_shader_parameter("wind_time_override",0.0)
	for model in tree.find_children("*","MeshInstance3D",true,false):
		model.visibility_range_begin=0
		model.visibility_range_end=0
	for lod in ["Near","Far"]:
		tree.get_node("Near").visible=lod=="Near"
		tree.get_node("Far").visible=lod=="Far"
		await create_timer(1).timeout
		await RenderingServer.frame_post_draw
		assert(root.get_texture().get_image().save_png("res://../validation/nature/tree-"+lod.to_lower()+".png")==OK)
	print("TREE_LOD_CAPTURE_OK")
	quit()
