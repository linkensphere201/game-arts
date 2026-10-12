extends SceneTree
## Isolated local review; no changes to the default demo.
var actors: Array[Sprite2D] = []
var elapsed := 0.0
var capture := ""
var captured := false
var calibrated := false
var bounded := false

func _initialize():
    root.size = Vector2i(800,640)
    root.content_scale_size = Vector2i(800,640)
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture="): capture = arg.trim_prefix("--capture=")
        if arg=="--calibrated":calibrated=true
        if arg=="--bounded":
            calibrated=true;bounded=true
    var scene := Node2D.new()
    scene.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    root.add_child(scene)
    var bg := Polygon2D.new()
    bg.polygon = PackedVector2Array([Vector2.ZERO,Vector2(800,0),Vector2(800,640),Vector2(0,640)])
    bg.color = Color("ded8ca")
    scene.add_child(bg)
    for i in range(4):
        var direction: String = "S" if i<2 else "N"
        var action: String = "walk" if i%2==0 else "run"
        var folder:="bounded-axial" if bounded else "calibrated-axial" if calibrated else "axial-motion"
        var path := ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/"+folder+"/rowan-"+direction+"-"+action+".png")
        var image := Image.load_from_file(path)
        if image == null or image.get_size()!=Vector2i(768,128):
            push_error("Run build_axial_motion.py first: "+path)
            quit(1)
            return
        var foot := Vector2(220+360*(i%2),270+300*(i/2))
        var shadow := Polygon2D.new()
        var points := PackedVector2Array()
        for n in range(32): points.append(Vector2(cos(TAU*n/32.0)*28,sin(TAU*n/32.0)*7))
        shadow.polygon = points
        shadow.position = foot
        shadow.color = Color(.2,.25,.2,.28)
        scene.add_child(shadow)
        var sprite := Sprite2D.new()
        sprite.texture = ImageTexture.create_from_image(image)
        sprite.hframes = 8
        sprite.centered = false
        sprite.scale = Vector2(2,2)
        sprite.position = foot-Vector2(48,112)*2
        scene.add_child(sprite)
        actors.append(sprite)
        var label := Label.new()
        label.text = direction+" / "+action.to_upper()+" / STUDY"
        label.position = foot+Vector2(-95,25)
        label.modulate = Color("29333a")
        scene.add_child(label)

func _process(delta: float) -> bool:
    elapsed += delta
    for i in range(actors.size()):
        var duration:=(1.0/(16.0 if i%2==0 else 20.0)) if calibrated else (0.1 if i%2==0 else 0.075)
        actors[i].frame = int(elapsed / duration)%8
    if not capture.is_empty() and elapsed>1.0 and not captured:
        captured = true
        save_capture.call_deferred()
    return false

func save_capture():
    await RenderingServer.frame_post_draw
    if root.get_texture().get_image().save_png(capture)!=OK:
        push_error("Axial capture failed")
        quit(1)
        return
    print("MODEL_AXIAL_MOTION_CAPTURE_OK")
    quit()
