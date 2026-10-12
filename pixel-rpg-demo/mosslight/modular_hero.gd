extends "res://mosslight/hero.gd"
var automated_run=false
func _physics_process(_delta):
    var input=auto_direction if automated else Input.get_vector("ui_left","ui_right","ui_up","ui_down")
    if not automated:
        input+=Vector2(float(Input.is_physical_key_pressed(KEY_D))-float(Input.is_physical_key_pressed(KEY_A)),float(Input.is_physical_key_pressed(KEY_S))-float(Input.is_physical_key_pressed(KEY_W)))
    input=input.limit_length()
    var running=automated_run if automated else Input.is_physical_key_pressed(KEY_SHIFT)
    var action="idle"
    if input.length()>.01:
        direction=HEADINGS[posmod(roundi(atan2(input.x,input.y)/(PI/4)),8)]
        action="run" if running else "walk"
    velocity=input*(115.0 if running else 65.0)
    move_and_slide()
    $Sprite.play(action+"_"+direction)
