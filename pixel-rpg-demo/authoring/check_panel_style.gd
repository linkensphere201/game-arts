extends SceneTree
func _initialize() -> void:
	call_deferred("check")

func check() -> void:
	root.size=Vector2i(680,460)
	root.content_scale_size=root.size
	var background:=ColorRect.new()
	background.color=Color("ded8c7")
	background.size=Vector2(680,460)
	root.add_child(background)
	var style:=load("res://mosslight/model_ui/panel.tres") as StyleBoxTexture
	assert(style!=null and style.texture.get_size()==Vector2(96,96))
	var positions:=[Vector2(20,20),Vector2(180,20),Vector2(20,210)]
	var sizes:=[Vector2(120,80),Vector2(320,144),Vector2(600,200)]
	for i in range(3):
		var panel:=Panel.new()
		panel.position=positions[i];panel.size=sizes[i]
		panel.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		panel.add_theme_stylebox_override("panel",style)
		root.add_child(panel)
	await process_frame
	await RenderingServer.frame_post_draw
	var rendered:=root.get_texture().get_image()
	# All four rendered corners must be pixel-identical across different panel sizes.
	for corner in [Vector2.ZERO,Vector2(1,0),Vector2(0,1),Vector2.ONE]:
		var expected:PackedByteArray
		for i in range(3):
			var at:Vector2=positions[i]+(sizes[i]-Vector2(12,12))*corner
			var pixels:=rendered.get_region(Rect2i(at,Vector2i(12,12))).get_data()
			if i==0:expected=pixels
			else:assert(pixels==expected,"Corner warped when panel resized")
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture="):
			var result:=rendered.save_png(arg.trim_prefix("--capture="))
			assert(result==OK)
	print("PANEL_STYLE_QA_OK: three rendered sizes, four corners pixel-identical")
	quit()
