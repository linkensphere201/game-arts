extends Node2D
## Project the existing model-derived door leaf around its left hinge.
## The frame stays fixed. This is a stylized 2D cutout, not a 3D reconstruction.
signal opened
const WIDTHS := [1.0, 0.94, 0.75, 0.50, 0.25, 0.08]
const FRAME_SECONDS := 0.10
var busy := false
var is_open := false
var elapsed := 0.0
var leaf: Sprite2D
var frame: Sprite2D

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var texture := load("res://mosslight/model_review/door.png") as Texture2D
	assert(texture.get_size() == Vector2(96, 144))
	frame = Sprite2D.new()
	frame.texture = texture
	frame.offset = Vector2(0, -68)
	add_child(frame)
	var aperture := Polygon2D.new()
	aperture.polygon = PackedVector2Array([Vector2(-32,-126), Vector2(32,-126), Vector2(32,-10), Vector2(-32,-10)])
	aperture.color = Color("202820")
	add_child(aperture)
	var atlas := AtlasTexture.new()
	atlas.atlas = texture
	atlas.region = Rect2(16, 14, 64, 116)
	leaf = Sprite2D.new()
	leaf.texture = atlas
	leaf.centered = false
	leaf.position = Vector2(-32, -126)
	add_child(leaf)
	reset_closed()

func reset_closed() -> void:
	busy = false
	is_open = false
	elapsed = 0
	leaf.scale.x = 1

func begin_open() -> bool:
	if busy or is_open:
		return false
	busy = true
	elapsed = 0
	return true

func _process(delta: float) -> void:
	if not busy:
		return
	elapsed += delta
	var index := mini(int(elapsed / FRAME_SECONDS), WIDTHS.size() - 1)
	leaf.scale.x = WIDTHS[index]
	if elapsed >= FRAME_SECONDS * WIDTHS.size():
		busy = false
		is_open = true
		opened.emit()
