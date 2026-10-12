extends SceneTree
func _initialize()->void:call_deferred("review")
func review()->void:
    root.size=Vector2i(640,420);root.content_scale_size=root.size
    var bg:=ColorRect.new();bg.size=Vector2(640,420);bg.color=Color("bac4c5");root.add_child(bg)
    var poses:=["near-contact","near-flight","far-contact","far-flight"]
    var material:=OS.get_cmdline_user_args().has("--material")
    var middle:=OS.get_cmdline_user_args().has("--middle") or material
    var arms:=OS.get_cmdline_user_args().has("--arms") or middle
    var down:=OS.get_cmdline_user_args().has("--down") or arms
    var crossing:=OS.get_cmdline_user_args().has("--crossing")
    var expanded:=["near-contact","near-support","near-flight","far-contact","far-support","far-flight"]
    var complete:=["near-contact","near-down","near-support","near-flight","far-contact","far-down","far-support","far-flight"]
    var actors:Array[AnimatedSprite2D]=[]
    for i in range(2):
        var frames:=SpriteFrames.new();frames.set_animation_speed("default",16 if arms else (16 if i==1 else 12) if down else (12 if crossing and i==1 else 8))
        var sequence:Array=complete if arms else (complete if i==1 else expanded) if down else ((expanded if i==1 else poses) if crossing else (poses if i==1 else [poses[0],poses[0],poses[0],poses[0]]))
        for name in sequence:
            var im:=Image.load_from_file("res://mosslight/model_review/neris-east-run-leg-"+name+".png")
            assert(im!=null and im.get_size()==Vector2i(96,144))
            if down and (i==1 or arms):
                var sheet_name:=("neris-east-run-material.png" if i==1 else "neris-east-run-arm-middle.png") if material else ("neris-east-run-arm-middle.png" if i==1 else "neris-east-run-arm-phases.png") if middle else ("neris-east-run-arm-phases.png" if arms and i==1 else "neris-east-run-leg-weighted.png")
                var sheet:=Image.load_from_file(ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/"+sheet_name))
                assert(sheet.get_size()==Vector2i(768,144))
                im=sheet.get_region(Rect2i(complete.find(name)*96,0,96,144))
            frames.add_frame("default",ImageTexture.create_from_image(im))
        var shadow:=Polygon2D.new();var points:=PackedVector2Array()
        for n in range(32):points.append(Vector2(cos(TAU*n/32.0)*29,sin(TAU*n/32.0)*8))
        shadow.polygon=points;shadow.color=Color(0,0,0,.22);shadow.position=Vector2(160+i*320,309);root.add_child(shadow)
        var actor:=AnimatedSprite2D.new();actor.sprite_frames=frames;actor.centered=false;actor.scale=Vector2(2,2);actor.position=Vector2(64+i*320,65);actor.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(actor);actor.play();actors.append(actor)
        var label:=Label.new();label.text=(["Original run materials","Shared coat palette candidate"] if material else ["Two arm endpoints","With intermediate arms"] if middle else ["Fixed running arms","Two opposite arm endpoints"] if arms else ["Six leg-phase studies","Eight with compression"] if down else ["Four leg-phase studies","Six phases with crossing"] if crossing else ["Held run key pose","Four leg-phase studies"])[i];label.position=Vector2(20+i*320,20);label.add_theme_color_override("font_color",Color("303630"));root.add_child(label)
    var note:=Label.new();note.text="Study: arm in-betweens, art polish and foot travel still pending.";note.position=Vector2(12,380);note.add_theme_color_override("font_color",Color("303630"));root.add_child(note)
    var seen:Dictionary={};var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/")
    for i in range(48 if down else 24):
        await create_timer(0.04167 if down else 0.0833).timeout
        await RenderingServer.frame_post_draw
        seen[actors[1].frame]=true
        assert(root.get_texture().get_image().save_png(base+("neris-east-run-material-%02d.png" if material else "neris-east-run-middle-%02d.png" if middle else "neris-east-run-arms-%02d.png" if arms else "neris-east-run-down-%02d.png" if down else "neris-east-run-crossing-%02d.png" if crossing else "neris-east-run-legs-%02d.png")%i)==OK)
    assert(seen.size()==(8 if down else 6 if crossing else 4) and actors[1].is_playing())
    print("NERIS_RUN_LEGS_PLAYBACK_OK: all requested slots, fixed shadow; incomplete cycle")
    quit()
