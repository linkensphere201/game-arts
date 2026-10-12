extends SceneTree
var failures: Array[String] = []
func check(ok: bool, message: String) -> void:
	if not ok:
		failures.append(message)
		printerr("FAIL ",message)
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var resource: PackedScene = load("res://sunward_coast/scenes/environment.tscn")
	var a: Node3D = resource.instantiate()
	var b: Node3D = resource.instantiate()
	root.add_child(a)
	root.add_child(b)
	b.position.x = 100
	await process_frame
	check(a._prepared and b._prepared,"Both instances initialize")
	a.grass_density = 0.4
	a.wind_strength = 0.0
	a.sunlight = 0.6
	a.shallow_water = Color(0.4,0.2,0.1)
	var ga: MultiMeshInstance3D = a.get_node("GrassPatches").get_child(0)
	var gb: MultiMeshInstance3D = b.get_node("GrassPatches").get_child(0)
	check(ga.multimesh != gb.multimesh,"Instance buffers isolated")
	check(ga.multimesh.visible_instance_count < gb.multimesh.visible_instance_count,"Density isolated")
	check(a._water_material != b._water_material,"Water materials isolated")
	check(b._water_material.get_shader_parameter("shallow_color") == b.shallow_water,"Other water unchanged")
	check(is_equal_approx(b.get_node("AfternoonSun").light_energy,0.95),"Other sunlight unchanged")
	check(is_equal_approx(a._grass_material.get_shader_parameter("wind_strength"),0.0),"Wind responds")
	var files := DirAccess.get_files_at("res://sunward_coast/props")
	var count := 0
	for file in files:
		if not file.ends_with(".tscn"): continue
		count += 1
		var path := "res://sunward_coast/props/"+file
		var text := FileAccess.get_file_as_string(path)
		check(text.contains(".glb"),"Wrapper retains GLB reference: "+file)
		check(not text.contains("PackedByteArray"),"No baked mesh copy: "+file)
		var prop: Node3D = load(path).instantiate()
		root.add_child(prop)
		check(prop.has_node("Model"),"Model exists: "+file)
		prop.queue_free()
	check(count == 17,"17 linked wrappers")
	print("PACK_VALIDATION ",JSON.stringify({"wrappers":count,"isolation_checks":true,"failures":failures}))
	a.queue_free()
	b.queue_free()
	await process_frame
	quit(0 if failures.is_empty() else 1)
