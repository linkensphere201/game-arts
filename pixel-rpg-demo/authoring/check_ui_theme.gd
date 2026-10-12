extends SceneTree
var activations:=0
func _initialize() -> void:
	call_deferred("check")

func key(pressed:bool) -> void:
	var event:=InputEventKey.new()
	event.keycode=KEY_SPACE
	event.physical_keycode=KEY_SPACE
	event.pressed=pressed
	Input.parse_input_event(event)
	await process_frame
	await process_frame

func mouse(at:Vector2, pressed:bool) -> void:
	var event:=InputEventMouseButton.new()
	event.position=at;event.global_position=at
	event.button_index=MOUSE_BUTTON_LEFT;event.pressed=pressed
	Input.parse_input_event(event)
	await process_frame
	await process_frame

func check() -> void:
	root.size=Vector2i(760,300)
	root.content_scale_size=root.size
	var background:=ColorRect.new()
	background.color=Color("ded8c7");background.size=Vector2(760,300)
	root.add_child(background)
	var theme:=load("res://mosslight/model_ui/theme.tres") as Theme
	assert(theme!=null)
	var buttons:Array[Button]=[]
	for i in range(4):
		var button:=Button.new()
		button.theme=theme;button.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		button.position=Vector2(30+(i%2)*360,40+floori(i/2.0)*115)
		button.size=Vector2(300,72)
		button.text=["Continue","Selected","Unavailable","Keyboard focus"][i]
		button.toggle_mode=i==1
		button.disabled=i==2
		button.pressed.connect(func():activations+=1)
		root.add_child(button);buttons.append(button)
	await process_frame
	# Real mouse input must activate the enabled toggle exactly once.
	await mouse(buttons[1].position+Vector2(60,35),true)
	await mouse(buttons[1].position+Vector2(60,35),false)
	assert(activations==1 and buttons[1].button_pressed)
	await mouse(buttons[2].position+Vector2(60,35),true)
	await mouse(buttons[2].position+Vector2(60,35),false)
	assert(activations==1,"Disabled button accepted a click")
	buttons[3].grab_focus()
	await key(true)
	await key(false)
	assert(activations==2 and buttons[3].has_focus(),"Keyboard activation/focus failed")
	assert(theme.get_stylebox("hover","Button")!=theme.get_stylebox("normal","Button"))
	var motion:=InputEventMouseMotion.new()
	motion.position=buttons[0].position+Vector2(60,35)
	motion.global_position=motion.position
	Input.parse_input_event(motion)
	await process_frame
	await process_frame
	assert(buttons[0].is_hovered(),"Mouse hover did not reach the button")
	await RenderingServer.frame_post_draw
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture="):
			var error:=root.get_texture().get_image().save_png(arg.trim_prefix("--capture="))
			assert(error==OK)
	print("UI_THEME_QA_OK: real mouse/keyboard activation, hover, toggle, disabled rejection and focus")
	quit()
