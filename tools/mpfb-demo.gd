extends Node3D
var actor: Node3D
var player: AnimationPlayer
var walking := false
var capture := false
func find_skeleton(node: Node) -> Skeleton3D:
	if node is Skeleton3D:
		return node
	for child in node.get_children():
		var result := find_skeleton(child)
		if result != null:
			return result
	return null

func _ready() -> void:
	capture = "--capture" in OS.get_cmdline_user_args()
	actor = load("res://adventurer.glb").instantiate()
	add_child(actor)
	player = actor.find_child("AnimationPlayer", true, false) as AnimationPlayer
	assert(player != null, "Missing AnimationPlayer")
	print("ANIMATIONS ", player.get_animation_list())
	for key in ["Idle", "Walk"]:
		assert(player.has_animation(key), "Missing " + key)
		player.get_animation(key).loop_mode = Animation.LOOP_LINEAR
	player.play("Idle")
	var camera := Camera3D.new()
	add_child(camera)
	camera.position = Vector3(2.3,1.5,3.5)
	camera.look_at(Vector3(0,.8,0))
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 2.25
	camera.current = true
	var light := DirectionalLight3D.new()
	add_child(light)
	light.rotation_degrees = Vector3(-45,-35,0)
	light.light_energy = .85
	light.shadow_enabled = true
	var environment := WorldEnvironment.new()
	environment.environment = Environment.new()
	environment.environment.background_mode = Environment.BG_COLOR
	environment.environment.background_color = Color(.12,.15,.19)
	environment.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.environment.ambient_light_color = Color(.8,.85,1)
	environment.environment.ambient_light_energy = .6
	add_child(environment)
	var floor_mesh := MeshInstance3D.new()
	floor_mesh.mesh = PlaneMesh.new()
	floor_mesh.mesh.size = Vector2(5,5)
	var floor_material := StandardMaterial3D.new()
	floor_material.albedo_color = Color(.35,.39,.44)
	floor_mesh.material_override = floor_material
	add_child(floor_mesh)
	var ui := CanvasLayer.new()
	add_child(ui)
	var label := Label.new()
	label.position = Vector2(20,20)
	label.text = "MPFB character pilot | SPACE: Idle / Walk | LEFT / RIGHT: turn\nBody + sweater + trousers + boots + back sword (separate meshes)"
	ui.add_child(label)
	if capture:
		player.play("Walk")
		player.pause()
		for frame in range(24):
			player.seek(float(frame)/24,true)
			await get_tree().process_frame
			await RenderingServer.frame_post_draw
			get_viewport().get_texture().get_image().save_png("res://walk-%02d.png" % frame)
		player.seek(.25,true)
		await RenderingServer.frame_post_draw
		get_viewport().get_texture().get_image().save_png("res://godot-preview.png")
		print("MPFB_GODOT_CAPTURE_OK")
		get_tree().quit()
	elif "--verify" in OS.get_cmdline_user_args():
		var skeleton := find_skeleton(actor)
		assert(skeleton != null and skeleton.get_bone_count() == 53)
		var foot := skeleton.find_bone("foot_l")
		assert(foot >= 0)
		for key in ["Idle", "Walk"]:
			player.play(key)
			player.seek(0,true)
			var first := skeleton.get_bone_global_pose(foot).origin
			player.seek(.25,true)
			var movement := first.distance_to(skeleton.get_bone_global_pose(foot).origin)
			print(key," foot displacement: ",movement)
			assert(movement < .0001 if key == "Idle" else movement > .02)
		print("MPFB_GODOT_ANIMATION_OK")
		get_tree().quit()

func _process(delta: float) -> void:
	if Input.is_action_just_pressed("ui_accept"):
		walking = not walking
		player.play("Walk" if walking else "Idle",.15)
	actor.rotate_y(Input.get_axis("ui_left","ui_right") * delta)
