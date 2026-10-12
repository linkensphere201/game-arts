extends "res://theme.gd"
var catalog={}
func _ready():
    catalog=JSON.parse_string(FileAccess.get_file_as_string("res://mosslight/modular/catalog.json"))
    super._ready()
func select_character(index):
    selected=posmod(index,16)
    var entry=catalog.presets[selected]
    $World/Hero/Sprite.sprite_frames=load("res://mosslight/modular/"+entry.id+"_frames.tres")
    $HUD/Name.text=str(selected+1)+"/16 "+entry.name+" | "+catalog.species[entry.species]+" | TAB next / SHIFT run"
func _unhandled_key_input(event):
    super._unhandled_key_input(event)
    if event.pressed and not event.echo and event.physical_keycode==KEY_TAB:select_character(selected+1)
func _process(delta):
    super._process(delta)
    if hero.automated:hero.automated_run=int(time/2.0)%2==1
