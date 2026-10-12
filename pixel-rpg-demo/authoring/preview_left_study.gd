extends SceneTree
func _initialize() -> void:
	call_deferred("review")
func review() -> void:
	var direction:="W"
	for arg in OS.get_cmdline_user_args():
		if arg=="--direction=NW":direction="NW"
		if arg=="--direction=SW":direction="SW"
	root.size=Vector2i(640,500);root.content_scale_size=root.size
	var background:=ColorRect.new()
	background.size=Vector2(640,500);background.color=Color("ded8c7")
	root.add_child(background)
	for i in range(2):
		var sprite:=Sprite2D.new()
		var path:="res://mosslight/model_motion/idle_"+direction+".png" if i==0 else "res://mosslight/model_review/"+("rowan-left" if direction=="W" else "rowan-"+direction)+".png"
		sprite.texture=ImageTexture.create_from_image(Image.load_from_file(ProjectSettings.globalize_path(path)))
		if i==0:sprite.hframes=4
		sprite.centered=false;sprite.position=Vector2(15+i*320,35)
		sprite.scale=Vector2(3,3);sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(sprite)
		var label:=Label.new()
		label.text="Current "+direction+" / gameplay" if i==0 else "New "+direction+" / redraw study"
		label.position=Vector2(15+i*320,8)
		label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
	await process_frame
	await RenderingServer.frame_post_draw
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture="):
			var error:=root.get_texture().get_image().save_png(arg.trim_prefix("--capture="))
			assert(error==OK)
	print("LEFT_STUDY_RENDER_OK: current gameplay compared with independent static study ",direction)
	quit()
