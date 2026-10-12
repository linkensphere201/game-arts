extends SceneTree
## Static turnaround inspection only; does not assert animation or artistic acceptance.
func _initialize() -> void:
	call_deferred("review")

func review() -> void:
	root.size = Vector2i(1008, 510)
	root.content_scale_size = Vector2i(1008, 510)
	var background := ColorRect.new()
	background.color = Color("ded8c7")
	background.size = Vector2(1008, 510)
	root.add_child(background)
	for i in range(3):
		var path := "res://mosslight/model_review/sylva%s.png" % ["", "-back", "-side"][i]
		var texture := load(path) as Texture2D
		if texture == null or texture.get_size() != Vector2(96, 144):
			push_error("Missing or incorrect study texture: " + path)
			quit(1)
			return
		var sprite := Sprite2D.new()
		sprite.texture = texture
		sprite.centered = false
		sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		sprite.position = Vector2(30 + i * 336, 30)
		sprite.scale = Vector2(3, 3)
		root.add_child(sprite)
		var label := Label.new()
		label.text = ["Sylva / front", "Sylva / rear study", "Sylva / side study"][i]
		label.position = Vector2(30 + i * 336, 8)
		label.add_theme_color_override("font_color", Color("33352e"))
		root.add_child(label)
	var note := Label.new()
	note.text = "Static studies: head proportions, shoulder, cuffs and footwear still need consistency work."
	note.position = Vector2(30, 475)
	note.add_theme_color_override("font_color", Color("33352e"))
	root.add_child(note)
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture="):
			var error := root.get_texture().get_image().save_png(arg.trim_prefix("--capture="))
			if error != OK:
				push_error("Capture failed: " + str(error))
				quit(1)
				return
	print("SYLVA_STATIC_RENDER_OK: three 96x144 studies at integer nearest scale")
	quit(0)
