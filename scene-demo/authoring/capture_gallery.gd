extends SceneTree
func _initialize() -> void:
	call_deferred("capture")
func capture() -> void:
	var scene: Node = load("res://sunward_coast/scenes/gallery.tscn").instantiate()
	root.add_child(scene)
	await create_timer(3.0).timeout
	await RenderingServer.frame_post_draw
	var path := ProjectSettings.globalize_path("res://../validation/coast-release/gallery.png")
	assert(root.get_texture().get_image().save_png(path) == OK)
	print("GALLERY_CAPTURE_OK")
	quit()
