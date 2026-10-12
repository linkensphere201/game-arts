extends SceneTree
## Validate and render the generated native SpriteFrames, not external PNG reads.
var capture := ""

func _initialize():
    root.size = Vector2i(1280,680)
    root.content_scale_size = Vector2i(1280,680)
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture="): capture = arg.trim_prefix("--capture=")
    var frames := load("res://mosslight/model_motion/rowan_study.tres") as SpriteFrames
    assert(frames!=null and frames.get_animation_names().size()==24)
    for animation in frames.get_animation_names():
        var count := 4 if animation.begins_with("idle_") else 8
        assert(frames.get_frame_count(animation)==count)
        for f in range(count):
            var texture := frames.get_frame_texture(animation,f) as AtlasTexture
            assert(texture!=null and texture.region.size==Vector2(96,144))
            assert(texture.atlas.get_size()==Vector2(96*count,144))
    var scene := Node2D.new()
    scene.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    root.add_child(scene)
    var bg := Polygon2D.new()
    bg.polygon = PackedVector2Array([Vector2.ZERO,Vector2(1280,0),Vector2(1280,680),Vector2(0,680)])
    bg.color = Color("ded8ca")
    scene.add_child(bg)
    for column in range(8):
        var direction: String = ["S","SE","E","NE","N","NW","W","SW"][column]
        for row in range(2):
            var animation := ("walk_" if row==0 else "run_")+direction
            assert(frames.has_animation(animation) and frames.get_frame_count(animation)==8)
            for f in range(8):
                var texture := frames.get_frame_texture(animation,f) as AtlasTexture
                assert(texture!=null and texture.region.size==Vector2(96,144))
                assert(texture.atlas.get_size()==Vector2(768,144))
            var foot := Vector2(80+160*column,285+320*row)
            var shadow := Polygon2D.new()
            var points := PackedVector2Array()
            for n in range(32): points.append(Vector2(cos(TAU*n/32.0)*26,sin(TAU*n/32.0)*7))
            shadow.polygon = points;shadow.position = foot;shadow.color = Color(.2,.25,.2,.28)
            scene.add_child(shadow)
            var sprite := AnimatedSprite2D.new()
            sprite.sprite_frames = frames
            sprite.offset = Vector2(0,-50)
            sprite.position = foot
            sprite.scale = Vector2(1.5,1.5)
            scene.add_child(sprite)
            sprite.play(animation)
            var label := Label.new()
            label.text = animation+" / STUDY"
            label.position = foot+Vector2(-68,36)
            label.modulate = Color("29333a")
            scene.add_child(label)
    print("NATIVE_SPRITEFRAMES_QA_OK: 24 clips, 128 movement frames + 32 idle timeline frames")
    if not capture.is_empty(): save_capture.call_deferred()

func save_capture():
    await create_timer(1.0).timeout
    await RenderingServer.frame_post_draw
    assert(root.get_texture().get_image().save_png(capture)==OK)
    print("UNIFIED_MOTION_CAPTURE_OK")
    quit()
