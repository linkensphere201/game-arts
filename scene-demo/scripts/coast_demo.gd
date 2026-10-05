extends Node3D
## Navigation and presentation only. All scenery is saved in the editor scene.
@onready var camera: Camera3D = $Camera
var hud: CanvasLayer
var status: Label
var elapsed := 0.0
var photo_mode := false
var capture_dir := ""
var capture_index := 0
var sample_ms: Array[float] = []
var qa_duration := 0.0
const VIEWS := [
	[Vector3(5,9.5,18),Vector3(-1,1,-5)],
	[Vector3(1,4.7,9),Vector3(-6,2,-7)],
	[Vector3(-10,2,-6),Vector3(8,2,4)]
]

func _ready() -> void:
	set_view(0)
	create_hud()
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="):
			capture_dir = arg.trim_prefix("--capture-dir=")
		if arg.begins_with("--qa-seconds="):
			qa_duration = float(arg.trim_prefix("--qa-seconds="))

func set_view(index: int) -> void:
	camera.position = VIEWS[index][0]
	camera.look_at(VIEWS[index][1])

func create_hud() -> void:
	hud = CanvasLayer.new()
	add_child(hud)
	var title := Label.new()
	title.text = "SUNWARD / COAST"
	title.position = Vector2(40,32)
	title.add_theme_font_size_override("font_size",28)
	title.add_theme_color_override("font_color",Color("fff7df"))
	title.add_theme_color_override("font_shadow_color",Color(0,0,0,0.4))
	title.add_theme_constant_override("shadow_offset_y",2)
	hud.add_child(title)
	var subtitle := Label.new()
	subtitle.text = "01     THE COASTAL MEADOW"
	subtitle.position = Vector2(42,73)
	subtitle.add_theme_font_size_override("font_size",13)
	hud.add_child(subtitle)
	var controls := Label.new()
	controls.text = "RMB + mouse  look     WASD  move     Q / E  down / up     Shift  faster\n1 / 2 / 3  viewpoints     H  hide interface     Esc  release mouse"
	controls.position = Vector2(42,820)
	controls.add_theme_font_size_override("font_size",15)
	controls.add_theme_color_override("font_shadow_color",Color(0,0,0,0.7))
	controls.add_theme_constant_override("shadow_offset_y",2)
	hud.add_child(controls)
	status = Label.new()
	status.position = Vector2(1380,42)
	status.add_theme_font_size_override("font_size",14)
	hud.add_child(status)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_RIGHT:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED if event.pressed else Input.MOUSE_MODE_VISIBLE
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		camera.rotation.y -= event.relative.x*0.003
		camera.rotation.x = clampf(camera.rotation.x-event.relative.y*0.003,-1.45,1.45)
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: set_view(0)
			KEY_2: set_view(1)
			KEY_3: set_view(2)
			KEY_H:
				photo_mode = not photo_mode
				hud.visible = not photo_mode
			KEY_ESCAPE: Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

func _process(delta: float) -> void:
	elapsed += delta
	var motion := Vector3.ZERO
	if Input.is_physical_key_pressed(KEY_W): motion.z -= 1
	if Input.is_physical_key_pressed(KEY_S): motion.z += 1
	if Input.is_physical_key_pressed(KEY_A): motion.x -= 1
	if Input.is_physical_key_pressed(KEY_D): motion.x += 1
	if motion.length_squared() > 0:
		camera.position += camera.basis*motion.normalized()*delta*(24 if Input.is_physical_key_pressed(KEY_SHIFT) else 4)
	if Input.is_physical_key_pressed(KEY_Q): camera.position.y -= delta*8
	if Input.is_physical_key_pressed(KEY_E): camera.position.y += delta*8
	status.text = "%d FPS\nFREE CAMERA"%Engine.get_frames_per_second()
	if qa_duration > 0 and elapsed > 5:
		sample_ms.append(delta*1000)
	if not capture_dir.is_empty() and capture_index < 3 and elapsed > 5+capture_index*5:
		var index := capture_index
		capture_index += 1
		capture_view(index)
	if qa_duration > 0 and elapsed > qa_duration:
		qa_duration = 0
		write_metrics()
		get_tree().quit()

func capture_view(index: int) -> void:
	set_view(index)
	await get_tree().create_timer(1.0).timeout
	await RenderingServer.frame_post_draw
	var path := capture_dir.path_join("coast-%d.png"%(index+1))
	var error := get_viewport().get_texture().get_image().save_png(path)
	print("SCREENSHOT ",path," status=",error)

func write_metrics() -> void:
	if sample_ms.is_empty(): return
	sample_ms.sort()
	var total := 0.0
	for value in sample_ms: total += value
	var result := {"seconds":elapsed,"frames_sampled":sample_ms.size(),"mean_frame_ms":total/sample_ms.size(),
		"p95_frame_ms":sample_ms[int(sample_ms.size()*0.95)],"renderer":RenderingServer.get_current_rendering_method(),
		"gpu":RenderingServer.get_video_adapter_name(),"viewport":str(get_viewport().get_visible_rect().size)}
	print("RUNTIME_METRICS ",JSON.stringify(result))
	if not capture_dir.is_empty():
		var file := FileAccess.open(capture_dir.path_join("runtime-metrics.json"),FileAccess.WRITE)
		file.store_string(JSON.stringify(result,"\t"))
