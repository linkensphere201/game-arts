extends SceneTree
## Playable review override. The shared eight-direction SpriteFrames are immutable.
var hero
var baseline:SpriteFrames
var candidate:SpriteFrames
var label:Label
var use_candidate:=true

func _initialize() -> void:
	call_deferred("start")

func start() -> void:
	var level=load("res://model_playable.tscn").instantiate()
	root.add_child(level)
	await physics_frame
	hero=level.hero
	for child in level.get_children():
		if child is Label and child!=level.state_label:child.hide()
	baseline=hero.sprite.sprite_frames
	candidate=baseline.duplicate(true)
	var source:="res://mosslight/model_motion/front_walk_candidate.png"
	if not FileAccess.file_exists(source):source="res://../production/pixel-rpg/model-wave-01/guided/phased-cycle/leg-poses.png"
	var image:=Image.load_from_file(ProjectSettings.globalize_path(source))
	if image==null or image.get_size()!=Vector2i(768,144):
		push_error("Build the phased front-walk study before opening this review.")
		quit(1);return
	var texture:=ImageTexture.create_from_image(image)
	candidate.clear("walk_S")
	candidate.set_animation_speed("walk_S",16)
	candidate.set_animation_loop("walk_S",true)
	for i in range(8):
		var atlas:=AtlasTexture.new();atlas.atlas=texture;atlas.region=Rect2(i*96,0,96,144)
		candidate.add_frame("walk_S",atlas)
	var canvas:=CanvasLayer.new();canvas.layer=30;root.add_child(canvas)
	var panel:=ColorRect.new();panel.position=Vector2(8,8);panel.size=Vector2(944,60)
	panel.color=Color(.07,.09,.10,.94);panel.mouse_filter=Control.MOUSE_FILTER_IGNORE;canvas.add_child(panel)
	label=Label.new();label.position=Vector2(16,10);canvas.add_child(label)
	apply_candidate()
	if OS.get_cmdline_user_args().has("--check"):await checks()

func _process(_delta:float) -> bool:
	if is_instance_valid(hero) and Input.is_physical_key_pressed(KEY_F6):
		if not hero.has_meta("toggle_held"):
			hero.set_meta("toggle_held",true);use_candidate=not use_candidate;apply_candidate()
	elif is_instance_valid(hero):hero.remove_meta("toggle_held")
	return false

func apply_candidate() -> void:
	var animation: StringName=hero.sprite.animation
	hero.sprite.sprite_frames=candidate if use_candidate else baseline
	hero.sprite.play(animation)
	label.text=("Front walk: candidate" if use_candidate else "Front walk: previous runtime")+" | F6 compare\nWASD/arrows move; Shift run. Only south WALK is replaced. Art study."

func tick(count:int) -> void:
	for i in range(count):await physics_frame

func checks() -> void:
	var baseline_fps:=baseline.get_animation_speed("walk_S")
	assert(candidate.get_frame_count("walk_S")==8)
	assert(candidate.get_animation_speed("walk_S")==16)
	hero.position=Vector2(430,310)
	Input.action_press("ui_down")
	await tick(4)
	assert(hero.sprite.animation=="walk_S" and hero.sprite.sprite_frames==candidate)
	assert(is_equal_approx(hero.velocity.length(),65))
	var seen:Dictionary={}
	for i in range(36):
		await tick(1);seen[hero.sprite.frame]=true
	assert(seen.size()==8)
	Input.action_release("ui_down")
	await tick(3)
	assert(hero.sprite.animation=="idle_S" and hero.velocity==Vector2.ZERO)
	var stop:Vector2=hero.position
	await tick(4);assert(hero.position.is_equal_approx(stop))
	Input.action_press("ui_down");await tick(3)
	assert(hero.sprite.animation=="walk_S")
	var toggle:=InputEventKey.new();toggle.physical_keycode=KEY_F6;toggle.pressed=true
	Input.parse_input_event(toggle);await tick(3)
	assert(hero.sprite.sprite_frames==baseline and baseline.get_animation_speed("walk_S")==baseline_fps)
	toggle.pressed=false;Input.parse_input_event(toggle);await tick(2)
	use_candidate=true;apply_candidate()
	Input.action_release("ui_down")
	hero.position=Vector2(50,420)
	Input.action_press("ui_left");await tick(20)
	assert(hero.position.x>=51 and hero.get_slide_collision_count()>0)
	assert(hero.sprite.animation=="walk_W")
	Input.action_release("ui_left")
	hero.position=Vector2(430,355)
	Input.action_press("ui_down");await tick(8)
	await RenderingServer.frame_post_draw
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture="):
			var error:=root.get_texture().get_image().save_png(arg.trim_prefix("--capture="))
			assert(error==OK)
	Input.action_release("ui_down")
	print("FRONT_WALK_PLAYABLE_OK: input, eight frames, stop/restart, comparison, wall collision; baseline unchanged")
	quit()
