extends SceneTree
func _initialize()->void:call_deferred("review")
func review()->void:
    root.size=Vector2i(640,420);root.content_scale_size=root.size
    var bg:=ColorRect.new();bg.size=Vector2(640,420);bg.color=Color("bac4c5");root.add_child(bg)
    var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/")
    var sheet:=Image.load_from_file(base+"neris-west-run-leg-weighted.png")
    assert(sheet.get_size()==Vector2i(768,144))
    var arms:=OS.get_cmdline_user_args().has("--arms")
    var actors:Array[AnimatedSprite2D]=[]
    for i in range(2):
        var frames:=SpriteFrames.new();frames.set_animation_speed("default",16)
        var selected:=Image.load_from_file(base+"neris-west-run-arm-middle.png") if arms and i==1 else sheet
        assert(selected.get_size()==Vector2i(768,144))
        for n in range(8):frames.add_frame("default",ImageTexture.create_from_image(selected.get_region(Rect2i((n if i==1 or arms else 0)*96,0,96,144))))
        var shadow:=Polygon2D.new();var points:=PackedVector2Array()
        for n in range(32):points.append(Vector2(cos(TAU*n/32.0)*29,sin(TAU*n/32.0)*8))
        shadow.polygon=points;shadow.color=Color(0,0,0,.22);shadow.position=Vector2(160+i*320,309);root.add_child(shadow)
        var actor:=AnimatedSprite2D.new();actor.sprite_frames=frames;actor.centered=false;actor.scale=Vector2(2,2);actor.position=Vector2(64+i*320,65);actor.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(actor);actor.play();actors.append(actor)
        var label:=Label.new();label.text=(["West fixed arms","West three arm poses"] if arms else ["West held key pose","West eight leg phases"])[i];label.position=Vector2(20+i*320,20);label.add_theme_color_override("font_color",Color("303630"));root.add_child(label)
    var note:=Label.new();note.text="Study: garment polish and travel calibration pending.";note.position=Vector2(12,380);note.add_theme_color_override("font_color",Color("303630"));root.add_child(note)
    var seen:Dictionary={}
    for i in range(48):
        await create_timer(0.04167).timeout
        await RenderingServer.frame_post_draw
        seen[actors[1].frame]=true
        assert(root.get_texture().get_image().save_png(base+("neris-west-run-arms-%02d.png" if arms else "neris-west-run-legs-%02d.png")%i)==OK)
    assert(seen.size()==8 and actors[1].is_playing())
    print("NERIS_WEST_RUN_PLAYBACK_OK: eight leg slots, fixed shadow; arms and travel incomplete")
    quit()
