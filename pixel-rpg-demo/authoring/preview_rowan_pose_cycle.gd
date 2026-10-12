extends SceneTree
func _initialize() -> void:
	call_deferred("review")
func review() -> void:
	root.size=Vector2i(400,500);root.content_scale_size=root.size
	var arms:=OS.get_cmdline_user_args().has("--arms")
	var contact:=OS.get_cmdline_user_args().has("--contact")
	var support:=OS.get_cmdline_user_args().has("--support")
	var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/"+("support-cycle/" if support else "contact-cycle/" if contact else "coordinated-cycle/" if arms else "keypose-cycle/"))
	var bg:=ColorRect.new();bg.size=Vector2(400,500);bg.color=Color("ded8ca");root.add_child(bg)
	var image:=Image.load_from_file(base+"leg-poses.png");assert(image!=null and image.get_size()==Vector2i(768,144))
	var texture:=ImageTexture.create_from_image(image)
	var frames:=SpriteFrames.new();frames.add_animation("pose_review");frames.set_animation_speed("pose_review",1000.0/120)
	if support:frames.set_animation_speed("pose_review",16)
	for i in range(8):
		var atlas:=AtlasTexture.new();atlas.atlas=texture;atlas.region=Rect2(i*96,0,96,144);frames.add_frame("pose_review",atlas)
	var sprite:=AnimatedSprite2D.new();sprite.sprite_frames=frames;sprite.centered=false
	sprite.position=Vector2(56,35);sprite.scale=Vector2(3,3);sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(sprite);sprite.play("pose_review")
	var label:=Label.new();label.text="Contact + passing / study" if contact else "Arm/leg pose loop / study" if arms else "Leg-pose loop / not locomotion";label.position=Vector2(20,8)
	if support:label.text="Rigid boot / sampled stance study"
	label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
	var seen:Dictionary={}
	for i in range(110):
		await create_timer(.02).timeout
		seen[sprite.frame]=true
	assert(seen.size()==8)
	await RenderingServer.frame_post_draw
	var error:=root.get_texture().get_image().save_png(base+"godot-cycle.png");assert(error==OK)
	print("KEYPOSE_CYCLE_RENDER_OK: all eight timeline frames played")
	quit()
