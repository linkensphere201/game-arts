extends SceneTree
## Two authored passing-pose candidates, not a finished animation cycle.
func _initialize() -> void:
	call_deferred("review")
func review() -> void:
	var arms:=OS.get_cmdline_user_args().has("--arms")
	root.size=Vector2i(640,500);root.content_scale_size=root.size
	var bg:=ColorRect.new();bg.size=Vector2(640,500);bg.color=Color("ded8ca");root.add_child(bg)
	for i in range(2):
		var seed:=(771007 if arms else 771003)+i
		var path:=ProjectSettings.globalize_path("res://mosslight/model_review/rowan-front-knee-"+str(seed)+".png")
		var image:=Image.load_from_file(path);assert(image!=null and image.get_size()==Vector2i(96,144))
		var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(image)
		sprite.centered=false;sprite.position=Vector2(15+i*320,35);sprite.scale=Vector2(3,3)
		sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sprite)
		var label:=Label.new();label.text="Raised right leg / study" if i==0 else "Raised left leg / study"
		label.position=Vector2(15+i*320,8);label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
	await process_frame
	await RenderingServer.frame_post_draw
	var path:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/"+("rowan-arm-keypose-pair.png" if arms else "rowan-keypose-pair.png"))
	var error:=root.get_texture().get_image().save_png(path);assert(error==OK)
	print("KEYPOSE_PAIR_RENDER_OK: two static candidates, not a complete animation")
	quit()
