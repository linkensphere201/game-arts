extends Node3D
var target := Vector3.ZERO
var distance := 9.0
var yaw := 0.0
var pitch := .7
var capture_dir := ""
var qa_seconds := 0.0
var elapsed := 0.0
var frame_ms: Array[float]=[]
var peak_draws := 0
var peak_primitives := 0
func _ready() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	var label := Label.new()
	label.position=Vector2(24,20)
	label.text="NATURE / SURFACE STUDY\n1 Compare  2 Ground  3 Grass  4/5 Tree styles  6 Bark | RMB orbit, wheel zoom, L light"
	label.add_theme_font_size_override("font_size",22)
	layer.add_child(label)
	set_view(1)
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="): capture_dir=arg.trim_prefix("--capture-dir=")
		if arg.begins_with("--qa-seconds="): qa_seconds=float(arg.trim_prefix("--qa-seconds="))
	if not capture_dir.is_empty(): capture()
func set_view(index: int) -> void:
	target=Vector3(0,0,0) if index==1 else Vector3(-2.5,0.06,0.7 if index==2 else -0.65)
	distance=6.2 if index==1 else (2.7 if index==2 else 1.7)
	pitch=.72 if index==1 else (.8 if index==2 else .3)
	for i in range(2): get_node("Caption"+str(i)).visible=index==1
	yaw=0
	if has_node("Tree0"):
		$Tree0.visible=index==1 or index==4 or index==6
		$Tree1.visible=index==1 or index==5
		if index==1:
			target=Vector3(0,1.9,0);distance=8.6;pitch=.30
		if index in [4,5]:
			target=Vector3(-3.3 if index==4 else 1.7,2.6,-.8);distance=6.4;pitch=.08
		if index==6:
			target=Vector3(-3.3,1.1,-.8);distance=1.15;pitch=.12
	update_camera()
func update_camera() -> void:
	$Camera.position=target+Vector3(sin(yaw)*cos(pitch),sin(pitch),cos(yaw)*cos(pitch))*distance
	$Camera.look_at(target)
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		if event.keycode==KEY_1: set_view(1)
		if event.keycode==KEY_2: set_view(2)
		if event.keycode==KEY_3: set_view(3)
		if event.keycode==KEY_4: set_view(4)
		if event.keycode==KEY_5: set_view(5)
		if event.keycode==KEY_6: set_view(6)
		if event.keycode==KEY_L: $Sun.rotation.y+=.5
	if event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
		yaw-=event.relative.x*.005
		pitch=clampf(pitch+event.relative.y*.005,.08,1.5)
		update_camera()
	if event is InputEventMouseButton and event.pressed:
		if event.button_index==MOUSE_BUTTON_WHEEL_UP: distance=maxf(.65,distance*.9)
		if event.button_index==MOUSE_BUTTON_WHEEL_DOWN: distance=minf(25,distance*1.1)
		update_camera()
func capture() -> void:
	for view in [1,2,3,4,5,6]:
		set_view(view)
		await get_tree().create_timer(2).timeout
		await RenderingServer.frame_post_draw
		# Release builds omit assert expressions: the save must execute independently.
		var error := get_viewport().get_texture().get_image().save_png(capture_dir.path_join("nature-%d.png"%view))
		if error!=OK:
			push_error("NATURE_CAPTURE_FAILED code="+str(error))
			get_tree().quit(1)
			return
	print("NATURE_CAPTURE_OK")
	if qa_seconds<=0: get_tree().quit()
func _process(delta: float) -> void:
	if qa_seconds<=0: return
	elapsed+=delta
	if elapsed>5:
		frame_ms.append(delta*1000)
		peak_draws=maxi(peak_draws,int(Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)))
		peak_primitives=maxi(peak_primitives,int(Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME)))
	if elapsed>=qa_seconds:
		frame_ms.sort()
		var total := 0.0
		for ms in frame_ms:total+=ms
		var result := {"seconds":elapsed,"mean_ms":total/frame_ms.size(),"p95_ms":frame_ms[int(frame_ms.size()*.95)],"samples":frame_ms.size(),"peak_draw_calls":peak_draws,"peak_primitives":peak_primitives,"gpu":RenderingServer.get_video_adapter_name(),"renderer":RenderingServer.get_current_rendering_method(),"logical_viewport":str(get_viewport().get_visible_rect().size)}
		if not capture_dir.is_empty():
			var file := FileAccess.open(capture_dir.path_join("metrics.json"),FileAccess.WRITE)
			file.store_string(JSON.stringify(result,"\t"))
		print("NATURE_RUNTIME_OK ",JSON.stringify(result))
		get_tree().quit()
