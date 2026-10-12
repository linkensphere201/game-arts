extends SceneTree
## Deterministic actual renderer capture: 64 time samples/s, moving world position.
func _initialize() -> void:
	call_deferred("review")

func review() -> void:
	root.size=Vector2i(640,600)
	root.content_scale_size=root.size
	var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/")
	var weight:=OS.get_cmdline_user_args().has("--weight")
	var phased:=OS.get_cmdline_user_args().has("--phased-arms")
	if phased:weight=true
	var output:=base+("weight-cycle/travel/" if weight else "support-cycle/travel/")
	if phased:output=base+"phased-cycle/travel/"
	var mkdir_error:=DirAccess.make_dir_recursive_absolute(output)
	if mkdir_error!=OK:quit(1);return
	var bg:=ColorRect.new();bg.size=Vector2(640,600);bg.color=Color("ded8ca");root.add_child(bg)
	for y in range(60,600,24):
		var line:=ColorRect.new();line.position=Vector2(0,y);line.size=Vector2(640,1)
		line.color=Color("b7b4a5");root.add_child(line)
	var sprites:Array[Sprite2D]=[]
	var descriptions=["Authored contacts / 8.33 fps", "Rigid boots / 16 fps"]
	if weight:descriptions=["Fixed torso / 16 fps", "Weight transfer / 16 fps"]
	if phased:descriptions=["Previous arm timing", "Phased arms + weight"]
	for index in range(2):
		var folder:String="contact-cycle" if index==0 else "support-cycle"
		if weight:folder="support-cycle" if index==0 else "weight-cycle"
		if phased:folder="weight-cycle" if index==0 else "phased-cycle"
		var image:=Image.load_from_file(base+folder+"/leg-poses.png")
		if image==null:quit(2);return
		var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(image)
		sprite.hframes=8;sprite.centered=false;sprite.scale=Vector2(3,3)
		sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sprite);sprites.append(sprite)
		var label:=Label.new();label.text=descriptions[index];label.position=Vector2(12+index*320,10)
		label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
	var samples:Array=[]
	for sample in range(64):
		var time:=sample/64.0
		for index in range(2):
			var fps:float=1000.0/120 if index==0 else 16.0
			if weight:fps=16.0
			sprites[index].frame=int(floor(time*fps))%8
			sprites[index].position=Vector2(16+index*320,30+time*65*3)
		await process_frame
		await RenderingServer.frame_post_draw
		var error:=root.get_texture().get_image().save_png(output+"frame-%03d.png"%sample)
		if error!=OK:quit(3);return
		samples.append({"time":time,"world_y":time*65,"original_frame":sprites[0].frame,"support_frame":sprites[1].frame})
	var file:=FileAccess.open(output+"samples.json",FileAccess.WRITE)
	if file==null:quit(4);return
	file.store_string(JSON.stringify(samples,"\t"));file.close()
	print("TRAVEL_CAPTURE_OK: 64 rendered moving-position samples at 65 px/s")
	quit()
