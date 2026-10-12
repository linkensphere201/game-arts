extends SceneTree
func _initialize() -> void:
	call_deferred("review")
func review() -> void:
	root.size=Vector2i(640,500);root.content_scale_size=root.size
	var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/left-motion/")
	var background:=ColorRect.new()
	background.size=Vector2(640,500);background.color=Color("ded8ca");root.add_child(background)
	var sprites:Array[AnimatedSprite2D]=[]
	for i in range(2):
		var action:="walk" if i==0 else "run"
		var image:=Image.load_from_file(base+action+"_W.png")
		assert(image!=null and image.get_size()==Vector2i(768,144))
		var texture:=ImageTexture.create_from_image(image)
		var frames:=SpriteFrames.new();frames.add_animation(action)
		frames.set_animation_speed(action,10.0 if i==0 else 13.333333)
		for f in range(8):
			var atlas:=AtlasTexture.new();atlas.atlas=texture;atlas.region=Rect2(f*96,0,96,144)
			frames.add_frame(action,atlas)
		var sprite:=AnimatedSprite2D.new();sprite.sprite_frames=frames
		sprite.centered=false;sprite.position=Vector2(15+i*320,35);sprite.scale=Vector2(3,3)
		sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(sprite);sprite.play(action);sprites.append(sprite)
		var label:=Label.new();label.text="Independent W / "+action
		label.position=Vector2(15+i*320,8);label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
	var seen:Array[Dictionary]=[{},{}]
	for tick in range(140):
		await create_timer(0.02).timeout
		for i in range(2):seen[i][sprites[i].frame]=true
	assert(seen[0].size()==8 and seen[1].size()==8)
	await RenderingServer.frame_post_draw
	var error:=root.get_texture().get_image().save_png(base+"godot-left-motion.png")
	assert(error==OK)
	print("LEFT_MOTION_RENDER_OK: actual walk/run playback visited all 16 frames")
	quit()
