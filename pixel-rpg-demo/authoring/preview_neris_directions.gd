extends SceneTree
## Direction ring uses the exported atlas; no artificial animation is presented.
func _initialize() -> void:
    call_deferred("review")
func review() -> void:
    root.size = Vector2i(840, 1020)
    root.content_scale_size = root.size
    var bg := ColorRect.new()
    bg.size = Vector2(840, 1020)
    bg.color = Color("ded8c7")
    root.add_child(bg)
    var title := Label.new()
    title.text = "Neris / Eight static direction studies - art review pending"
    title.position = Vector2(24, 15)
    title.add_theme_color_override("font_color", Color("33352e"))
    root.add_child(title)
    var base := ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/")
    var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(base + "neris-direction-studies.json"))
    var atlas := Image.load_from_file(base + "neris-direction-studies.png")
    assert(atlas != null and atlas.get_size() == Vector2i(768,144))
    assert(data.directions.size() == 8 and data.clips.is_empty())
    var cells := {"NW":Vector2i(0,0),"N":Vector2i(1,0),"NE":Vector2i(2,0),"W":Vector2i(0,1),"E":Vector2i(2,1),"SW":Vector2i(0,2),"S":Vector2i(1,2),"SE":Vector2i(2,2)}
    var seen: Dictionary = {}
    for entry in data.directions:
        assert(cells.has(entry.heading) and not seen.has(entry.heading))
        seen[entry.heading] = true
        var rect: Array = entry.rect
        var pixels := atlas.get_region(Rect2i(rect[0],rect[1],rect[2],rect[3]))
        var source := Image.load_from_file(ProjectSettings.globalize_path("res://../" + entry.sprite))
        source.convert(Image.FORMAT_RGBA8)
        pixels.convert(Image.FORMAT_RGBA8)
        assert(pixels.get_data() == source.get_data())
        assert(pixels.get_used_rect().end.y == 122)
        var cell: Vector2i = cells[entry.heading]
        var label := Label.new()
        label.text = entry.heading
        label.position = Vector2(cell.x * 280 + 125, cell.y * 300 + 63)
        label.add_theme_color_override("font_color",Color("33352e"))
        root.add_child(label)
        var sprite := Sprite2D.new()
        sprite.texture = ImageTexture.create_from_image(pixels)
        sprite.centered = false
        sprite.scale = Vector2(2,2)
        sprite.position = Vector2(cell.x * 280 + 44, cell.y * 300 + 94)
        sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
        root.add_child(sprite)
    var note := Label.new()
    note.text = "Static drafts only\n\n8 headings present\n0 movement clips\n\nShading / proportions\nstill need alignment"
    note.position = Vector2(325, 423)
    note.add_theme_color_override("font_color",Color("33352e"))
    root.add_child(note)
    await process_frame
    await RenderingServer.frame_post_draw
    var error := root.get_texture().get_image().save_png(base + "neris-directions-godot.png")
    assert(error == OK)
    print("NERIS_DIRECTIONS_RENDER_OK: 8 distinct headings, atlas pixels match source sprites, shared foot anchor; static only")
    quit()
