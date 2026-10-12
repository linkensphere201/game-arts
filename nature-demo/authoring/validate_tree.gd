extends SceneTree
func _initialize() -> void: call_deferred("verify")
func verify() -> void:
	var trees: Array[Node3D]=[]
	for style in ["realistic","cartoon"]:
		var tree: Node3D=load("res://tree_asset/tree_"+style+".tscn").instantiate()
		root.add_child(tree)
		trees.append(tree)
		var counts: Array[int]=[]
		var roots := 0
		for lod in ["Near","Far"]:
			var count := 0
			var roles := 0
			for model in tree.get_node(lod).find_children("*","MeshInstance3D",true,false):
				count+=model.mesh.get_faces().size()/3
				assert(model.material_override is ShaderMaterial)
				var shader_path: String=model.material_override.shader.resource_path
				if model.name.begins_with("Bark"):
					assert(shader_path.ends_with("bark.gdshader"));roles+=1
					var vertices: PackedVector3Array=model.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
					for v in vertices:
						if absf(v.y)<.0001: roots+=1
				else:
					assert(shader_path.ends_with("leaves.gdshader"));roles+=1
				assert(model.visibility_range_begin==28 if lod=="Far" else model.visibility_range_end==28)
			assert(roles==2)
			counts.append(count)
		print("TREE_COUNTS ",counts," roots=",roots)
		assert(counts[0]==5974 and counts[1]==3070 and roots>0)
		assert(tree.find_children("*","CollisionShape3D",true,false).size()==4)
	assert(trees[0]._leaves!=trees[1]._leaves)
	trees[0].wind_strength=0
	assert(trees[0]._leaves.get_shader_parameter("wind_strength")==0)
	assert(trees[1]._leaves.get_shader_parameter("wind_strength")>0)
	print("TREE_CHECK_OK separate_materials=true near=5974 far=3070 root_vertices_found=true wind_isolated=true trunk_colliders=4")
	for tree in trees: tree.queue_free()
	await process_frame
	quit()
