extends Node3D
var target := Vector3(0,.5,0)
var distance := 15.0
var yaw := 0.0
var pitch := .30
var capture_dir := ""
func _ready() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	var label := Label.new()
	label.position=Vector2(30,25)
	label.text="STONE / MATERIAL STUDY\n1 Realistic   2 Cartoon   3 Comparison   RMB drag: orbit   Wheel: zoom"
	label.add_theme_font_size_override("font_size",22)
	layer.add_child(label)
	set_view(3)
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="): capture_dir=arg.trim_prefix("--capture-dir=")
	if not capture_dir.is_empty(): capture()
func set_view(index: int) -> void:
	target=Vector3(1.7 if index==1 else 5.1,.6,0) if index!=3 else Vector3(0,.5,0)
	distance=3.0 if index!=3 else 7.8
	for i in range(4):
		get_node("Sample%d"%i).visible = index==3 or i==(2 if index==1 else 3)
		get_node("Caption%d"%i).visible = index==3
	yaw=.18 if index!=3 else 0.0
	pitch=.25 if index!=3 else .30
	update_camera()
func update_camera() -> void:
	$Camera.position=target+Vector3(sin(yaw)*cos(pitch),sin(pitch),cos(yaw)*cos(pitch))*distance
	$Camera.look_at(target)
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		if event.keycode==KEY_1: set_view(1)
		if event.keycode==KEY_2: set_view(2)
		if event.keycode==KEY_3: set_view(3)
	if event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
		yaw-=event.relative.x*.005
		pitch=clampf(pitch+event.relative.y*.005,-.05,1.3)
		update_camera()
	if event is InputEventMouseButton and event.pressed:
		if event.button_index==MOUSE_BUTTON_WHEEL_UP: distance=maxf(2,distance*.9)
		if event.button_index==MOUSE_BUTTON_WHEEL_DOWN: distance=minf(22,distance*1.1)
		update_camera()
func capture() -> void:
	for view in [3,1,2]:
		set_view(view)
		await get_tree().create_timer(2).timeout
		await RenderingServer.frame_post_draw
		assert(get_viewport().get_texture().get_image().save_png(capture_dir.path_join("stone-%d.png"%view))==OK)
	print("STONE_CAPTURE_OK")
	get_tree().quit()
