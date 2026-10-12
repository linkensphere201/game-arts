extends SceneTree
## Interactive static-art review. Never substitutes still frames for movement clips.
class ReviewInput extends Node:
	var handler: Callable
	func _input(event: InputEvent) -> void:
		handler.call(event)
const IDS := ["bren", "mira", "osric", "tovin", "neris"]
const NAMES := ["Bren / Dragonborn warrior", "Mira / Wolf apothecary", "Osric / Veteran swordsman", "Tovin / Goblin merchant", "Neris / Elf steward"]
const NOTES := [
	"Armor finish, ear shape and boot proportions differ between views.",
	"Tail, boots and side-view shading need consistency work.",
	"Sword details, boot silhouette and camera need consistency work.",
	"Rear hair, strap continuity, eye shape and trouser shading need work.",
	"Profile shading, collar color, bun detail and projection need consistency work."
]
var selected := 0
var zoom := 2
var dark := false
var images: Dictionary = {}
var figures: Array[Sprite2D] = []
var heading: Label
var notes: Label
var scale_label: Label
var background: ColorRect
var foreground_labels: Array[Label] = []
var character_buttons: Array[Button] = []
var zoom_buttons: Array[Button] = []

func _initialize() -> void:
	call_deferred("build")

func label_at(value: String, position: Vector2, size: int = 18) -> Label:
	var item := Label.new()
	item.text = value
	item.position = position
	item.add_theme_font_size_override("font_size", size)
	root.add_child(item)
	foreground_labels.append(item)
	return item

func button_at(value: String, position: Vector2, action: Callable) -> Button:
	var item := Button.new()
	item.text = value
	item.position = position
	item.custom_minimum_size = Vector2(100, 34)
	item.pressed.connect(action)
	root.add_child(item)
	return item

func build() -> void:
	root.size = Vector2i(1024, 700)
	root.content_scale_size = root.size
	root.title = "Mosslight / Character art review"
	var receiver := ReviewInput.new()
	receiver.handler = handle_input
	root.add_child(receiver)
	for id in IDS:
		for suffix in ["", "-back", "-side"]:
			var path: String = "res://mosslight/model_review/" + id + suffix + ".png"
			var pixels := Image.load_from_file(ProjectSettings.globalize_path(path))
			if pixels == null or pixels.get_size() != Vector2i(96, 144):
				push_error("Missing or invalid local study: " + path)
				quit(1)
				return
			if OS.get_cmdline_user_args().has("--check") and pixels.get_used_rect().end.y != 122:
				push_error("Study foot anchor is not 122: " + path)
				quit(1)
				return
			images[id + suffix] = ImageTexture.create_from_image(pixels)
	background = ColorRect.new()
	background.size = Vector2(1024, 700)
	root.add_child(background)
	heading = label_at("", Vector2(26, 16), 24)
	for i in range(IDS.size()):
		character_buttons.append(button_at(IDS[i].capitalize(), Vector2(26 + i * 105, 56), func(): select_character(i)))
	for i in range(3):
		zoom_buttons.append(button_at(str(i + 1) + "x", Vector2(560 + i * 105, 56), func(): set_zoom(i + 1)))
	button_at("Light / Dark", Vector2(880, 56), toggle_background)
	for i in range(3):
		label_at(["Front", "Rear", "Right side"][i], Vector2(64 + i * 320, 107))
		var line := ColorRect.new()
		line.position = Vector2(32 + i * 320, 560)
		line.size = Vector2(288, 1)
		line.color = Color("888471")
		root.add_child(line)
		var sprite := Sprite2D.new()
		sprite.centered = false
		sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(sprite)
		figures.append(sprite)
	scale_label = label_at("", Vector2(26, 586), 16)
	notes = label_at("", Vector2(26, 615), 17)
	label_at("Static studies only. Other headings and walk/run are incomplete.", Vector2(26, 644), 17)
	label_at("Left/Right: character   1/2/3: pixel zoom   B: background   Esc: close", Vector2(26, 672), 14)
	refresh()
	if OS.get_cmdline_user_args().has("--check"):
		await check_interactions()

func select_character(index: int) -> void:
	selected = posmod(index, IDS.size())
	refresh()

func set_zoom(value: int) -> void:
	zoom = clampi(value, 1, 3)
	refresh()

func toggle_background() -> void:
	dark = not dark
	refresh()

func refresh() -> void:
	heading.text = NAMES[selected]
	notes.text = NOTES[selected]
	scale_label.text = "%dx nearest-neighbor pixels | Shared foot baseline | No animation preview" % zoom
	background.color = Color("242a2a") if dark else Color("ded8c7")
	for item in foreground_labels:
		item.add_theme_color_override("font_color", Color("e5e2d5") if dark else Color("35372e"))
	for i in range(3):
		figures[i].texture = images[IDS[selected] + ["", "-back", "-side"][i]]
		figures[i].scale = Vector2(zoom, zoom)
		figures[i].position = Vector2(176 + i * 320 - 48 * zoom, 560 - 122 * zoom)
	for i in range(character_buttons.size()):
		character_buttons[i].disabled = i == selected
	for i in range(zoom_buttons.size()):
		zoom_buttons[i].disabled = i + 1 == zoom

func handle_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_LEFT: select_character(selected - 1)
			KEY_RIGHT: select_character(selected + 1)
			KEY_1: set_zoom(1)
			KEY_2: set_zoom(2)
			KEY_3: set_zoom(3)
			KEY_B: toggle_background()
			KEY_ESCAPE: quit()

func press_key(code: Key) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.pressed = true
	Input.parse_input_event(event)
	await process_frame
	var release := InputEventKey.new()
	release.keycode = code
	release.pressed = false
	Input.parse_input_event(release)
	await process_frame

func check_interactions() -> void:
	for i in range(IDS.size()):
		assert(selected == i)
		for sprite in figures:
			assert(sprite.texture != null)
			assert(sprite.position.y + 122 * sprite.scale.y == 560)
		await press_key(KEY_RIGHT)
	assert(selected == 0)
	await press_key(KEY_LEFT)
	assert(selected == IDS.size() - 1)
	for key in [KEY_1, KEY_2, KEY_3]:
		await press_key(key)
		assert(zoom == key - KEY_1 + 1)
	await press_key(KEY_B)
	assert(dark)
	# Exercise the same button signals used by mouse activation.
	character_buttons[1].pressed.emit()
	assert(selected == 1)
	zoom_buttons[1].pressed.emit()
	assert(zoom == 2)
	await press_key(KEY_B)
	select_character(IDS.size() - 1)
	await process_frame
	await RenderingServer.frame_post_draw
	var path := ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/roster-review-godot.png")
	var error := root.get_texture().get_image().save_png(path)
	assert(error == OK)
	print("ROSTER_REVIEW_OK: %d textures; character wrap, zoom, background and button signals" % images.size())
	quit()
