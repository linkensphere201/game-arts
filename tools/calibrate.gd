extends SceneTree

func _initialize() -> void:
	call_deferred("check")

func check() -> void:
	var sheet := Image.create(256, 64, false, Image.FORMAT_RGBA8)
	sheet.fill(Color.TRANSPARENT)
	for frame in range(4):
		sheet.fill_rect(Rect2i(frame * 64 + 20, 16, 24, 40), Color.from_hsv(frame / 4.0, 0.8, 1.0))
		for mark in range(frame + 1):
			sheet.fill_rect(Rect2i(frame * 64 + 22 + mark * 5, 24, 3, 3), Color.WHITE)
	assert(sheet.save_png("res://calibration.png") == OK)
	var texture := ImageTexture.create_from_image(sheet)
	var frames := SpriteFrames.new()
	frames.remove_animation("default")
	frames.add_animation("calibration")
	frames.set_animation_speed("calibration", 8)
	frames.set_animation_loop("calibration", true)
	for frame in range(4):
		var atlas := AtlasTexture.new()
		atlas.atlas = texture
		atlas.region = Rect2(frame * 64, 0, 64, 64)
		frames.add_frame("calibration", atlas)
	var sprite := AnimatedSprite2D.new()
	sprite.sprite_frames = frames
	sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sprite.offset = Vector2(0, -24)
	root.add_child(sprite)
	root.size = Vector2i(256, 256)
	sprite.position = Vector2(128, 180)
	sprite.scale = Vector2(3, 3)
	sprite.play("calibration")
	await create_timer(0.2).timeout
	assert(sprite.frame > 0, "Animation did not advance")
	assert(frames.get_frame_count("calibration") == 4)
	assert(sheet.get_pixel(0, 0).a == 0.0)
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://calibration-render.png")
	print("CALIBRATION_PASS: 4 atlas frames, transparent RGBA, 8 FPS, advancing playback")
	quit(0)
