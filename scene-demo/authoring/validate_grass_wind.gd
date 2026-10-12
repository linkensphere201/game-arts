extends SceneTree
## Actual imported mesh + production shader, two deterministic rendered wind phases.
func _initialize() -> void:
	call_deferred("verify")

func verify() -> void:
	var model: Node3D = load("res://sunward_coast/meshes/grass_tuft.glb").instantiate()
	root.add_child(model)
	var mesh_node: MeshInstance3D = model.find_children("*", "MeshInstance3D", true, false)[0]
	var material := ShaderMaterial.new()
	material.shader = load("res://sunward_coast/materials/grass.gdshader")
	material.set_shader_parameter("wind_strength", 2.0)
	mesh_node.material_override = material
	var vertices: PackedVector3Array = mesh_node.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var uvs: PackedVector2Array = mesh_node.mesh.surface_get_arrays(0)[Mesh.ARRAY_TEX_UV]
	var roots := 0
	var tips := 0
	for i in vertices.size():
		if absf(vertices[i].y) < 0.00001:
			roots += 1
			assert(is_equal_approx(uvs[i].y, 1.0)) # Regression: UV-based weight was inverted.
			assert(is_zero_approx(pow(clampf(vertices[i].y / 0.55, 0, 1), 2)))
		if vertices[i].y > 0.3: tips += 1
	assert(roots > 0 and tips > 0)
	var camera := Camera3D.new()
	root.add_child(camera)
	camera.position = Vector3(0, 0.28, 2)
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 1.35
	camera.look_at(Vector3(0, 0.28, 0))
	var light := DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-25, -15, 0)
	root.add_child(light)
	var world := WorldEnvironment.new()
	world.environment = Environment.new()
	world.environment.background_mode = Environment.BG_COLOR
	world.environment.background_color = Color(0.06, 0.08, 0.11)
	world.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	world.environment.ambient_light_color = Color.WHITE
	world.environment.ambient_light_energy = 0.5
	root.add_child(world)
	# Fixed baseline makes root anchoring visible in both screenshots.
	var baseline := MeshInstance3D.new()
	var bar := BoxMesh.new()
	bar.size = Vector3(1.0, 0.008, 0.008)
	baseline.mesh = bar
	baseline.position = Vector3(0, -0.006, 0.05)
	root.add_child(baseline)
	var frames: Array[Image] = []
	for phase in [0.0, 1.5]:
		material.set_shader_parameter("wind_time_override", phase)
		await process_frame
		await RenderingServer.frame_post_draw
		var img := root.get_texture().get_image()
		frames.append(img)
		assert(img.save_png("res://../validation/coast-rock/wind-%s.png" % str(phase)) == OK)
	assert(frames[0].get_data() != frames[1].get_data())
	print("WIND_CHECK_OK roots=", roots, " upper_vertices=", tips, " root_weight=0 rendered_phases_differ=true")
	quit()
