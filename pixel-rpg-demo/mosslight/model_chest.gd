extends Node2D
## Reusable model-derived chest. Physics footprint and reward survive visual state changes.
signal first_opened
var sprite: AnimatedSprite2D
var is_open := false
var busy := false
var claimed := false

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sprite = AnimatedSprite2D.new()
	sprite.sprite_frames = SpriteFrames.new()
	sprite.offset = Vector2(0, -28)
	var frames := sprite.sprite_frames
	for clip in ["closed", "open", "opening", "closing"]:
		frames.add_animation(clip)
		frames.set_animation_loop(clip, false)
		frames.set_animation_speed(clip, 7.5)
	var states := {"closed":["closed"], "open":["open"], "opening":["closed","half","open"], "closing":["open","half","closed"]}
	for clip in states:
		for pose in states[clip]:
			var texture := load("res://mosslight/model_chest/"+pose+".png") as Texture2D
			assert(texture != null and texture.get_size() == Vector2(64,64))
			frames.add_frame(clip, texture)
	add_child(sprite)
	sprite.play("closed")
	sprite.animation_finished.connect(_finished)
	var body := StaticBody2D.new()
	var shape := CollisionShape2D.new()
	var box := RectangleShape2D.new()
	box.size = Vector2(42,22)
	shape.shape = box
	shape.position = Vector2(0,-12)
	body.add_child(shape)
	add_child(body)

func interact() -> bool:
	if busy: return false
	busy = true
	sprite.play("closing" if is_open else "opening")
	return true

func _finished() -> void:
	if not busy: return
	is_open = sprite.animation == "opening"
	busy = false
	sprite.play("open" if is_open else "closed")
	if is_open and not claimed:
		claimed = true
		first_opened.emit()
