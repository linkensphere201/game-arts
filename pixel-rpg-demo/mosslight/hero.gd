extends CharacterBody2D
@export var speed := 70.0
var direction := "S"
var automated := false
var auto_direction := Vector2.ZERO
const HEADINGS := ["S","SE","E","NE","N","NW","W","SW"]
func _physics_process(_delta):
    var input := auto_direction if automated else Input.get_vector("ui_left","ui_right","ui_up","ui_down")
    if not automated:
        input+=Vector2(float(Input.is_physical_key_pressed(KEY_D))-float(Input.is_physical_key_pressed(KEY_A)),float(Input.is_physical_key_pressed(KEY_S))-float(Input.is_physical_key_pressed(KEY_W)))
    input=input.limit_length()
    if input.length()>.01:
        var angle := atan2(input.x,input.y)
        direction=HEADINGS[posmod(roundi(angle/(PI/4)),8)]
    velocity=input*speed
    move_and_slide()
    $Sprite.play(("walk_" if input.length()>.01 else "idle_")+direction)
