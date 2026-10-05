extends Node2D

const CHARACTER = preload("res://ember_imp/ember_imp.tscn")
const INK := Color("edf0f8")
const MUTED := Color("8f9aaf")
const ACCENT := Color("ff815c")
var actor: AnimatedSprite2D
var native: AnimatedSprite2D
var state_label: Label
var frame_label: Label
var selected: StringName = &"idle"
var paused := false
var light_background := false
var elapsed := 0.0
var capture_path := ""
var self_test := false
var test_seconds := 2.2
var visited_frames: Dictionary = {}

func text(value: String, at: Vector2, size: int, color: Color = INK) -> Label:
	var label := Label.new()
	label.text = value
	label.position = at
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", color)
	add_child(label)
	return label

func button(value: String, at: Vector2, callback: Callable) -> Button:
	var control := Button.new()
	control.text = value
	control.position = at
	control.size = Vector2(284, 42)
	control.add_theme_font_size_override("font_size", 17)
	var style := StyleBoxFlat.new()
	style.bg_color = Color("253046")
	style.set_corner_radius_all(8)
	control.add_theme_stylebox_override("normal", style)
	control.pressed.connect(callback)
	add_child(control)
	return control

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture="):
			capture_path = arg.trim_prefix("--capture=")
		if arg.begins_with("--test-seconds="):
			test_seconds = maxf(2.2, float(arg.trim_prefix("--test-seconds=")))
		if arg == "--self-test":
			self_test = true
	var metadata = JSON.parse_string(FileAccess.get_file_as_string("res://ember_imp/character.json"))
	text("GAME ARTS  /  SPRITE LAB", Vector2(48, 28), 14, ACCENT)
	text(str(metadata.title).to_upper(), Vector2(45, 48), 42)
	text("A reusable character. A real Godot scene.", Vector2(48, 107), 17, MUTED)
	text("LIVE PREVIEW", Vector2(70, 175), 13, MUTED)
	text("5x / nearest", Vector2(650, 175), 13, MUTED)
	actor = CHARACTER.instantiate()
	actor.position = Vector2(420, 526)
	actor.scale = Vector2(5, 5)
	add_child(actor)
	native = CHARACTER.instantiate()
	native.position = Vector2(738, 544)
	add_child(native)
	text("1x", Vector2(728, 563), 12, MUTED)
	text("ANIMATION", Vector2(842, 181), 13, MUTED)
	state_label = text("IDLE", Vector2(840, 209), 30)
	frame_label = text("", Vector2(842, 250), 14, MUTED)
	button("Idle   /   4 frames", Vector2(842, 291), func(): choose(&"idle"))
	button("Walk   /   6 frames", Vector2(842, 341), func(): choose(&"walk"))
	button("Pause / resume", Vector2(842, 391), toggle_pause)
	button("Dark / light background", Vector2(842, 441), func(): light_background = not light_background; queue_redraw())
	text("Playback speed", Vector2(842, 501), 14, MUTED)
	var speed := HSlider.new()
	speed.position = Vector2(842, 530)
	speed.size = Vector2(284, 24)
	speed.min_value = 0.25
	speed.max_value = 2.0
	speed.step = 0.25
	speed.value = 1.0
	speed.value_changed.connect(func(value: float): actor.speed_scale = value; native.speed_scale = value)
	add_child(speed)
	text("Arrow keys: move   |   Space: pause", Vector2(70, 581), 14, MUTED)
	text("IDLE / 8 FPS", Vector2(48, 634), 12, MUTED)
	text("WALK / 8 FPS", Vector2(430, 634), 12, MUTED)
	for animation in [&"idle", &"walk"]:
		for i in range(actor.sprite_frames.get_frame_count(animation)):
			var thumb := Sprite2D.new()
			thumb.texture = actor.sprite_frames.get_frame_texture(animation, i)
			thumb.position = Vector2((80 if animation == &"idle" else 462) + i * 66, 696)
			add_child(thumb)
	choose(&"idle")
	if not capture_path.is_empty():
		await get_tree().process_frame
		await RenderingServer.frame_post_draw
		var error := get_viewport().get_texture().get_image().save_png(capture_path)
		print("CAPTURE_RESULT ", error)
		get_tree().quit(error)

func choose(animation: StringName) -> void:
	selected = animation
	paused = false
	actor.play(animation)
	native.play(animation)
	state_label.text = String(animation).to_upper()

func toggle_pause() -> void:
	paused = not paused
	if paused:
		actor.pause()
		native.pause()
	else:
		actor.play()
		native.play()

func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_SPACE:
		toggle_pause()

func _process(delta: float) -> void:
	elapsed += delta
	var direction := Input.get_axis("ui_left", "ui_right")
	if not paused:
		if direction != 0.0:
			actor.play(&"walk")
			native.play(&"walk")
			actor.flip_h = direction < 0.0
			native.flip_h = actor.flip_h
			actor.position.x = clampf(actor.position.x + direction * delta * 170, 200, 622)
		else:
			actor.play(selected)
			native.play(selected)
	frame_label.text = "Frame %02d / %02d  |  %.1f FPS" % [actor.frame + 1, actor.sprite_frames.get_frame_count(actor.animation), 8.0 * actor.speed_scale]
	if self_test:
		visited_frames[String(actor.animation) + str(actor.frame)] = true
		if elapsed > 1.0 and selected != &"walk":
			choose(&"walk")
		if elapsed > test_seconds:
			if visited_frames.size() != 10:
				push_error("Expected all 10 animation frames, observed %d" % visited_frames.size())
				get_tree().quit(1)
			else:
				print("DEMO_SELF_TEST_PASS: both animations advanced through all 10 frames")
				get_tree().quit(0)

func _draw() -> void:
	draw_rect(Rect2(48, 160, 744, 456), Color("121a29"))
	draw_rect(Rect2(816, 160, 336, 456), Color("151e30"))
	var base := Color("e6e4df") if light_background else Color("192437")
	draw_rect(Rect2(68, 214, 704, 354), base)
	for x in range(68, 772, 32):
		draw_line(Vector2(x, 214), Vector2(x, 568), Color(0.5, 0.6, 0.8, 0.08))
	for y in range(214, 568, 32):
		draw_line(Vector2(68, y), Vector2(772, y), Color(0.5, 0.6, 0.8, 0.08))
	draw_line(Vector2(100, 527), Vector2(680, 527), Color("596273"))
	draw_line(Vector2(420, 520), Vector2(420, 534), ACCENT)
	draw_rect(Rect2(48, 660, 280, 72), Color("151e30"))
	draw_rect(Rect2(430, 660, 412, 72), Color("151e30"))
