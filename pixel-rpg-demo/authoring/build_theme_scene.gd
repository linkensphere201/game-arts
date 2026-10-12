extends "res://authoring/build_scene.gd"
const CAST=["rowan","sylva","bren","osric"]
func add_image(parent,path,at,offset=Vector2.ZERO):
    var node=Sprite2D.new();node.texture=load(path);node.position=at;node.offset=offset
    parent.add_child(node)
    return node
func build():
    for id in CAST:
        var frames=SpriteFrames.new();frames.remove_animation("default")
        for action in ["idle","walk"]:
            var texture=load("res://mosslight/theme/"+id+"_"+action+".png")
            var count=4 if action=="idle" else 6
            for row in range(8):
                var clip=action+"_"+DIRS[row]
                frames.add_animation(clip);frames.set_animation_speed(clip,4 if action=="idle" else 8)
                for column in range(count):
                    var atlas=AtlasTexture.new();atlas.atlas=texture;atlas.region=Rect2(column*48,row*64,48,64)
                    frames.add_frame(clip,atlas)
        assert(ResourceSaver.save(frames,"res://mosslight/theme/"+id+"_frames.tres")==OK)
    var main=Node2D.new();main.name="MosslightStreet";main.set_script(load("res://theme.gd"))
    add_image(main,"res://mosslight/theme/street_floor.png",Vector2(320,224))
    var world=Node2D.new();world.name="World";world.y_sort_enabled=true;main.add_child(world)
    add_image(world,"res://mosslight/theme/guild_shop.png",Vector2(137,235),Vector2(0,-80))
    collider(world,Vector2(174,83),Vector2(134,187))
    add_image(world,"res://mosslight/theme/apothecary_stall.png",Vector2(471,232),Vector2(0,-44))
    collider(world,Vector2(108,35),Vector2(471,211))
    var chest=add_image(world,"res://mosslight/chest_animation.png",Vector2(410,338),Vector2(0,-40));chest.name="Chest";chest.hframes=4
    collider(world,Vector2(40,12),Vector2(410,332))
    var lantern=add_image(world,"res://mosslight/lantern_animation.png",Vector2(239,321),Vector2(0,-40));lantern.name="Lantern";lantern.hframes=4
    collider(world,Vector2(8,8),Vector2(239,317))
    for i in range(3):
        var npc=AnimatedSprite2D.new();npc.sprite_frames=load("res://mosslight/theme/"+CAST[i+1]+"_frames.tres")
        npc.position=[Vector2(432,269),Vector2(200,269),Vector2(479,331)][i];npc.offset=Vector2(0,-24);npc.animation="idle_S";npc.autoplay="idle_S";world.add_child(npc)
    var hero=load("res://mosslight/hero.tscn").instantiate();hero.name="Hero";hero.position=Vector2(320,302);world.add_child(hero)
    collider(main,Vector2(640,12),Vector2(320,65));collider(main,Vector2(640,12),Vector2(320,395))
    collider(main,Vector2(12,448),Vector2(6,224));collider(main,Vector2(12,448),Vector2(634,224))
    var hud=CanvasLayer.new();hud.name="HUD";main.add_child(hud)
    var top=ColorRect.new();top.size=Vector2(640,59);top.color=Color("#252737");hud.add_child(top)
    var title=Label.new();title.text="MOSSLIGHT / GUILD STREET - STYLE STUDY";title.position=Vector2(14,5);title.add_theme_font_size_override("font_size",16);hud.add_child(title)
    var selected=Label.new();selected.name="Name";selected.position=Vector2(14,30);selected.add_theme_font_size_override("font_size",12);hud.add_child(selected)
    var bar=ColorRect.new();bar.position=Vector2(0,405);bar.size=Vector2(640,43);bar.color=Color("#252737");hud.add_child(bar)
    var note=Label.new();note.name="Note";note.text="WASD / arrows move | E chest";note.position=Vector2(10,418);note.add_theme_font_size_override("font_size",12);hud.add_child(note)
    var items=["potion","crystal","book","shield","sword","key"]
    for i in range(items.size()):
        var slot=ColorRect.new();slot.position=Vector2(364+i*44,411);slot.size=Vector2(34,32);slot.color=Color("#343a4e");hud.add_child(slot)
        add_image(hud,"res://mosslight/theme/item_"+items[i]+".png",Vector2(381+i*44,427))
    save_scene(main,"res://theme.tscn");main.free()
    print("THEME_SCENE_BUILT")
    quit()
