extends SceneTree
func _initialize() -> void:call_deferred("show_roster")
func show_roster() -> void:
	var back:=OS.get_cmdline_user_args().has("--back")
	var turnaround:=OS.get_cmdline_user_args().has("--turnaround")
	var mira:=OS.get_cmdline_user_args().has("--mira")
	var osric_turnaround:=OS.get_cmdline_user_args().has("--osric-turnaround")
	var osric_back:=OS.get_cmdline_user_args().has("--osric-back")
	var osric:=OS.get_cmdline_user_args().has("--osric")
	var tovin:=OS.get_cmdline_user_args().has("--tovin")
	var neris:=OS.get_cmdline_user_args().has("--neris")
	var neris_turnaround:=OS.get_cmdline_user_args().has("--neris-turnaround")
	var neris_diagonal:=OS.get_cmdline_user_args().has("--neris-diagonal")
	var neris_front_diagonal:=OS.get_cmdline_user_args().has("--neris-front-diagonal")
	var neris_west:=OS.get_cmdline_user_args().has("--neris-west")
	var neris_walk:=OS.get_cmdline_user_args().has("--neris-walk-poses")
	var neris_compact:=OS.get_cmdline_user_args().has("--neris-compact")
	var neris_east_stride:=OS.get_cmdline_user_args().has("--neris-east-stride")
	var neris_rear_walk:=OS.get_cmdline_user_args().has("--neris-rear-walk")
	var neris_contact:=OS.get_cmdline_user_args().has("--neris-contact")
	var neris_back:=OS.get_cmdline_user_args().has("--neris-back")
	var tovin_back:=OS.get_cmdline_user_args().has("--tovin-back")
	var tovin_turnaround:=OS.get_cmdline_user_args().has("--tovin-turnaround")
	var osric_sword:=OS.get_cmdline_user_args().has("--osric-sword")
	var mira_hair:=OS.get_cmdline_user_args().has("--mira-hair")
	var mira_turnaround:=OS.get_cmdline_user_args().has("--mira-turnaround")
	var mira_back:=OS.get_cmdline_user_args().has("--mira-back")
	root.size=Vector2i(660,380);root.content_scale_size=root.size
	var bg:=ColorRect.new();bg.size=Vector2(660,380);bg.color=Color("ded8c7");root.add_child(bg)
	for index in range(3):
		var name:String=["Rowan","Sylva","Bren"][index]
		var path:String=["res://mosslight/model_motion/idle_S.png","res://mosslight/model_review/sylva.png","res://mosslight/model_review/bren.png"][index]
		if back and index>0:
			name="Bren front" if index==1 else "Bren rear"
			path="res://mosslight/model_review/bren.png" if index==1 else "res://mosslight/model_review/bren-back.png"
		if turnaround:
			name=["Bren front","Bren rear","Bren side"][index]
			path="res://mosslight/model_review/"+["bren.png","bren-back.png","bren-side.png"][index]
		if mira and index>0:
			name="Bren" if index==1 else "Mira"
			path="res://mosslight/model_review/"+("bren.png" if index==1 else "mira.png")
		if mira_back and index>0:
			name="Mira front" if index==1 else "Mira rear"
			path="res://mosslight/model_review/"+("mira.png" if index==1 else "mira-back.png")
		if mira_turnaround:
			name=["Mira front","Mira rear","Mira side"][index]
			path="res://mosslight/model_review/"+["mira.png","mira-back.png","mira-side.png"][index]
		if mira_hair:
			name=["Mira front","Side baseline","Side broad shadows"][index]
			path="res://mosslight/model_review/"+["mira.png","mira-side.png","mira-side-locks.png"][index]
		if osric and index>0:
			name="Bren" if index==1 else "Osric"
			path="res://mosslight/model_review/"+("bren.png" if index==1 else "osric.png")
		if osric_back and index>0:
			name="Osric front" if index==1 else "Osric rear"
			path="res://mosslight/model_review/"+("osric.png" if index==1 else "osric-back.png")
		if osric_turnaround:
			name=["Osric front","Osric rear","Osric side"][index]
			path="res://mosslight/model_review/"+["osric.png","osric-back.png","osric-side.png"][index]
		if osric_sword:
			name=["Osric front","Side baseline","Sword candidate"][index]
			path="res://mosslight/model_review/"+["osric.png","osric-side.png","osric-side-sword.png"][index]
		if tovin and index>0:
			name="Osric" if index==1 else "Tovin"
			path="res://mosslight/model_review/"+("osric.png" if index==1 else "tovin.png")
		if tovin_back and index>0:
			name="Tovin front" if index==1 else "Tovin rear"
			path="res://mosslight/model_review/"+("tovin.png" if index==1 else "tovin-back.png")
		if tovin_turnaround:
			name=["Tovin front","Tovin rear","Tovin side"][index]
			path="res://mosslight/model_review/"+["tovin.png","tovin-back.png","tovin-side.png"][index]
		if neris and index>0:
			name="Mira" if index==1 else "Neris"
			path="res://mosslight/model_review/"+("mira.png" if index==1 else "neris.png")
		if neris_back and index>0:
			name="Neris front" if index==1 else "Neris rear"
			path="res://mosslight/model_review/"+("neris.png" if index==1 else "neris-back.png")
		if neris_turnaround:
			name=["Neris front","Neris rear","Neris side"][index]
			path="res://mosslight/model_review/"+["neris.png","neris-back.png","neris-side.png"][index]
		if neris_diagonal:
			name=["Neris rear","Neris NE study","Neris side"][index]
			path="res://mosslight/model_review/"+["neris-back.png","neris-NE.png","neris-side.png"][index]
		if neris_front_diagonal:
			name=["Neris front","Neris SE study","Neris side"][index]
			path="res://mosslight/model_review/"+["neris.png","neris-SE.png","neris-side.png"][index]
		if neris_west:
			name=["Neris west","Neris front","Neris east"][index]
			path="res://mosslight/model_review/"+["neris-W.png","neris.png","neris-side.png"][index]
		if neris_walk:
			name=["Neris standing","Left foot lift","Right foot lift"][index]
			path="res://mosslight/model_review/"+["neris-walk-neutral.png","neris-walk-left.png","neris-walk-right.png"][index]
		if neris_contact:
			name=["Left foot forward","Neris standing","Right foot forward"][index]
			path="res://mosslight/model_review/"+["neris-walk-contact-left.png","neris-walk-neutral.png","neris-walk-contact-right.png"][index]
		if neris_rear_walk:
			name=["Rear standing","Rear left lift","Rear right lift"][index]
			path="res://mosslight/model_review/"+["neris-walk-rear-neutral.png","neris-walk-rear-left.png","neris-walk-rear-right.png"][index]
		if neris_east_stride:
			name=["East standing","Near leg leading","Far leg leading"][index]
			path="res://mosslight/model_review/"+["neris-walk-east-neutral.png","neris-walk-east-near-contact.png","neris-walk-east-far-contact.png"][index]
		if neris_compact:
			name=["Long stride","Short stride / near","Short stride / far"][index]
			path="res://mosslight/model_review/"+["neris-walk-east-near-contact.png","neris-walk-east-near-compact.png","neris-walk-east-far-compact.png"][index]
		var image:=Image.load_from_file(ProjectSettings.globalize_path(path))
		if image==null:quit(1);return
		if index==0:image=image.get_region(Rect2i(0,0,96,144))
		var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(image)
		sprite.centered=false;sprite.position=Vector2(14+index*220,55);sprite.scale=Vector2(2,2)
		sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sprite)
		var label:=Label.new();label.text=name;label.position=Vector2(26+index*220,20)
		label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
	await process_frame
	await RenderingServer.frame_post_draw
	var target:="bren-back-godot.png" if back else "bren-godot.png"
	if turnaround:target="bren-turnaround-godot.png"
	if mira:target="mira-godot.png"
	if mira_back:target="mira-back-godot.png"
	if mira_turnaround:target="mira-turnaround-godot.png"
	if mira_hair:target="mira-hair-godot.png"
	if osric:target="osric-godot.png"
	if tovin:target="tovin-godot.png"
	if neris:target="neris-godot.png"
	if neris_turnaround:target="neris-turnaround-godot.png"
	if neris_diagonal:target="neris-diagonal-godot.png"
	if neris_front_diagonal:target="neris-front-diagonal-godot.png"
	if neris_west:target="neris-west-godot.png"
	if neris_walk:target="neris-walk-poses-godot.png"
	if neris_compact:target="neris-compact-godot.png"
	if neris_east_stride:target="neris-east-stride-godot.png"
	if neris_rear_walk:target="neris-rear-walk-godot.png"
	if neris_contact:target="neris-contact-godot.png"
	if neris_back:target="neris-back-godot.png"
	if tovin_back:target="tovin-back-godot.png"
	if tovin_turnaround:target="tovin-turnaround-godot.png"
	if osric_back:target="osric-back-godot.png"
	if osric_turnaround:target="osric-turnaround-godot.png"
	if osric_sword:target="osric-sword-godot.png"
	var error:=root.get_texture().get_image().save_png(ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/"+target))
	assert(error==OK)
	print("BREN_RENDER_OK: actual engine static roster comparison")
	quit()
