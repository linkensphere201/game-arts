extends SceneTree
## In-place lower-body transition experiment, not a locomotion animation.
func _initialize() -> void:
    call_deferred("review")
func review() -> void:
    root.size=Vector2i(640,420)
    root.content_scale_size=root.size
    var bg:=ColorRect.new()
    bg.size=Vector2(640,420);bg.color=Color("ded8c7");root.add_child(bg)
    var rear:=OS.get_cmdline_user_args().has("--rear")
    var color_stable:=OS.get_cmdline_user_args().has("--color-stable")
    var transitions:=OS.get_cmdline_user_args().has("--arm-transitions") or color_stable
    var arms:=OS.get_cmdline_user_args().has("--arms") or transitions
    var textures:Dictionary={}
    for pose in ["neutral","left","right","left-half","right-half","left-arm","right-arm","left-arm-half","right-arm-half"]:
        var path:=ProjectSettings.globalize_path("res://mosslight/model_review/neris-walk-"+("rear-" if rear else "")+pose+".png")
        var pixels:=Image.load_from_file(path)
        assert(pixels!=null and pixels.get_size()==Vector2i(96,144))
        textures[pose]=ImageTexture.create_from_image(pixels)
    if color_stable:
        for pose in ["left-arm","right-arm","left-arm-half","right-arm-half"]:
            var pixels:=Image.load_from_file(ProjectSettings.globalize_path("res://mosslight/model_review/neris-walk-"+pose+"-stable.png"))
            assert(pixels!=null and pixels.get_size()==Vector2i(96,144))
            textures[pose+"-stable"]=ImageTexture.create_from_image(pixels)
    var tracks:Array[AnimatedSprite2D]=[]
    var sequences:Array=[
        ["neutral","neutral","left","left","neutral","neutral","right","right"],
        ["neutral","left-half","left","left-half","neutral","right-half","right","right-half"]
    ]
    if arms:
        sequences[0]=sequences[1].duplicate()
        sequences[1]=["neutral","left-half","left-arm","left-half","neutral","right-half","right-arm","right-half"]
    if transitions:
        sequences[0]=sequences[1].duplicate()
        sequences[1]=["neutral","left-arm-half","left-arm","left-arm-half","neutral","right-arm-half","right-arm","right-arm-half"]
    if color_stable:
        sequences[0]=sequences[1].duplicate()
        for i in range(sequences[1].size()):
            if "arm" in sequences[1][i]:sequences[1][i]+="-stable"
    for index in range(2):
        var label:=Label.new()
        label.text=["Direct lift / held poses","With intermediate poses"][index]
        if arms:label.text=["Leg study / fixed arms","Opposing arm extremes"][index]
        if transitions:label.text=["Abrupt arm extremes","With arm transitions"][index]
        if color_stable:label.text=["Model colors per pose","Reference sleeve colors"][index]
        label.position=Vector2(30+index*320,20)
        label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
        var frames:=SpriteFrames.new()
        frames.set_animation_speed("default",8)
        frames.set_animation_loop("default",true)
        for pose in sequences[index]:frames.add_frame("default",textures[pose])
        var actor:=AnimatedSprite2D.new()
        actor.sprite_frames=frames;actor.centered=false;actor.scale=Vector2(2,2)
        actor.position=Vector2(64+index*320,68)
        actor.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
        root.add_child(actor);tracks.append(actor);actor.play()
    var note:=Label.new()
    note.text="In-place leg study only. Arm swing, contact and weight transfer are missing."
    if arms:note.text="Arm extremes study. Arm transitions, contact and weight transfer are missing."
    if transitions:note.text="In-place pose transitions. Contact, travel and weight transfer remain unfinished."
    if color_stable:note.text="Color-transfer study; same model silhouettes. Gait and art approval pending."
    note.position=Vector2(16,375)
    note.add_theme_color_override("font_color",Color("33352e"));root.add_child(note)
    var seen:Dictionary={}
    var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/")
    for i in range(24):
        await create_timer(0.0833).timeout
        await RenderingServer.frame_post_draw
        seen[tracks[1].frame]=true
        var error:=root.get_texture().get_image().save_png(base+("neris-rear-arm-%02d.png" if rear and transitions else "neris-rear-leg-%02d.png" if rear else "neris-arm-color-%02d.png" if color_stable else "neris-arm-transition-%02d.png" if transitions else ("neris-arm-preview-%02d.png" if arms else "neris-leg-preview-%02d.png")) % i)
        assert(error==OK)
    assert(seen.size()==8 and tracks[1].is_playing())
    print("NERIS_LEG_PREVIEW_OK: live playback visited all 8 slots; live pose comparison; not locomotion")
    quit()
