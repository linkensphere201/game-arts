extends "res://authoring/build_theme_scene.gd"
func build():
    var data=JSON.parse_string(FileAccess.get_file_as_string("res://mosslight/modular/catalog.json"))
    for entry in data.presets:
        var frames=SpriteFrames.new();frames.remove_animation("default")
        for action in ["idle","walk","run"]:
            var count=int(data.animations[action].frames)
            var texture=load("res://mosslight/modular/"+entry.id+"_"+action+".png")
            for row in range(8):
                var clip=action+"_"+DIRS[row];frames.add_animation(clip);frames.set_animation_speed(clip,data.animations[action].fps)
                for col in range(count):
                    var atlas=AtlasTexture.new();atlas.atlas=texture;atlas.region=Rect2(col*48,row*64,48,64);frames.add_frame(clip,atlas)
        var error=ResourceSaver.save(frames,"res://mosslight/modular/"+entry.id+"_frames.tres");assert(error==OK)
        var actor=CharacterBody2D.new();actor.name=entry.name;actor.set_script(load("res://mosslight/modular_hero.gd"))
        var ground=add_image(actor,"res://mosslight/modular/shadow.png",Vector2(0,-24));ground.name="GroundShadow"
        var animated=AnimatedSprite2D.new();animated.name="Sprite";animated.sprite_frames=frames;animated.position=Vector2(0,-24);animated.animation="idle_S";actor.add_child(animated)
        var shape=CollisionShape2D.new();var circle=CircleShape2D.new();circle.radius=5;shape.shape=circle;actor.add_child(shape)
        save_scene(actor,"res://mosslight/modular/"+entry.id+".tscn");actor.free()
    var main=load("res://theme.tscn").instantiate();main.set_script(load("res://modular.gd"))
    var hero=main.get_node("World/Hero");hero.set_script(load("res://mosslight/modular_hero.gd"))
    var shadow_node=add_image(hero,"res://mosslight/modular/shadow.png",Vector2(0,-24));shadow_node.name="GroundShadow";hero.move_child(shadow_node,0);shadow_node.owner=main
    for child in main.get_node("World").get_children():
        if child is AnimatedSprite2D:child.free()
    for i in range(15):
        var actor=Node2D.new();actor.position=Vector2(45+(i%8)*76,285+(i/8)*86);main.get_node("World").add_child(actor)
        add_image(actor,"res://mosslight/modular/shadow.png",Vector2(0,-24))
        var sprite=AnimatedSprite2D.new();sprite.sprite_frames=load("res://mosslight/modular/"+data.presets[i+1].id+"_frames.tres")
        sprite.position=Vector2(0,-24);sprite.animation="idle_S";sprite.autoplay="idle_S";actor.add_child(sprite)
    main.get_node("HUD/Note").text="WASD move | SHIFT run | TAB cast | E chest"
    main.get_node("HUD/Note").add_theme_font_size_override("font_size",10)
    save_scene(main,"res://modular.tscn");main.free();print("MODULAR_SCENE_BUILT");quit()
