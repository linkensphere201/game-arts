extends Node3D
var actor: Node3D
var player: AnimationPlayer
var skeleton: Skeleton3D
var camera: Camera3D
var clips: Array
var selected := 0
var elapsed := 0.0
var playing := true
var travel := true
var capturing := false
var yaw := .5
var status: Label
var timeline: HSlider
var review_right_hand := false

func find_skeleton(node: Node) -> Skeleton3D:
	if node is Skeleton3D: return node
	for child in node.get_children():
		var found := find_skeleton(child)
		if found != null: return found
	return null

func _ready() -> void:
	clips = JSON.parse_string(FileAccess.get_file_as_string("res://actions.json"))["clips"]
	actor = load("res://body-actions.glb").instantiate()
	add_child(actor)
	player = actor.find_child("AnimationPlayer",true,false)
	skeleton = find_skeleton(actor)
	assert(player != null and skeleton != null)
	for clip in clips:
		assert(player.has_animation(clip.name),"Missing animation " + clip.name)
		player.get_animation(clip.name).loop_mode = Animation.LOOP_NONE
	camera = Camera3D.new()
	add_child(camera)
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 2.35
	camera.current = true
	var env := WorldEnvironment.new()
	env.environment = Environment.new()
	env.environment.background_mode = Environment.BG_COLOR
	env.environment.background_color = Color(.09,.12,.16)
	env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.environment.ambient_light_color = Color(.8,.86,1)
	env.environment.ambient_light_energy = .35
	add_child(env)
	var light := DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-40,-35,0)
	light.light_energy = .65
	light.shadow_enabled = true
	add_child(light)
	var ground := MeshInstance3D.new()
	var plane := PlaneMesh.new()
	plane.size = Vector2(100,100)
	ground.mesh = plane
	var material := ShaderMaterial.new()
	material.shader = Shader.new()
	material.shader.code = "shader_type spatial; varying vec3 world; void vertex(){world=(MODEL_MATRIX*vec4(VERTEX,1.0)).xyz;} void fragment(){vec2 g=abs(fract(world.xz*2.0+0.5)-0.5); float line=1.0-step(0.012,min(g.x,g.y)); ALBEDO=mix(vec3(0.18,0.21,0.25),vec3(0.26,0.29,0.32),line); ROUGHNESS=0.95;}"
	ground.material_override = material
	add_child(ground)
	var marker := MeshInstance3D.new()
	var disc := CylinderMesh.new()
	disc.top_radius = .24
	disc.bottom_radius = .24
	disc.height = .004
	marker.mesh = disc
	marker.position.y = .002
	var marker_material := StandardMaterial3D.new()
	marker_material.albedo_color = Color(.10,.35,.55)
	marker.material_override = marker_material
	add_child(marker)
	make_ui()
	choose(0)
	if "--verify" in OS.get_cmdline_user_args():
		verify_import()
	elif "--capture" in OS.get_cmdline_user_args():
		capturing = true
		capture_all()

func make_ui() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	var panel := VBoxContainer.new()
	var scroll := ScrollContainer.new()
	scroll.position = Vector2(18,18)
	scroll.size = Vector2(300,684)
	layer.add_child(scroll)
	panel.custom_minimum_size.x = 245
	scroll.add_child(panel)
	var title := Label.new()
	title.text = "白模动作验证 / Phase 1"
	panel.add_child(title)
	var labels := ["待机呼吸","行走","左转 90°","右转 90°","跑","跳","左手攻击","右手攻击","轻受击：后撤半步","重受击：后撤 5 步"]
	for i in range(clips.size()):
		var button := Button.new()
		button.text = str(clips[i].get("label", labels[i] if i < labels.size() else clips[i].name))
		button.pressed.connect(choose.bind(i))
		panel.add_child(button)
	var pause_button := Button.new()
	pause_button.text = "播放 / 暂停 [Space]"
	pause_button.pressed.connect(func(): playing = not playing)
	panel.add_child(pause_button)
	var replay := Button.new()
	replay.text = "从头播放"
	replay.pressed.connect(func(): choose(selected))
	panel.add_child(replay)
	var checkbox := CheckBox.new()
	checkbox.text = "行走 / 跑 显示位移"
	checkbox.button_pressed = true
	checkbox.toggled.connect(func(on: bool): travel = on)
	panel.add_child(checkbox)
	var hand_toggle := CheckBox.new()
	hand_toggle.text = "手型近景：查看右手"
	hand_toggle.toggled.connect(func(on: bool): review_right_hand = on)
	panel.add_child(hand_toggle)
	status = Label.new()
	panel.add_child(status)
	timeline = HSlider.new()
	timeline.step = .01
	timeline.value_changed.connect(func(value: float):
		elapsed = value
		apply_frame()
	)
	panel.add_child(timeline)
	var help := Label.new()
	help.text = "← → 旋转观察\n格线间距 0.5 米；蓝圆为起点\n单次动作结束后保持末帧"
	panel.add_child(help)

