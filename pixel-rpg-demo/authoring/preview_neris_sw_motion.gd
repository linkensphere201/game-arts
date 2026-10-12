extends SceneTree
func _initialize()->void:call_deferred("review")
func review()->void:
    root.size=Vector2i(640,420);root.content_scale_size=root.size
    var bg:=ColorRect.new();bg.size=Vector2(640,420);bg.color=Color("ded8c7");root.add_child(bg)
    var transitions:=OS.get_cmdline_user_args().has("--transitions")
    var two_arms:=OS.get_cmdline_user_args().has("--two-arms") or transitions
    var arms:=OS.get_cmdline_user_args().has("--arms") or two_arms
    var poses:Dictionary={}
    for name in ["near-contact","far-contact","near-passing","far-passing","near-arm","far-arm","near-arm-half","far-arm-half","near-twoarm","far-twoarm","near-twoarm-half","far-twoarm-half"]:
        var im:=Image.load_from_file("res://mosslight/model_review/neris-walk-SW-"+name+".png")
        assert(im!=null and im.get_size()==Vector2i(96,144))
        poses[name]=ImageTexture.create_from_image(im)
    var sequences:Array=[
        ["near-contact","near-contact","near-contact","near-contact","far-contact","far-contact","far-contact","far-contact"],
        ["near-contact","near-contact","near-passing","near-passing","far-contact","far-contact","far-passing","far-passing"]]
    if arms:
        sequences[0]=sequences[1].duplicate()
        sequences[1]=["near-arm","near-arm-half","near-passing","far-arm-half","far-arm","far-arm-half","far-passing","near-arm-half"]
    if two_arms:
        sequences[0]=sequences[1].duplicate()
        sequences[1]=["near-twoarm","near-twoarm-half","near-passing","far-twoarm-half","far-twoarm","far-twoarm-half","far-passing","near-twoarm-half"]
    if transitions:
        sequences[0]=sequences[1].duplicate()
        sequences[1]=[]
        var sheet:=Image.load_from_file(ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/neris-SW-complete-phase-study.png"))
        assert(sheet.get_size()==Vector2i(768,144))
        for n in range(8):
            var key:="phase%d"%n
            poses[key]=ImageTexture.create_from_image(sheet.get_region(Rect2i(n*96,0,96,144)))
            sequences[1].append(key)
    var actors:Array[AnimatedSprite2D]=[]
    for i in range(2):
        var label:=Label.new();label.text=(["Held passing legs","SW leg transitions"] if transitions else ["SW near arm only","SW both arms"] if two_arms else ["SW fixed arm","SW near-arm phases"] if arms else ["SW contacts only","SW contact + passing"])[i];label.position=Vector2(20+i*320,20);label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
        var frames:=SpriteFrames.new();frames.set_animation_speed("default",8)
        for name in sequences[i]:frames.add_frame("default",poses[name])
        var actor:=AnimatedSprite2D.new();actor.sprite_frames=frames;actor.centered=false;actor.scale=Vector2(2,2);actor.position=Vector2(64+i*320,65);actor.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(actor);actor.play();actors.append(actor)
    var note:=Label.new();note.text="Side leg study: arms, timing, ground lock and art consistency unfinished.";note.position=Vector2(12,380);note.add_theme_color_override("font_color",Color("33352e"));root.add_child(note)
    var seen:Dictionary={}
    var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/")
    for i in range(24):
        await create_timer(0.0833).timeout
        await RenderingServer.frame_post_draw
        seen[actors[1].frame]=true
        assert(root.get_texture().get_image().save_png(base+("neris-SW-transition-%02d.png" if transitions else "neris-SW-twoarm-%02d.png" if two_arms else "neris-SW-arm-%02d.png" if arms else "neris-SW-leg-%02d.png")%i)==OK)
    assert(seen.size()==8 and actors[1].is_playing())
    print("NERIS_SW_PLAYBACK_OK: contact/passing live comparison, all eight slots; not locomotion")
    quit()
