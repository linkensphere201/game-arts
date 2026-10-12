extends Node2D
# Isolated static visual review. Does not change the playable demo or claim animation.
var capture_path := ""
func label_at(text: String, at: Vector2, font_size: int = 12):
    var label = Label.new()
    label.text = text
    label.position = at
    label.add_theme_font_size_override("font_size", font_size)
    label.modulate = Color("ddd8c7")
    add_child(label)
func sprite_at(id: String, foot: Vector2):
    var sprite = Sprite2D.new()
    sprite.texture = load("res://mosslight/model_review/" + id + ".png")
    assert(sprite.texture != null)
    sprite.position = foot
    sprite.offset.y = -sprite.texture.get_height()/2.0 + 4
    add_child(sprite)
func _ready():
    texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture="):capture_path = arg.trim_prefix("--capture=")
    label_at("MOSSLIGHT / LOCAL MODEL STYLE PILOT",Vector2(16,10),19)
    label_at("Static review only | camera + pixel cleanup pending",Vector2(16,38))
    sprite_at("guild",Vector2(225,370))
    sprite_at("rowan",Vector2(346,375))
    sprite_at("chest",Vector2(429,370))
    sprite_at("book",Vector2(552,174))
    label_at("Guild / 320 px cell",Vector2(85,391))
    label_at("Character",Vector2(314,391))
    label_at("Chest",Vector2(410,391))
    label_at("Item / 32 px",Vector2(511,188))
    label_at("Shared 128-color conversion palette / separate character shadow",Vector2(16,414))
    queue_redraw()
    if not capture_path.is_empty():
        await get_tree().create_timer(1.0).timeout
        await RenderingServer.frame_post_draw
        var result = get_viewport().get_texture().get_image().save_png(capture_path)
        assert(result == OK)
        print("MODEL_ART_REVIEW_CAPTURE_OK")
        get_tree().quit()
func _draw():
    draw_rect(Rect2(0,0,640,448),Color("252c32"))
    draw_rect(Rect2(16,65,475,343),Color("69796d"))
    for x in range(16,492,32):draw_line(Vector2(x,65),Vector2(x,408),Color(1,1,1,.035))
    for y in range(65,409,32):draw_line(Vector2(16,y),Vector2(491,y),Color(1,1,1,.035))
    draw_set_transform(Vector2(346,374),0,Vector2(1,.3))
    draw_circle(Vector2.ZERO,17,Color(0.08,.1,.13,.25))
    draw_set_transform(Vector2.ZERO)
