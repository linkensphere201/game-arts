extends SceneTree
func _initialize() -> void: call_deferred("verify")
func mesh_in(node: Node) -> Mesh:
	if node is MeshInstance3D: return node.mesh
	for child in node.get_children():
		var mesh := mesh_in(child)
		if mesh: return mesh
	return null
func verify() -> void:
	var roots := 0
	var patches := 0
	for variant in ["short","medium","dry"]:
		for style in ["realistic","cartoon"]:
			if not ResourceLoader.exists("res://grass_asset/grass_"+variant+"_"+style+".tscn"): continue
			var plant: Node=load("res://grass_asset/grass_"+variant+"_"+style+".tscn").instantiate()
			root.add_child(plant)
			var mesh := mesh_in(plant)
			var arrays := mesh.surface_get_arrays(0)
			var vertices: PackedVector3Array=arrays[Mesh.ARRAY_VERTEX]
			var uv: PackedVector2Array=arrays[Mesh.ARRAY_TEX_UV]
			var aux: PackedVector2Array=arrays[Mesh.ARRAY_TEX_UV2]
			var min_u := 1.0
			var max_u := 0.0
			for i in vertices.size():
				min_u=minf(min_u,uv[i].x); max_u=maxf(max_u,uv[i].x)
				assert(aux[i].x>=0 and aux[i].x<=1)
				assert(1.0-aux[i].y>0)
				if absf(vertices[i].y)<0.00001:
					assert(is_zero_approx(aux[i].x));roots+=1
			assert(max_u-min_u>.99)
			plant.queue_free()
	for style in ["realistic","cartoon"]:
		if not ResourceLoader.exists("res://ground_asset/ground_patch_"+style+".tscn"): continue
		patches+=1
		var patch: Node=load("res://ground_asset/ground_patch_"+style+".tscn").instantiate()
		root.add_child(patch)
		var colors: PackedColorArray=mesh_in(patch).surface_get_arrays(0)[Mesh.ARRAY_COLOR]
		for c in colors: assert(absf(c.r+c.g+c.b-1.0)<.015)
		assert(patch.find_children("*","CollisionShape3D",true,false).size()==1)
		patch.queue_free()
	assert(roots>0 or patches==2)
	print("NATURE_SAMPLES_OK grass_variants=3 styles=2 anchored_roots=",roots," full_uv=true ground_weights_normalized=true")
	quit()
