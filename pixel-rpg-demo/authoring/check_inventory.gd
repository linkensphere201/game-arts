extends SceneTree
func _initialize() -> void:
	call_deferred("check")

func check() -> void:
	root.size=Vector2i(440,350);root.content_scale_size=root.size
	var background:=ColorRect.new()
	background.size=Vector2(440,350);background.color=Color("ded8c7")
	root.add_child(background)
	var inventory=load("res://mosslight/model_inventory.gd").new()
	inventory.position=Vector2(20,20)
	root.add_child(inventory)
	for i in range(3):await process_frame
	assert(inventory.selected_id=="sword" and inventory.buttons.size()==14)
	# Select key with actual mouse press/release, then bread through keyboard focus.
	var button:Button=inventory.buttons[7]
	for pressed in [true,false]:
		var mouse:=InputEventMouseButton.new()
		mouse.position=button.get_global_rect().get_center();mouse.global_position=mouse.position
		mouse.button_index=MOUSE_BUTTON_LEFT;mouse.pressed=pressed
		Input.parse_input_event(mouse)
		await process_frame
		await process_frame
	assert(inventory.selected_id=="key" and inventory.details.text.begins_with("Key\n"))
	for index in [11,12,13]:
		for pressed in [true,false]:
			var mouse:=InputEventMouseButton.new()
			mouse.position=inventory.buttons[index].get_global_rect().get_center();mouse.global_position=mouse.position
			mouse.button_index=MOUSE_BUTTON_LEFT;mouse.pressed=pressed
			Input.parse_input_event(mouse)
			await process_frame
			await process_frame
		assert(inventory.selected_id==inventory.ITEMS[index][0])
		assert(inventory.details.text.begins_with(inventory.ITEMS[index][1]+"\n"))
	inventory.buttons[9].grab_focus()
	for pressed in [true,false]:
		var key:=InputEventKey.new()
		key.keycode=KEY_SPACE;key.physical_keycode=KEY_SPACE;key.pressed=pressed
		Input.parse_input_event(key)
		await process_frame
		await process_frame
	assert(inventory.selected_id=="bread" and inventory.details.text.begins_with("Bread\n"))
	var selected:=0
	for item in inventory.buttons:
		if item.button_pressed:selected+=1
		assert(inventory.get_global_rect().encloses(item.get_global_rect()),"Item extends outside panel")
	assert(selected==1)
	assert(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(inventory.get_global_rect()))
	var hero=load("res://mosslight/model_character.gd").new()
	hero.position=Vector2(100,270)
	root.add_child(hero);hero.hide()
	var start:Vector2=hero.position
	var right:=InputEventKey.new()
	right.keycode=KEY_RIGHT;right.physical_keycode=KEY_RIGHT;right.pressed=true
	Input.parse_input_event(right)
	for i in range(10):await physics_frame
	assert(hero.position==start,"UI navigation also moved the character")
	var escape:=InputEventKey.new()
	escape.keycode=KEY_ESCAPE;escape.physical_keycode=KEY_ESCAPE;escape.pressed=true
	Input.parse_input_event(escape)
	for i in range(10):await physics_frame
	assert(root.gui_get_focus_owner()==null and hero.position.x>start.x+3,"Escape did not return movement control")
	right.pressed=false;Input.parse_input_event(right)
	escape.pressed=false;Input.parse_input_event(escape)
	inventory.buttons[9].grab_focus()
	await RenderingServer.frame_post_draw
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture="):
			var error:=root.get_texture().get_image().save_png(arg.trim_prefix("--capture="))
			assert(error==OK)
	print("INVENTORY_QA_OK: mouse/key selection, descriptions, bounds, UI focus movement lock and Escape release")
	quit()
