extends Node2D
## Model-derived building/character/prop scale and occlusion review.
var hero: CharacterBody2D
var sorted: Node2D
var guild: Sprite2D
var tree: Sprite2D
var capture := ""
var chest: Node2D
var loot_count := 0
var interaction_label: Label
var interact_held := false
var shadows: Node2D
var standalone_checks := true

func contact_shadow(at: Vector2, radius: Vector2) -> Node2D:
    var shadow=load("res://mosslight/contact_shadow.gd").new()
    shadow.position=at
    shadow.half_size=radius
    shadows.add_child(shadow)
    return shadow

func obstacle(at: Vector2, size: Vector2):
    var body := StaticBody2D.new()
    body.position = at
    var shape := CollisionShape2D.new()
    var box := RectangleShape2D.new()
    box.size = size
    shape.shape = box
    body.add_child(shape)
    add_child(body)

func prop(id: String, foot: Vector2, scale_factor: float) -> Sprite2D:
    var sprite := Sprite2D.new()
    sprite.texture = load("res://mosslight/model_review/"+id+".png")
    assert(sprite.texture!=null)
    sprite.position=foot
    sprite.offset.y=-sprite.texture.get_height()/2.0+4
    sprite.scale=Vector2.ONE*scale_factor
    sorted.add_child(sprite)
    if id!="guild":
        var radius := Vector2(sprite.texture.get_width()*.35, sprite.texture.get_width()*.09)*scale_factor
        if id=="tree":radius=Vector2(34,9)
        contact_shadow(foot+Vector2(0,-4*scale_factor),radius)
    return sprite

func _ready():
    get_window().size=Vector2i(1200,900)
    get_window().content_scale_size=Vector2i(1200,900)
    texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
    var grass := TextureRect.new()
    grass.texture=load("res://mosslight/model_ground/grass.png")
    assert(grass.texture!=null)
    grass.position=Vector2(44,124)
    grass.size=Vector2(1112,720)
    grass.stretch_mode=TextureRect.STRETCH_TILE
    grass.mouse_filter=Control.MOUSE_FILTER_IGNORE
    add_child(grass)
    var paving = load("res://mosslight/paving_layer.gd").new()
    paving.position=Vector2(44,124)
    add_child(paving)
    var vertices := {}
    for y in range(17,21):
        for x in range(6,28):vertices[Vector2i(x,y)]=true
    # A short branch tests concave corners as well as the outer rounded boundary.
    for y in range(14,18):
        for x in range(21,24):vertices[Vector2i(x,y)]=true
    paving.paint_vertices(vertices,Rect2i(4,12,26,10))
    assert(paving.get_used_cells().size()==260)
    shadows=Node2D.new()
    add_child(shadows)
    sorted=Node2D.new()
    sorted.y_sort_enabled=true
    add_child(sorted)
    tree=prop("tree",Vector2(1020,520),1)
    prop("rock",Vector2(938,566),1)
    obstacle(Vector2(1020,508),Vector2(24,20))
    obstacle(Vector2(938,550),Vector2(46,24))
    guild=prop("guild",Vector2(340,650),1.5)
    # Sort at the wall contact line, not the decorative paving edge.
    guild.position.y-=10
    guild.offset.y+=10.0/1.5
    chest=load("res://mosslight/model_chest.gd").new()
    chest.position=Vector2(800,640)
    chest.first_opened.connect(func(): loot_count+=1)
    sorted.add_child(chest)
    contact_shadow(chest.position+Vector2(0,-4),Vector2(25,7))
    prop("barrel",Vector2(610,620),1)
    prop("barrel",Vector2(650,635),1)
    obstacle(Vector2(610,609),Vector2(34,20))
    obstacle(Vector2(650,624),Vector2(34,20))
    prop("crate",Vector2(705,629),1)
    obstacle(Vector2(705,617),Vector2(42,22))
    # Ground footprint only: roof pixels must not become a tall collision rectangle.
    obstacle(Vector2(340,608),Vector2(400,64))
    obstacle(Vector2(600,112),Vector2(1120,24))
    obstacle(Vector2(600,856),Vector2(1120,24))
    obstacle(Vector2(32,484),Vector2(24,768))
    obstacle(Vector2(1168,484),Vector2(24,768))
    hero=load("res://mosslight/model_character.gd").new()
    hero.position=Vector2(640,740)
    sorted.add_child(hero)
    var label := Label.new()
    label.position=Vector2(32,20)
    label.text="MOSSLIGHT / COURTYARD SCALE STUDY\nWASD / arrows: move    Shift: run\nModel art in context | ground texture studies | exterior only"
    label.add_theme_font_size_override("font_size",20)
    add_child(label)
    var inventory_panel=load("res://mosslight/model_inventory.gd").new()
    inventory_panel.position=Vector2(774,0)
    add_child(inventory_panel)
    interaction_label=Label.new()
    interaction_label.position=Vector2(680,855)
    add_child(interaction_label)
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture="):capture=arg.trim_prefix("--capture=")
    if standalone_checks and "--self-test" in OS.get_cmdline_user_args():checks.call_deferred()

