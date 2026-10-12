extends SceneTree
func _initialize() -> void: call_deferred("capture")
func set_wind(node: Node, phase: float) -> void:
    if node is MultiMeshInstance3D:
        node.material_override.set_shader_parameter("wind_time_override",phase)
    for child in node.get_children(): set_wind(child,phase)
func capture() -> void:
    var scene: Node=load("res://demo.tscn").instantiate()
    root.add_child(scene)
    scene.set_view(3)
    for phase in [0.0,1.8,3.0]:
        set_wind(scene,phase)
        if phase==3.0: scene.get_node("Sun").rotation_degrees=Vector3(-22,150,0)
        await create_timer(.5).timeout
        await RenderingServer.frame_post_draw
        var error := root.get_texture().get_image().save_png("res://../validation/nature/realistic-v2/wind-%s.png"%str(phase))
        if error!=OK:
            push_error("GRASS_CAPTURE_FAILED")
            quit(1)
            return
    print("GRASS_LIGHT_WIND_CAPTURE_OK")
    quit()
