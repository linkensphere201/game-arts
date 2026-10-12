extends Node2D
## Isolated review room for the actual model-derived SpriteFrames.
var hero: CharacterBody2D
var state_label: Label

func wall(at: Vector2, size: Vector2):
    var body := StaticBody2D.new()
    body.position = at
    var shape := CollisionShape2D.new()
    var rectangle := RectangleShape2D.new()
    rectangle.size = size
    shape.shape = rectangle
    body.add_child(shape)
    add_child(body)

func _ready():
    get_window().content_scale_size = Vector2i(960,640)
    texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    wall(Vector2(480,92),Vector2(896,24))
    wall(Vector2(480,606),Vector2(896,24))
    wall(Vector2(32,350),Vector2(24,540))
    wall(Vector2(928,350),Vector2(24,540))
    wall(Vector2(560,335),Vector2(68,30))
    var sorted := Node2D.new()
    sorted.y_sort_enabled = true
    add_child(sorted)
    hero = load("res://mosslight/model_character.gd").new()
    hero.name = "Hero"
    hero.position = Vector2(430,420)
    sorted.add_child(hero)
    var chest := Sprite2D.new()
    chest.texture = load("res://mosslight/model_review/chest.png")
    assert(chest.texture!=null)
    chest.position = Vector2(560,350)
    chest.offset.y = -chest.texture.get_height()/2.0+4
    sorted.add_child(chest)
    var title := Label.new()
    title.text = "MOSSLIGHT / MODEL CHARACTER PLAYABLE STUDY"
    title.position = Vector2(32,18)
    title.add_theme_font_size_override("font_size",22)
    add_child(title)
    var help := Label.new()
    help.text = "WASD / arrows: move   |   Shift: run   |   Eight independent direction sources"
    help.position = Vector2(32,50)
    add_child(help)
    state_label = Label.new()
    state_label.position = Vector2(32,616)
    add_child(state_label)

func _process(_delta):
    state_label.text = "Direction: %s    Action: %s    Art polish pending" % [hero.direction,hero.action]

func _draw():
    draw_rect(Rect2(0,0,960,640),Color("293932"))
    draw_rect(Rect2(44,104,872,490),Color("6f8170"))
    for x in range(44,917,32): draw_line(Vector2(x,104),Vector2(x,594),Color(1,1,1,.05))
    for y in range(104,595,32): draw_line(Vector2(44,y),Vector2(916,y),Color(1,1,1,.05))
    draw_rect(Rect2(526,320,68,30),Color(.08,.1,.08,.15))
