extends Node2D
var time := 0.0
var capture_dir := ""
var qa_seconds := 0.0
var chest_open := false
var chest_elapsed := 0.0
var hero: CharacterBody2D
func _ready():
    texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
    hero=$World/Hero
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture-dir="):capture_dir=arg.trim_prefix("--capture-dir=")
        if arg.begins_with("--qa-seconds="):qa_seconds=float(arg.trim_prefix("--qa-seconds="))
    if not capture_dir.is_empty():
        hero.automated=true
        run_captures()
func _process(delta):
    time+=delta
    $World/Lantern.frame=int(time*5)%4
    if hero.automated:
        var phase=int(time/1.2)%8
        var angle=phase*PI/4
        hero.auto_direction=Vector2(sin(angle),cos(angle))*.65
    if chest_open:
        chest_elapsed+=delta
        $World/Chest.frame=mini(3,int(chest_elapsed*6))
    if qa_seconds>0 and time>=qa_seconds:
        print("PIXEL_RPG_RUNTIME_OK seconds=",time," position=",hero.position," chest=",chest_open)
        get_tree().quit()
func run_captures():
    await get_tree().create_timer(.7).timeout
    await RenderingServer.frame_post_draw
    var result=get_viewport().get_texture().get_image().save_png(capture_dir.path_join("room.png"))
    if result!=OK:push_error("CAPTURE_FAILED");get_tree().quit(1)
    await get_tree().create_timer(2).timeout
    chest_open=true
    $World/Chest.frame=3
    await RenderingServer.frame_post_draw
    result=get_viewport().get_texture().get_image().save_png(capture_dir.path_join("room-open.png"))
    if result!=OK:push_error("CAPTURE_FAILED");get_tree().quit(1)
    print("PIXEL_RPG_CAPTURE_OK")
    if qa_seconds<=0:get_tree().quit()

func _unhandled_key_input(event):
    if event.pressed and not event.echo and (event.physical_keycode==KEY_E or event.keycode==KEY_E):
        if hero.position.distance_to($World/Chest.position)<55 and not chest_open:
            chest_open=true
            $HUD/Note.text="Chest opened: 10 gold | E interacts near the chest"
