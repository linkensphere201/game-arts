extends Node2D
## Interactive model-art interior study; rectangular modular cutaway walls and model furniture.
@onready var root: Window = get_tree().root
var standalone_checks := true
var room: Node2D
var hero: CharacterBody2D
var sorted: Node2D
var table: Node2D
var door: Node2D
var chair: Node2D
var bed: Node2D

func _ready():
	call_deferred("build")

func obstacle(at: Vector2, size: Vector2) -> void:
	var body:=StaticBody2D.new()
	body.position=at
	var shape:=CollisionShape2D.new()
	var box:=RectangleShape2D.new()
	box.size=size
	shape.shape=box
	body.add_child(shape)
	room.add_child(body)

func build() -> void:
	root.size=Vector2i(960,720)
	root.content_scale_size=Vector2i(960,720)
	room=Node2D.new()
	room.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	add_child(room)
	var background:=ColorRect.new()
	background.color=Color("293932")
	background.size=Vector2(960,720)
	room.add_child(background)
	var shell=load("res://mosslight/timber_room.gd").new()
	shell.position=Vector2(96,240)
	room.add_child(shell)
	sorted=Node2D.new()
	sorted.y_sort_enabled=true
	room.add_child(sorted)
	for item in [["bookshelf",Vector2(280,365)],["table",Vector2(520,490)],["chair",Vector2(520,390)],["chair",Vector2(660,500)],["bed",Vector2(760,630)]]:
		var furniture:PackedScene=load("res://mosslight/furniture/"+item[0]+".tscn")
		var sprite:=furniture.instantiate() as Node2D
		sprite.position=item[1]
		sorted.add_child(sprite)
		if item[0]=="table":table=sprite
		if item[0]=="chair":chair=sprite
		if item[0]=="bed":bed=sprite
	door=load("res://mosslight/model_door.gd").new()
	door.position=Vector2(736,256)
	sorted.add_child(door)
	hero=load("res://mosslight/model_character.gd").new()
	hero.position=Vector2(480,610)
	sorted.add_child(hero)
	var label:=Label.new()
	label.position=Vector2(32,24)
	label.text="MOSSLIGHT / INTERIOR ART STUDY\nWASD / arrows: move   Shift: run\nModel furniture and timber room; exit at the wooden door"
	room.add_child(label)
	if standalone_checks and "--self-test" in OS.get_cmdline_user_args():await checks()

func checks() -> void:
	hero.automated=true
	hero.position=Vector2(520,535)
	hero.auto_direction=Vector2.UP
	for i in range(55):await get_tree().physics_frame
	assert(hero.position.y>=495 and hero.get_slide_collision_count()>0)
	assert(hero.position.y>table.position.y)
	hero.position=Vector2(520,425)
	hero.auto_direction=Vector2.DOWN
	for i in range(40):await get_tree().physics_frame
	assert(hero.position.y<=443 and hero.get_slide_collision_count()>0)
	assert(hero.position.y<table.position.y)
	hero.position=Vector2(280,404)
	hero.auto_direction=Vector2.UP
	for i in range(40):await get_tree().physics_frame
	assert(hero.position.y>=368 and hero.get_slide_collision_count()>0)
	# The spare chair exposes its full silhouette and both sorting sides.
	hero.position=Vector2(660,540)
	hero.auto_direction=Vector2.UP
	for i in range(40):await get_tree().physics_frame
	assert(hero.position.y>=507 and hero.position.y>chair.position.y and hero.get_slide_collision_count()>0)
	hero.position=Vector2(660,440)
	hero.auto_direction=Vector2.DOWN
	for i in range(40):await get_tree().physics_frame
	assert(hero.position.y<=469 and hero.position.y<chair.position.y and hero.get_slide_collision_count()>0)
	hero.position=Vector2(760,654)
	hero.auto_direction=Vector2.UP
	for i in range(30):await get_tree().physics_frame
	assert(hero.position.y>=633 and hero.position.y>bed.position.y and hero.get_slide_collision_count()>0)
	hero.position=Vector2(760,449)
	hero.auto_direction=Vector2.DOWN
	for i in range(40):await get_tree().physics_frame
	assert(hero.position.y<=479 and hero.position.y<bed.position.y and hero.get_slide_collision_count()>0)
	hero.position=Vector2(680,556)
	hero.auto_direction=Vector2.RIGHT
	for i in range(30):await get_tree().physics_frame
	assert(hero.position.x<=701 and hero.get_slide_collision_count()>0)
	hero.auto_direction=Vector2.ZERO
	hero.position=Vector2(420,580)
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture="):assert(root.get_texture().get_image().save_png(arg.trim_prefix("--capture="))==OK)
	print("FURNITURE_ROOM_QA_OK: table/chair/bed front-back, bed side and shelf collision, shared Y-sort")
	get_tree().quit()
