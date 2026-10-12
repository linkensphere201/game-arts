extends SceneTree
var failures=[]
func check(ok,message):
    if not ok:failures.append(message);push_error(message)
func _initialize():call_deferred("run")
func run():
    var scene=load("res://main.tscn").instantiate();root.add_child(scene)
    var hero=scene.get_node("World/Hero")
    scene.set_process(false);hero.automated=true
    for i in range(8):
        hero.position=Vector2(320,240)
        var heading=Vector2(sin(i*PI/4),cos(i*PI/4))
        hero.auto_direction=heading
        for frame in range(8):await physics_frame
        check(hero.get_node("Sprite").animation=="walk_"+hero.HEADINGS[i],"Wrong heading "+str(i))
        check((hero.position-Vector2(320,240)).dot(heading)>2,"No movement "+str(i))
    hero.auto_direction=Vector2.ZERO
    for frame in range(3):await physics_frame
    check(hero.get_node("Sprite").animation=="idle_SW","Idle loses facing")
    hero.position=Vector2(23,240);hero.auto_direction=Vector2.LEFT
    for frame in range(20):await physics_frame
    check(hero.position.x>=20,"Boundary collision failed")
    hero.auto_direction=Vector2.ZERO;hero.position=Vector2(390,235)
    var key=InputEventKey.new();key.physical_keycode=KEY_E;key.pressed=true
    root.push_input(key)
    await process_frame
    scene._process(.2)
    check(scene.chest_open,"E interaction failed")
    var release=InputEventKey.new();release.physical_keycode=KEY_E;release.pressed=false;root.push_input(release)
    scene._process(.6)
    check(scene.get_node("World/Chest").frame==3,"Chest animation incomplete")
    scene.free()
    print("M5_BEHAVIOR_QA failures=",failures)
    quit(0 if failures.is_empty() else 1)