func _process(_delta: float) -> void:
    if interaction_label == null or hero == null: return
    var near := hero.position.distance_to(chest.position)<70
    interaction_label.text=("E: open / close chest" if near else "Approach the chest")+" | Potions collected: "+str(loot_count)
    var pressed := Input.is_physical_key_pressed(KEY_E)
    if pressed and not interact_held and near: chest.interact()
    interact_held=pressed

func press_interact() -> void:
    var event := InputEventKey.new()
    event.physical_keycode=KEY_E
    event.keycode=KEY_E
    event.pressed=true
    Input.parse_input_event(event)
    for i in range(3):await get_tree().physics_frame
    event=InputEventKey.new()
    event.physical_keycode=KEY_E
    event.keycode=KEY_E
    Input.parse_input_event(event)
    for i in range(3):await get_tree().physics_frame

func checks():
    hero.automated=true
    hero.position=Vector2(340,674)
    hero.auto_direction=Vector2.UP
    hero.automated_run=true
    for i in range(30):await get_tree().physics_frame
    assert(hero.position.y>=647 and hero.get_slide_collision_count()>0)
    assert(hero.position.y>guild.position.y)
    if not capture.is_empty():
        await RenderingServer.frame_post_draw
        assert(get_viewport().get_texture().get_image().save_png(capture.get_basename()+"-front.png")==OK)
    hero.position=Vector2(340,552)
    hero.auto_direction=Vector2.DOWN
    for i in range(30):await get_tree().physics_frame
    assert(hero.position.y<=569 and hero.get_slide_collision_count()>0)
    assert(hero.position.y<guild.position.y)
    if not capture.is_empty():
        await RenderingServer.frame_post_draw
        assert(get_viewport().get_texture().get_image().save_png(capture.get_basename()+"-back.png")==OK)
    hero.position=Vector2(610,660)
    hero.auto_direction=Vector2.UP
    for i in range(30):await get_tree().physics_frame
    assert(hero.position.y>=626 and hero.get_slide_collision_count()>0)
    hero.position=Vector2(705,666)
    hero.auto_direction=Vector2.UP
    for i in range(30):await get_tree().physics_frame
    assert(hero.position.y>=635 and hero.get_slide_collision_count()>0)
    hero.auto_direction=Vector2.ZERO
    hero.position=Vector2(1020,554)
    hero.auto_direction=Vector2.UP
    for i in range(30):await get_tree().physics_frame
    assert(hero.position.y>=525 and hero.get_slide_collision_count()>0)
    assert(hero.position.y>tree.position.y)
    if not capture.is_empty():
        await RenderingServer.frame_post_draw
        assert(get_viewport().get_texture().get_image().save_png(capture.get_basename()+"-tree-front.png")==OK)
    hero.position=Vector2(1020,466)
    hero.auto_direction=Vector2.DOWN
    for i in range(30):await get_tree().physics_frame
    assert(hero.position.y<=491 and hero.get_slide_collision_count()>0)
    assert(hero.position.y<tree.position.y)
    if not capture.is_empty():
        await RenderingServer.frame_post_draw
        assert(get_viewport().get_texture().get_image().save_png(capture.get_basename()+"-tree-back.png")==OK)
    hero.position=Vector2(938,598)
    hero.auto_direction=Vector2.UP
    for i in range(30):await get_tree().physics_frame
    assert(hero.position.y>=569 and hero.get_slide_collision_count()>0)
    hero.auto_direction=Vector2.ZERO
    hero.position=Vector2(800,684)
    hero.auto_direction=Vector2.UP
    for i in range(30):await get_tree().physics_frame
    assert(hero.position.y>=646 and hero.get_slide_collision_count()>0)
    hero.auto_direction=Vector2.ZERO
    hero.position=Vector2(800,680)
    await press_interact()
    assert(chest.busy)
    await press_interact()
    await get_tree().create_timer(.5).timeout
    assert(chest.is_open and not chest.busy and loot_count==1)
    if not capture.is_empty():
        await RenderingServer.frame_post_draw
        assert(get_viewport().get_texture().get_image().save_png(capture.get_basename()+"-chest-open.png")==OK)
    await press_interact()
    await get_tree().create_timer(.5).timeout
    assert(not chest.is_open and loot_count==1)
    await press_interact()
    await get_tree().create_timer(.5).timeout
    assert(chest.is_open and loot_count==1)
    hero.position=Vector2(640,740)
    await press_interact()
    assert(chest.is_open and not chest.busy and loot_count==1)
    hero.position=Vector2(640,740)
    assert(hero.get_parent()==guild.get_parent() and sorted.y_sort_enabled)
    assert(shadows.get_index()<sorted.get_index() and shadows.get_child_count()==6)
    await get_tree().create_timer(.2).timeout
    if not capture.is_empty():
        await RenderingServer.frame_post_draw
        assert(get_viewport().get_texture().get_image().save_png(capture)==OK)
    print("COURTYARD_QA_OK: building/prop collision, Y-sort, chest live E input/range/busy gate/open-close/reopen/single reward; actual scene rendered")
    get_tree().quit()

func _draw():
    draw_rect(Rect2(0,0,1200,900),Color("293932"))
    draw_rect(Rect2(44,124,1112,720),Color("71816f"))
    for x in range(44,1157,32):draw_line(Vector2(x,124),Vector2(x,844),Color(1,1,1,.035))
    for y in range(124,845,32):draw_line(Vector2(44,y),Vector2(1156,y),Color(1,1,1,.035))
