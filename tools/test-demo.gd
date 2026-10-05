extends SceneTree
func _initialize() -> void:
	call_deferred("check")
func check() -> void:
	var scene = load("res://main.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	var buttons = scene.find_children("*", "Button", true, false)
	for button in buttons:
		if button.text.begins_with("Walk"):
			button.pressed.emit()
	await create_timer(0.2).timeout
	assert(scene.actor.animation == &"walk" and scene.actor.frame > 0)
	for button in buttons:
		if button.text.begins_with("Pause"):
			button.pressed.emit()
	var held = scene.actor.frame
	await create_timer(0.2).timeout
	assert(scene.paused and scene.actor.frame == held)
	for button in buttons:
		if button.text.begins_with("Pause"):
			button.pressed.emit()
		if button.text.begins_with("Dark"):
			button.pressed.emit()
	assert(scene.light_background)
	var sliders = scene.find_children("*", "HSlider", true, false)
	sliders[0].value = 1.5
	assert(scene.actor.speed_scale == 1.5 and scene.native.speed_scale == 1.5)
	var origin = scene.actor.position.x
	Input.action_press("ui_right")
	await create_timer(0.2).timeout
	Input.action_release("ui_right")
	assert(scene.actor.position.x > origin and not scene.actor.flip_h)
	Input.action_press("ui_left")
	await create_timer(0.2).timeout
	Input.action_release("ui_left")
	assert(scene.actor.flip_h)
	for button in buttons:
		if button.text.begins_with("Idle"):
			button.pressed.emit()
	await process_frame
	assert(scene.actor.animation == &"idle")
	print("DEMO_CONTROLS_PASS: action selection, pause, background, speed, movement, facing")
	quit()
