extends CharacterBody2D
## Reusable study controller; art is still under review.
const HEADINGS := ["S","SE","E","NE","N","NW","W","SW"]
var direction := "S"
var action := "idle"
var automated := false
var auto_direction := Vector2.ZERO
var automated_run := false
var sprite: AnimatedSprite2D

func _ready():
    texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    sprite = AnimatedSprite2D.new()
    sprite.name = "Sprite"
    sprite.sprite_frames = load("res://mosslight/model_motion/rowan_study.tres")
    assert(sprite.sprite_frames!=null)
    sprite.offset = Vector2(0,-50)
    add_child(sprite)
    var shape := CollisionShape2D.new()
    var circle := CircleShape2D.new()
    circle.radius = 8
    shape.shape = circle
    add_child(shape)
    sprite.play("idle_S")

func _physics_process(_delta):
    var input := auto_direction if automated else Input.get_vector("ui_left","ui_right","ui_up","ui_down")
    if not automated:
        input += Vector2(float(Input.is_physical_key_pressed(KEY_D))-float(Input.is_physical_key_pressed(KEY_A)),float(Input.is_physical_key_pressed(KEY_S))-float(Input.is_physical_key_pressed(KEY_W)))
        if get_viewport().gui_get_focus_owner() is BaseButton:
            input = Vector2.ZERO
    input = input.limit_length()
    var running := automated_run if automated else Input.is_physical_key_pressed(KEY_SHIFT)
    action = "idle"
    if input.length()>.01:
        direction = HEADINGS[posmod(roundi(atan2(input.x,input.y)/(PI/4)),8)]
        action = "run" if running else "walk"
    velocity = input*(115.0 if running else 65.0)
    move_and_slide()
    sprite.play(action+"_"+direction)

func _draw():
    draw_set_transform(Vector2.ZERO,0,Vector2(1,.3))
    draw_circle(Vector2.ZERO,14,Color(.08,.1,.08,.26))
    draw_set_transform(Vector2.ZERO)
