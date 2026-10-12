extends Node2D
## Retain both room instances; detach the inactive room so its collision leaves the world.
var outside: Node2D
var inside: Node2D
var indoors := false
var held := false
var initialized := false
var switching := false
var transitions := 0
var hint: Label
const DOOR := Vector2(294,666)
const EXIT := Vector2(736,268)
const INSIDE_SPAWN := Vector2(736,304)

func _ready() -> void:
	outside=load("res://model_courtyard.gd").new()
	outside.standalone_checks=false
	add_child(outside)
	inside=load("res://model_interior.gd").new()
	inside.standalone_checks=false
	add_child(inside)
	await get_tree().process_frame
	await get_tree().process_frame
	remove_child(inside)
	inside.position=Vector2(120,90)
	get_window().size=Vector2i(1200,900)
	get_window().content_scale_size=Vector2i(1200,900)
	var overlay:=CanvasLayer.new()
	add_child(overlay)
	hint=Label.new()
	hint.position=Vector2(32,865)
	overlay.add_child(hint)
	initialized=true
	if "--self-test" in OS.get_cmdline_user_args():await checks()

func _process(_delta: float) -> void:
	if not initialized or switching:return
	var current=inside if indoors else outside
	var portal:=EXIT if indoors else DOOR
	var near: bool=current.hero.position.distance_to(portal)<48
	hint.text=("E: leave guild" if indoors else "E: enter guild") if near else ("Exit: wooden door on the back wall" if indoors else "Entrance: guild front door")
	var pressed:=Input.is_physical_key_pressed(KEY_E)
	if pressed and not held and near:change_room.call_deferred()
	held=pressed

func change_room() -> void:
	if switching:return
	switching=true
	var previous=inside if indoors else outside
	if indoors:
		hint.text="Opening door..."
		inside.hero.set_physics_process(false)
		inside.hero.velocity=Vector2.ZERO
		var started:bool=inside.door.begin_open()
		if not started:
			inside.hero.set_physics_process(true)
			switching=false
			return
		await inside.door.opened
		# Present the final open pose before detaching the room.
		await RenderingServer.frame_post_draw
		inside.hero.set_physics_process(true)
	remove_child(previous)
	# PhysicsServer removes the exited room's bodies at the next physics synchronization.
	await get_tree().physics_frame
	await get_tree().physics_frame
	indoors=not indoors
	var current=inside if indoors else outside
	add_child(current)
	if indoors:inside.door.reset_closed()
	current.hero.position=INSIDE_SPAWN if indoors else Vector2(294,690)
	current.hero.velocity=Vector2.ZERO
	transitions+=1
	held=Input.is_physical_key_pressed(KEY_E)
	switching=false

func press_e() -> void:
	var event:=InputEventKey.new()
	event.physical_keycode=KEY_E
	event.pressed=true
	Input.parse_input_event(event)
	for i in range(4):await get_tree().physics_frame
	event=InputEventKey.new()
	event.physical_keycode=KEY_E
	Input.parse_input_event(event)
	for i in range(4):await get_tree().physics_frame

func capture_room(suffix: String) -> void:
	await RenderingServer.frame_post_draw
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture="):
			var path:=arg.trim_prefix("--capture=")
			assert(get_viewport().get_texture().get_image().save_png(path.get_basename()+suffix+".png")==OK)

func checks() -> void:
	outside.hero.automated=true
	inside.hero.automated=true
	assert(inside.room.get_parent()==inside)
	outside.chest.interact()
	await get_tree().create_timer(.5).timeout
	assert(outside.loot_count==1)
	outside.hero.position=Vector2(640,740)
	await press_e()
	assert(not indoors)
	for cycle in range(2):
		outside.hero.position=DOOR
		await press_e()
		assert(indoors and inside.is_inside_tree() and not outside.is_inside_tree())
		assert(inside.hero.position.distance_to(INSIDE_SPAWN)<1)
		assert(not inside.door.is_open and inside.door.leaf.scale.x==1)
		inside.hero.auto_direction=Vector2.RIGHT
		for i in range(10):await get_tree().physics_frame
		assert(inside.hero.position.x>INSIDE_SPAWN.x+5 and inside.hero.get_slide_collision_count()==0)
		inside.hero.auto_direction=Vector2.ZERO
		if cycle==0:await capture_room("-inside")
		inside.hero.position=EXIT
		var before:int=transitions
		await press_e()
		assert(indoors and switching and inside.door.busy)
		assert(not inside.hero.is_physics_processing())
		assert(not inside.door.begin_open())
		await press_e() # Repeated input must not restart or queue another transition.
		assert(transitions==before and indoors)
		assert(inside.door.leaf.scale.x<1 and inside.door.frame.scale==Vector2.ONE)
		if cycle==0:await capture_room("-door-opening")
		for tick in range(90):
			if not switching:break
			await get_tree().physics_frame
		assert(not indoors and outside.is_inside_tree() and not inside.is_inside_tree())
		assert(transitions==before+1 and inside.door.is_open and inside.hero.is_physics_processing())
		assert(outside.hero.position.distance_to(Vector2(294,690))<1)
		assert(outside.loot_count==1 and outside.chest.claimed and outside.chest.is_open)
	await capture_room("-outside")
	print("WORLD_LINK_QA_OK: live E, animated door and repeated-input guard, two round trips, safe entry/return, retained reward")
	get_tree().quit()

func _exit_tree() -> void:
	# Detached rooms are still owned by this demo; free memory when the demo closes.
	if is_instance_valid(inside) and inside.get_parent()==null:inside.free()
	if is_instance_valid(outside) and outside.get_parent()==null:outside.free()
