extends SceneTree
func _initialize()->void:call_deferred("review")
func review()->void:
    root.size=Vector2i(1000,720);root.content_scale_size=root.size
    var bg:=ColorRect.new();bg.size=Vector2(1000,720);bg.color=Color("bac4c5");root.add_child(bg)
    var names:=["S","SW","W","NW","N","NE","E","SE"]
    var paths:=["neris-stance/coordinated-weighted.png","neris-SW-travel/calibrated.png","neris-west-travel/calibrated.png","neris-NW-travel/calibrated.png","neris-rear-stance/coordinated-weighted.png","neris-NE-travel/calibrated.png","neris-east-compact-travel/calibrated.png","neris-SE-travel/calibrated.png"]
    var palette:=OS.get_cmdline_user_args().has("--palette")
    if palette:
        paths[2]="neris-coat-palette/W-walk.png"
        paths[6]="neris-coat-palette/E-walk.png"
    var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/")
    var actors:Array[AnimatedSprite2D]=[]
    var seen:Array=[]
    for i in range(8):
        var origin:=Vector2(29+(i%4)*250,40+(i/4)*350)
        var label:=Label.new();label.text=names[i]+" / 12 fps / 2x";label.position=origin-Vector2(0,27);label.add_theme_color_override("font_color",Color("303630"));root.add_child(label)
        var ground:=ColorRect.new();ground.position=origin+Vector2(0,244);ground.size=Vector2(192,1);ground.color=Color("879795");root.add_child(ground)
        var sheet:=Image.load_from_file(base+paths[i]);assert(sheet.get_size()==Vector2i(768,144))
        var frames:=SpriteFrames.new();frames.set_animation_speed("default",12)
        for n in range(8):frames.add_frame("default",ImageTexture.create_from_image(sheet.get_region(Rect2i(n*96,0,96,144))))
        var actor:=AnimatedSprite2D.new();actor.centered=false;actor.position=origin;actor.scale=Vector2(2,2);actor.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;actor.sprite_frames=frames;root.add_child(actor);actor.play();actors.append(actor);seen.append({})
    for tick in range(24):
        await create_timer(0.0833).timeout
        await RenderingServer.frame_post_draw
        for i in range(8):seen[i][actors[i].frame]=true
        assert(root.get_texture().get_image().save_png(base+("neris-walk-palette-gallery-%02d.png" if palette else "neris-walk-gallery-%02d.png")%tick)==OK)
    for i in range(8):assert(seen[i].size()==8 and actors[i].is_playing())
    print("NERIS_WALK_GALLERY_OK: all eight headings playing all eight slots at common scale; art review only")
    quit()
