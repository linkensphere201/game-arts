extends SceneTree
## Local art-review runner: --path pixel-rpg-demo --script res://authoring/preview_side_motion.gd
var actors: Array[Sprite2D] = []
var elapsed := 0.0
var capture := ""
var captured := false

func _initialize():
    root.size = Vector2i(800, 480)
    root.content_scale_size = Vector2i(800, 480)
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture="):
            capture = arg.trim_prefix("--capture=")
    var scene := Node2D.new()
    scene.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    root.add_child(scene)
    var bg := Polygon2D.new()
    bg.polygon = PackedVector2Array([Vector2.ZERO,Vector2(800,0),Vector2(800,480),Vector2(0,480)])
    bg.color = Color("ded8ca")
    scene.add_child(bg)
    var heading := Label.new()
    heading.text = "LOCAL MODEL / SIDE MOTION STUDY — E ONLY"
    heading.position = Vector2(24,18)
    heading.modulate = Color("29333a")
    scene.add_child(heading)
    for i in range(2):
        var action: String = ["walk", "run"][i]
        var image_path := ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/motion/rowan-E-" + action + ".png")
        var image := Image.load_from_file(image_path)
        if image == null or image.get_size() != Vector2i(768,128):
            push_error("Run authoring/build_side_motion.py first: " + image_path)
            quit(1)
            return
        var shadow := Polygon2D.new()
        var points := PackedVector2Array()
        for n in range(32):
            var angle := TAU*n/32.0
            points.append(Vector2(cos(angle)*30,sin(angle)*7))
        shadow.polygon = points
        shadow.position = Vector2(220+i*360,390)
        shadow.color = Color(0.2,0.25,0.2,0.28)
        scene.add_child(shadow)
        var sprite := Sprite2D.new()
        sprite.texture = ImageTexture.create_from_image(image)
        sprite.hframes = 8
        sprite.centered = false
        sprite.scale = Vector2(2.5,2.5)
        sprite.position = shadow.position-Vector2(48,122)*2.5
        scene.add_child(sprite)
        actors.append(sprite)
        var label := Label.new()
        label.text = action.to_upper()+" / 8 frames"
        label.position = Vector2(160+i*360,420)
        label.modulate = Color("29333a")
        scene.add_child(label)

func _process(delta: float) -> bool:
    elapsed += delta
    for i in range(actors.size()):
        actors[i].frame = int(elapsed / [0.1,0.075][i]) % 8
    if not capture.is_empty() and elapsed > 1.0 and not captured:
        captured = true
        save_capture.call_deferred()
    return false

func save_capture():
    await RenderingServer.frame_post_draw
    var result := root.get_texture().get_image().save_png(capture)
    if result != OK:
        push_error("Motion capture failed")
        quit(1)
        return
    print("MODEL_SIDE_MOTION_CAPTURE_OK")
    quit()
