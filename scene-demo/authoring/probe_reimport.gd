extends SceneTree
func mesh_in(node: Node) -> Mesh:
	if node is MeshInstance3D: return node.mesh
	for child in node.get_children():
		var found := mesh_in(child)
		if found != null: return found
	return null
func _initialize() -> void:
	var prop: Node3D = load("res://sunward_coast/props/coastal_tree.tscn").instantiate()
	root.add_child(prop)
	var width := mesh_in(prop.get_node("Model")).get_aabb().size.x
	assert(prop.has_node("Collision/Shape"))
	assert(is_equal_approx(prop.get_node("Collision/Shape").shape.radius,0.28))
	print("REIMPORT_WIDTH=",width)
	quit()
