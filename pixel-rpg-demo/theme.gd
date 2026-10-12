extends "res://main.gd"
const CAST=["rowan","sylva","bren","osric"]
var selected=0
func select_character(index):
    selected=index
    $World/Hero/Sprite.sprite_frames=load("res://mosslight/theme/"+CAST[index]+"_frames.tres")
    $HUD/Name.text="PLAYING: "+CAST[index].to_upper()+"  |  1-4 switch character"
func _ready():
    super._ready()
    select_character(0)
func _unhandled_key_input(event):
    super._unhandled_key_input(event)
    if event.pressed and not event.echo:
        var key=event.physical_keycode if event.physical_keycode!=0 else event.keycode
        if key>=KEY_1 and key<=KEY_4:select_character(key-KEY_1)
