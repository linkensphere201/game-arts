extends SceneTree
var failures=[]
func check(ok,message):
    if not ok:failures.append(message);push_error(message)
func _initialize():call_deferred("run")
func press(key):
    var event=InputEventKey.new();event.physical_keycode=key;event.pressed=true;root.push_input(event)
func run():
    var scene=load("res://theme.tscn").instantiate();root.add_child(scene);scene.set_process(false)
    var hero=scene.get_node("World/Hero");hero.automated=true
    for index in range(4):
        press(KEY_1+index)
        check(scene.selected==index,"Cast selection failed")
        for direction in range(8):
            hero.position=Vector2(320,300)
            var heading=Vector2(sin(direction*PI/4),cos(direction*PI/4));hero.auto_direction=heading
            for frame in range(6):await physics_frame
            check(hero.get_node("Sprite").animation=="walk_"+hero.HEADINGS[direction],"Wrong clip")
            check((hero.position-Vector2(320,300)).dot(heading)>1,"No displacement")
    hero.position=Vector2(134,250);hero.auto_direction=Vector2.UP
    for frame in range(40):await physics_frame
    check(hero.position.y>=233,"Shop collision failed")
    hero.auto_direction=Vector2.ZERO;hero.position=Vector2(410,358);press(KEY_E)
    await process_frame
    check(scene.chest_open,"Chest interaction failed")
    scene.free();print("THEME_RUNTIME_QA failures=",failures);quit(0 if failures.is_empty() else 1)
