extends SceneTree
func _initialize()->void:call_deferred("review")
func review()->void:
    root.size=Vector2i(900,410);root.content_scale_size=root.size
    var bg:=ColorRect.new();bg.size=Vector2(900,410);bg.color=Color("bac4c5");root.add_child(bg)
    var names:=["idle","walk","run-before","run"]
    for i in range(4):
        var im:=Image.load_from_file("res://mosslight/model_review/neris-east-run-study-"+names[i]+".png")
        assert(im!=null and im.get_size()==Vector2i(96,144))
        var actor:=Sprite2D.new();actor.texture=ImageTexture.create_from_image(im);actor.centered=false;actor.scale=Vector2(2,2);actor.position=Vector2(20+i*220,60);actor.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(actor)
        var label:=Label.new();label.text="E "+names[i];label.position=Vector2(20+i*220,20);label.add_theme_color_override("font_color",Color("303630"));root.add_child(label)
    var note:=Label.new();note.text="Single run pose only. Garment details and complete cycle pending.";note.position=Vector2(20,370);note.add_theme_color_override("font_color",Color("303630"));root.add_child(note)
    await process_frame
    await RenderingServer.frame_post_draw
    assert(root.get_texture().get_image().save_png(ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/neris-east-run-godot.png"))==OK)
    print("NERIS_RUN_RENDER_OK: four static comparisons; not animation")
    quit()