func choose(index: int) -> void:
	selected = index
	elapsed = 0
	playing = true
	timeline.max_value = float(clips[index].duration)
	player.play(clips[index].name)
	player.pause()
	apply_frame()

func apply_frame() -> void:
	var clip: Dictionary = clips[selected]
	player.seek(elapsed,true)
	var speed := float(clip.samples[0].speed)
	actor.position = Vector3(0,0,speed*elapsed if travel else 0.0)
	var root_index := skeleton.find_bone("Root")
	var root_position := skeleton.get_bone_global_pose(root_index).origin + actor.position
	var center := Vector3(root_position.x,.85,root_position.z)
	if clip.get("hand_view",false):
		var side := "r" if review_right_hand else "l"
		center = skeleton.get_bone_global_pose(skeleton.find_bone("hand_"+side)).origin + actor.position
		center += Vector3(0,-.05,0)
		camera.size = .38
		camera.position = center + Vector3(sin(yaw)*2,.1,cos(yaw)*2)
		camera.look_at(center)
		status.text = "%s / %s" % [clip.label, "右手" if review_right_hand else "左手"]
		timeline.set_value_no_signal(elapsed)
		return
	camera.size = 2.35
	# Offset framing so the character is not covered by the left UI panel.
	center += Vector3(-.30,0,.12)
	camera.position = center + Vector3(sin(yaw)*5,1.0,cos(yaw)*5)
	camera.look_at(center)
	status.text = "%s  %.2f / %.2fs" % [clip.name,elapsed,float(clip.duration)]
	timeline.set_value_no_signal(elapsed)

func _process(delta: float) -> void:
	if capturing: return
	if Input.is_action_just_pressed("ui_accept"): playing = not playing
	yaw += Input.get_axis("ui_left","ui_right")*delta
	if playing:
		elapsed += delta
		var clip: Dictionary = clips[selected]
		if elapsed > float(clip.duration):
			if clip.loop: elapsed = fmod(elapsed,float(clip.duration))
			else:
				elapsed = float(clip.duration)
				playing = false
	apply_frame()

func verify_import() -> void:
	var result := {"bones":skeleton.get_bone_count(),"clips":[],"max_foot_error_m":0.0}
	var ok := skeleton.get_bone_count() == 53
	for i in range(clips.size()):
		choose(i)
		var clip: Dictionary = clips[i]
		var max_error := 0.0
		var worst := {}
		for sample in clip.samples:
			elapsed = float(sample.frame-1)/30.0
			player.seek(elapsed,true)
			for side in ["l","r"]:
				var a: Array = sample.actual_feet[side]
				var expected := Vector3(float(a[0]),float(a[2]),-float(a[1]))
				var actual := skeleton.get_bone_global_pose(skeleton.find_bone("foot_"+side)).origin
				var error := actual.distance_to(expected)
				if error > max_error:
					worst = {"frame":sample.frame,"side":side,"expected":str(expected),"actual":str(actual)}
				max_error = maxf(max_error,error)
		result.clips.append({"name":clip.name,"foot_error_m":max_error,"duration":player.get_animation(clip.name).length,"worst":worst})
		result.max_foot_error_m = maxf(result.max_foot_error_m,max_error)
		ok = ok and max_error < .002
		print("VERIFY ",clip.name," foot error ",max_error)
	var file := FileAccess.open("res://engine-verification.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(result,"  "))
	print("BODY_ACTIONS_GODOT_OK" if ok else "BODY_ACTIONS_GODOT_FAILED")
	get_tree().quit(0 if ok else 1)

func capture_all() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://captures"))
	for i in range(clips.size()):
		choose(i)
		var clip: Dictionary = clips[i]
		var frames := int(ceil(float(clip.duration)*20))
		for frame in range(frames+1):
			elapsed = minf(float(frame)/20,float(clip.duration))
			apply_frame()
			await get_tree().process_frame
			await RenderingServer.frame_post_draw
			get_viewport().get_texture().get_image().save_png("res://captures/%s-%03d.png" % [clip.name,frame])
		print("CAPTURED ",clip.name)
	print("BODY_ACTIONS_CAPTURE_OK")
	get_tree().quit()
