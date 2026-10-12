extends SceneTree
## Real physics/input/animation integration checks; no claim of art acceptance.
var capture := ""

func _initialize():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture="): capture=arg.trim_prefix("--capture=")
    run_checks.call_deferred()

func tick(count: int):
    for i in range(count): await physics_frame

func run_checks():
    var packed := load("res://model_playable.tscn") as PackedScene
    assert(packed!=null)
    var level = packed.instantiate()
    root.add_child(level)
    await tick(2)
    var hero = level.hero
    hero.automated=true
    var directions := {"S":Vector2.DOWN,"SE":Vector2(1,1),"E":Vector2.RIGHT,"NE":Vector2(1,-1),"N":Vector2.UP,"NW":Vector2(-1,-1),"W":Vector2.LEFT,"SW":Vector2(-1,1)}
    for name in directions:
        hero.position=Vector2(430,420)
        hero.auto_direction=directions[name]
        hero.automated_run=false
        await tick(4)
        assert(hero.direction==name and hero.sprite.animation=="walk_"+name)
        assert(is_equal_approx(hero.velocity.length(),65.0))
        hero.automated_run=true
        await tick(4)
        assert(hero.sprite.animation=="run_"+name)
        assert(is_equal_approx(hero.velocity.length(),115.0))
        hero.auto_direction=Vector2.ZERO
        await tick(2)
        assert(hero.direction==name and hero.sprite.animation=="idle_"+name)
        assert(hero.velocity==Vector2.ZERO)
    hero.position=Vector2(50,420)
    hero.auto_direction=Vector2.LEFT
    await tick(20)
    assert(hero.position.x>=51.0 and hero.get_slide_collision_count()>0)
    hero.position=Vector2(505,335)
    hero.auto_direction=Vector2.RIGHT
    await tick(25)
    assert(hero.position.x<520 and hero.get_slide_collision_count()>0)
    # Exercise the live input path too, rather than only the automated control variables.
    hero.position=Vector2(430,420)
    hero.automated=false
    Input.action_press("ui_up")
    Input.action_press("ui_right")
    await tick(4)
    assert(hero.direction=="NE" and hero.action=="walk")
    var shift := InputEventKey.new()
    shift.physical_keycode=KEY_SHIFT
    shift.pressed=true
    Input.parse_input_event(shift)
    await tick(3)
    assert(hero.action=="run" and hero.sprite.animation=="run_NE")
    shift.pressed=false
    Input.parse_input_event(shift)
    Input.action_release("ui_up")
    Input.action_release("ui_right")
    await tick(3)
    assert(hero.sprite.animation=="idle_NE")
    var idle_frame: int = hero.sprite.frame
    await create_timer(.65).timeout
    assert(hero.sprite.animation=="idle_NE" and hero.sprite.frame!=idle_frame)
    assert(hero.sprite.is_playing() and hero.velocity==Vector2.ZERO)
    print("LIVE_IDLE_QA_OK: stopped character continues its breathing animation")
    print("MODEL_PLAYABLE_QA_OK: 8 headings, walk/run/idle, normalized speed, walls/chest collision, live input + Shift")
    if not capture.is_empty():
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(capture)==OK)
        print("MODEL_PLAYABLE_CAPTURE_OK")
    quit()
