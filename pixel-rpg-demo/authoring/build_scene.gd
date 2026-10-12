extends SceneTree
const DIRS=["S","SE","E","NE","N","NW","W","SW"]
func _initialize():call_deferred("build")
func own(node,owner_node):
    for child in node.get_children():
        child.owner=owner_node
        if child.scene_file_path.is_empty():own(child,owner_node)
func save_scene(node,path):
    own(node,node)
    var packed=PackedScene.new()
    var error=packed.pack(node)
    assert(error==OK)
    error=ResourceSaver.save(packed,path)
    assert(error==OK)
func collider(parent,size,at):
    var body=StaticBody2D.new()
    var shape=CollisionShape2D.new()
    var rect=RectangleShape2D.new();rect.size=size
    shape.shape=rect;body.position=at;body.add_child(shape);parent.add_child(body)
func build():
    var frames=SpriteFrames.new()
    frames.remove_animation("default")
    for action in ["idle","walk"]:
        var texture=load("res://mosslight/"+action+".png")
        var count=4 if action=="idle" else 6
        for row in range(8):
            var clip=action+"_"+DIRS[row]
            frames.add_animation(clip);frames.set_animation_speed(clip,4 if action=="idle" else 8)
            for column in range(count):
                var atlas=AtlasTexture.new();atlas.atlas=texture
                atlas.region=Rect2(column*48,row*64,48,64);frames.add_frame(clip,atlas)
    ResourceSaver.save(frames,"res://mosslight/hero_frames.tres")
    var actor=CharacterBody2D.new();actor.name="Hero";actor.set_script(load("res://mosslight/hero.gd"))
    var sprite=AnimatedSprite2D.new();sprite.name="Sprite";sprite.sprite_frames=frames;sprite.position=Vector2(0,-24)
    sprite.animation="idle_S";actor.add_child(sprite)
    var collision=CollisionShape2D.new();var capsule=CircleShape2D.new();capsule.radius=5;collision.shape=capsule
    actor.add_child(collision)
    save_scene(actor,"res://mosslight/hero.tscn");actor.free()
    var main=Node2D.new();main.name="MosslightSample";main.set_script(load("res://main.gd"))
    var tiles=TileSet.new();tiles.tile_size=Vector2i(32,32)
    var source=TileSetAtlasSource.new();source.texture=load("res://mosslight/terrain.png");source.texture_region_size=Vector2i(32,32)
    for x in range(4):source.create_tile(Vector2i(x,0))
    for mask in range(16):source.create_tile(Vector2i(mask%4,1+mask/4))
    tiles.add_source(source,0)
    ResourceSaver.save(tiles,"res://mosslight/terrain_tileset.tres")
    var floor_layer=TileMapLayer.new();floor_layer.name="Terrain";floor_layer.tile_set=tiles;main.add_child(floor_layer)
    for y in range(14):
        for x in range(20):
            floor_layer.set_cell(Vector2i(x,y),0,Vector2i([0,2,3][(x*17+y*7)%3],0))
            if x==10 or (y==8 and x>=4 and x<=16):
                var mask=0
                if x==10 or y==9:mask|=1
                if y==8 and x<16:mask|=2
                if x==10 or y==7:mask|=4
                if y==8 and x>4:mask|=8
                floor_layer.set_cell(Vector2i(x,y),0,Vector2i(mask%4,1+mask/4))
    var world=Node2D.new();world.name="World";world.y_sort_enabled=true;main.add_child(world)
    var names=["oak_tree","shrub","rock","wooden_crate","barrel","chest","signpost","wooden_fence","bench","well","lantern","flower_patch"]
    var positions=[Vector2(105,158),Vector2(190,167),Vector2(465,175),Vector2(427,332),Vector2(465,333),Vector2(390,214),Vector2(282,185),Vector2(167,336),Vector2(217,223),Vector2(516,259),Vector2(363,310),Vector2(252,345)]
    for i in range(names.size()):
        var prop=Sprite2D.new()
        prop.texture=load("res://mosslight/"+names[i]+("_animation" if names[i] in ["chest","lantern"] else "")+".png")
        prop.name="Chest" if names[i]=="chest" else ("Lantern" if names[i]=="lantern" else names[i])
        if names[i] in ["chest","lantern"]:prop.hframes=4
        prop.offset=Vector2(0,-40);prop.position=positions[i];world.add_child(prop)
        if names[i]!="flower_patch":collider(world,Vector2(22 if names[i]!="wooden_fence" else 64,10),positions[i]+Vector2(0,-5))
    var player=load("res://mosslight/hero.tscn").instantiate();player.name="Hero";player.position=Vector2(320,240);world.add_child(player)
    collider(main,Vector2(640,16),Vector2(320,36));collider(main,Vector2(640,16),Vector2(320,426))
    collider(main,Vector2(16,448),Vector2(8,224));collider(main,Vector2(16,448),Vector2(632,224))
    var hud=CanvasLayer.new();hud.name="HUD";main.add_child(hud)
    var panel=ColorRect.new();panel.color=Color("#252737");panel.size=Vector2(640,38);hud.add_child(panel)
    var title=Label.new();title.text="MOSSLIGHT JOURNEY  /  M5 ART SAMPLE";title.position=Vector2(14,5);title.add_theme_font_size_override("font_size",16);hud.add_child(title)
    var note=Label.new();note.name="Note";note.text="Arrows / WASD move in 8 directions | E opens nearby chest"
    note.position=Vector2(14,421);note.add_theme_font_size_override("font_size",13);hud.add_child(note)
    save_scene(main,"res://main.tscn")
    main.free()
    print("PIXEL_RPG_SCENE_BUILT")
    quit()
