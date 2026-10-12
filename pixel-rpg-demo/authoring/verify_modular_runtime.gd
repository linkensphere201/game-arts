extends SceneTree
var failures=[]
func check(ok,message):
    if not ok:failures.append(message);push_error(message)
func _initialize():call_deferred("run")
func press(key):
    var event=InputEventKey.new();event.physical_keycode=key;event.pressed=true;root.push_input(event)
func run():
    for i in range(16):
        var standalone=load("res://mosslight/modular/cast_%02d.tscn" % (i+1)).instantiate()
        check(standalone.has_node("GroundShadow"),"Standalone shadow missing")
        check(standalone.get_node("Sprite").sprite_frames.get_animation_names().size()==24,"Standalone clip count wrong")
        standalone.free()
    var scene=load("res://modular.tscn").instantiate();root.add_child(scene);scene.set_process(false)
    var hero=scene.get_node("World/Hero");hero.automated=true
    check(hero.has_node("GroundShadow"),"Missing independent shadow")
    if not hero.has_node("GroundShadow"):scene.free();quit(1);return
    var anchor=hero.get_node("GroundShadow").position
    for index in range(16):
        scene.select_character(index)
        for action in ["walk","run"]:
            hero.automated_run=action=="run"
            for direction in range(8):
                hero.position=Vector2(320,300)
                var heading=Vector2(sin(direction*PI/4),cos(direction*PI/4));hero.auto_direction=heading
                for frame in range(3):await physics_frame
                check(hero.get_node("Sprite").animation==action+"_"+hero.HEADINGS[direction],"Wrong clip "+str(index))
                check(hero.velocity.length()>100 if action=="run" else hero.velocity.length()<70,"Wrong speed")
                check(hero.get_node("GroundShadow").position==anchor,"Shadow bobs with body")
    hero.auto_direction=Vector2.ZERO
    for frame in range(3):await physics_frame
    check(hero.get_node("Sprite").animation=="idle_SW","Idle heading failed")
    scene.select_character(15);press(KEY_TAB);await process_frame
    check(scene.selected==0,"Tab wrap failed")
    hero.position=Vector2(134,250);hero.auto_direction=Vector2.UP
    for frame in range(20):await physics_frame
    check(hero.position.y>=233,"Shop collision failed")
    hero.auto_direction=Vector2.ZERO;hero.position=Vector2(410,358);press(KEY_E);await process_frame
    check(scene.chest_open,"Chest interaction failed")
    scene.free();print("MODULAR_RUNTIME_QA 256 movement clips, shadow, selection, collision; failures=",failures)
    quit(0 if failures.is_empty() else 1)
