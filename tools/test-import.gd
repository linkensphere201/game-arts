extends SceneTree
func _initialize() -> void:
	call_deferred("check")
func check() -> void:
	var packed = load("res://characters/renamed/ember_imp.tscn")
	assert(packed is PackedScene)
	var actor = packed.instantiate()
	root.add_child(actor)
	assert(actor is AnimatedSprite2D)
	assert(actor.texture_filter == CanvasItem.TEXTURE_FILTER_NEAREST)
	assert(actor.offset == Vector2(0, -24))
	for name in [&"idle", &"walk"]:
		var count := 4 if name == &"idle" else 6
		assert(actor.sprite_frames.get_frame_count(name) == count)
		assert(actor.sprite_frames.get_animation_speed(name) == 8.0)
		assert(actor.sprite_frames.get_animation_loop(name))
		actor.play(name)
		await create_timer(0.2).timeout
		assert(actor.frame > 0)
	actor.pause()
	var held = actor.frame
	await create_timer(0.2).timeout
	assert(actor.frame == held)
	print("FRESH_IMPORT_PASS: relocated folder, 2 animations, 10 frames, playback and pause")
	quit()
