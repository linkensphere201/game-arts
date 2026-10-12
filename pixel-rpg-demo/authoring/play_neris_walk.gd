extends SceneTree
class Driver extends Node:
    var tick:Callable
    func _process(delta:float)->void:tick.call(delta)
var body:Node2D
var sprite:Sprite2D
var shadow:Polygon2D
var idle:Texture2D
var frames:Array[Texture2D]=[]
var north_frames:Array[Texture2D]=[]
var east_frames:Array[Texture2D]=[]
var east_run_frames:Array[Texture2D]=[]
var west_run_frames:Array[Texture2D]=[]
var running:=false
var west_frames:Array[Texture2D]=[]
var se_frames:Array[Texture2D]=[]
var se_idle:Texture2D
var sw_frames:Array[Texture2D]=[]
var sw_idle:Texture2D
var ne_frames:Array[Texture2D]=[]
var ne_idle:Texture2D
var nw_frames:Array[Texture2D]=[]
var nw_idle:Texture2D
var west_idle:Texture2D
var east_idle:Texture2D
var south_idle:Texture2D
var north_idle:Texture2D
var facing:=1
var phase:=0.0
var moving:=false
var driver:Driver
func _initialize()->void:call_deferred("setup")
func tick(delta:float)->void:
    if Input.is_key_pressed(KEY_ESCAPE):quit()
    if Input.is_key_pressed(KEY_R):body.position=Vector2(320,380)
    var down:=Input.is_key_pressed(KEY_SPACE) or Input.is_key_pressed(KEY_DOWN)
    var up:=Input.is_key_pressed(KEY_UP)
    var east:=Input.is_key_pressed(KEY_RIGHT)
    var west:=Input.is_key_pressed(KEY_LEFT)
    var vertical:=int(down)-int(up)
    var horizontal:=int(east)-int(west)
    # Each direction uses independently authored artwork.
    var direction:=horizontal*2 if not (down or up) else vertical if not (east or west) else 0
    if east and down and not (west or up):direction=3
    if west and down and not (east or up):direction=4
    if east and up and not (west or down):direction=5
    if west and up and not (east or down):direction=6
    if direction!=0 and direction!=facing:
        facing=direction
        phase=0.0
    idle=nw_idle if facing==6 else ne_idle if facing==5 else sw_idle if facing==4 else se_idle if facing==3 else west_idle if facing==-2 else east_idle if facing==2 else north_idle if facing==-1 else south_idle
    var velocity:=Vector2(-1,-1).normalized() if direction==6 else Vector2(1,-1).normalized() if direction==5 else Vector2(-1,1).normalized() if direction==4 else Vector2.ONE.normalized() if direction==3 else Vector2(float(direction)/2.0,0) if abs(direction)==2 else Vector2(0,direction)
    var wants_run:bool=absi(direction)==2 and Input.is_key_pressed(KEY_SHIFT)
    if wants_run!=running:phase=0.0
    running=wants_run
    var speed:=48.0 if running else 24.0
    var next:=body.position+velocity*speed*2.0*delta
    if direction in [3,4,5,6]:
        var edge_x:=100.0 if direction in [4,6] else 550.0
        var edge_y:=330.0 if direction in [5,6] else 470.0
        var distance:=minf(48.0*delta,minf((edge_x-body.position.x)/velocity.x,(edge_y-body.position.y)/velocity.y))
        next=body.position+velocity*maxf(0,distance)
    next.x=clampf(next.x,100,550);next.y=clampf(next.y,330,470)
    if direction==3 and (body.position.x>=550 or body.position.y>=470):next=body.position
    if direction==4 and (body.position.x<=100 or body.position.y>=470):next=body.position
    if direction==5 and (body.position.x>=550 or body.position.y<=330):next=body.position
    if direction==6 and (body.position.x<=100 or body.position.y<=330):next=body.position
    moving=direction!=0 and next!=body.position
    if moving:
        body.position=next
        phase+=delta
        sprite.texture=(west_run_frames if running and facing==-2 else east_run_frames if running else nw_frames if facing==6 else ne_frames if facing==5 else sw_frames if facing==4 else se_frames if facing==3 else west_frames if facing==-2 else east_frames if facing==2 else north_frames if facing==-1 else frames)[int(phase*(16.0 if running else 12.0))%8]
    else:
        running=false
        phase=0.0
        sprite.texture=idle
    shadow.position=Vector2(0,0)
func setup()->void:
    root.size=Vector2i(640,560);root.content_scale_size=root.size
    var bg:=ColorRect.new();bg.size=Vector2(640,560);bg.color=Color("ded8c7");root.add_child(bg)
    for y in range(150,500,32):
        var line:=ColorRect.new();line.position=Vector2(20,y);line.size=Vector2(600,1);line.color=Color("c4bfaf");root.add_child(line)
    var label:=Label.new();label.text="NERIS / EIGHT-DIRECTION WALK STUDY\nARROWS: walk | SHIFT + LEFT/RIGHT: run | R: reset | ESC: exit\nEast/west run candidates. Other headings walk. Art unfinished.";label.position=Vector2(20,12);label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
    body=Node2D.new();body.position=Vector2(320,380);root.add_child(body)
    shadow=Polygon2D.new();var points:=PackedVector2Array()
    for n in range(24):
        var angle:=float(n)*TAU/24.0
        points.append(Vector2(cos(angle)*29,sin(angle)*8))
    shadow.polygon=points;shadow.color=Color(0.16,0.14,0.18,0.24);body.add_child(shadow)
    sprite=Sprite2D.new();sprite.centered=false;sprite.position=Vector2(-96,-244);sprite.scale=Vector2(2,2);sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;body.add_child(sprite)
    idle=ImageTexture.create_from_image(Image.load_from_file("res://mosslight/model_review/neris-walk-neutral.png"))
    var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/neris-stance/")
    var sheet:=Image.load_from_file(base+"coordinated-weighted.png");assert(sheet.get_size()==Vector2i(768,144))
    for n in range(8):frames.append(ImageTexture.create_from_image(sheet.get_region(Rect2i(n*96,0,96,144))))
    south_idle=idle
    north_idle=ImageTexture.create_from_image(Image.load_from_file("res://mosslight/model_review/neris-walk-rear-neutral.png"))
    var north_sheet:=Image.load_from_file(base.replace("neris-stance/","neris-rear-stance/")+"coordinated-weighted.png")
    assert(north_sheet.get_size()==Vector2i(768,144))
    for n in range(8):north_frames.append(ImageTexture.create_from_image(north_sheet.get_region(Rect2i(n*96,0,96,144))))
    east_idle=ImageTexture.create_from_image(Image.load_from_file("res://mosslight/model_review/neris-walk-east-neutral.png"))
    var east_base:=base.replace("neris-stance/","neris-east-compact-travel/")
    var east_meta:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(east_base+"manifest.json"))
    assert(east_meta.fps==12 and east_meta.calibrated_speed==24)
    var east_sheet:=Image.load_from_file(east_base+"calibrated.png")
    assert(east_sheet.get_size()==Vector2i(768,144))
    for n in range(8):east_frames.append(ImageTexture.create_from_image(east_sheet.get_region(Rect2i(n*96,0,96,144))))
    var run_base:=base.replace("neris-stance/","neris-east-run-travel/")
    var run_meta:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(run_base+"manifest.json"))
    assert(run_meta.fps==16 and run_meta.calibrated_speed==48)
    assert(FileAccess.get_sha256(base.replace("neris-stance/","neris-east-run-material.png"))==run_meta.source_sha256,"Stale run source; regenerate calibration")
    var run_sheet:=Image.load_from_file(run_base+"calibrated.png")
    assert(run_sheet.get_size()==Vector2i(768,144))
    for n in range(8):east_run_frames.append(ImageTexture.create_from_image(run_sheet.get_region(Rect2i(n*96,0,96,144))))
    var west_run_base:=base.replace("neris-stance/","neris-west-run-travel/")
    var west_run_meta:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(west_run_base+"manifest.json"))
    assert(west_run_meta.fps==16 and west_run_meta.calibrated_speed==-48)
    assert(FileAccess.get_sha256(base.replace("neris-stance/","neris-west-run-arm-middle.png"))==west_run_meta.source_sha256,"Stale west run source")
    var west_run_sheet:=Image.load_from_file(west_run_base+"calibrated.png")
    assert(west_run_sheet.get_size()==Vector2i(768,144))
    for n in range(8):west_run_frames.append(ImageTexture.create_from_image(west_run_sheet.get_region(Rect2i(n*96,0,96,144))))
    west_idle=ImageTexture.create_from_image(Image.load_from_file("res://mosslight/model_review/neris-walk-west-neutral.png"))
    var west_base:=base.replace("neris-stance/","neris-west-travel/")
    var west_meta:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(west_base+"manifest.json"))
    assert(west_meta.fps==12 and west_meta.calibrated_speed==-24)
    var west_sheet:=Image.load_from_file(west_base+"calibrated.png")
    assert(west_sheet.get_size()==Vector2i(768,144))
    for n in range(8):west_frames.append(ImageTexture.create_from_image(west_sheet.get_region(Rect2i(n*96,0,96,144))))
    se_idle=ImageTexture.create_from_image(Image.load_from_file("res://mosslight/model_review/neris-walk-SE-neutral.png"))
    var se_base:=base.replace("neris-stance/","neris-SE-travel/")
    var se_meta:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(se_base+"manifest.json"))
    assert(se_meta.fps==12 and se_meta.speed==24)
    assert(absf(Vector2(se_meta.velocity[0],se_meta.velocity[1]).length()-24)<0.001)
    var se_sheet:=Image.load_from_file(se_base+"calibrated.png")
    assert(se_sheet.get_size()==Vector2i(768,144))
    for n in range(8):se_frames.append(ImageTexture.create_from_image(se_sheet.get_region(Rect2i(n*96,0,96,144))))
    sw_idle=ImageTexture.create_from_image(Image.load_from_file("res://mosslight/model_review/neris-walk-SW-neutral.png"))
    var sw_base:=base.replace("neris-stance/","neris-SW-travel/")
    var sw_meta:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(sw_base+"manifest.json"))
    assert(sw_meta.fps==12 and sw_meta.speed==24)
    assert(absf(Vector2(sw_meta.velocity[0],sw_meta.velocity[1]).length()-24)<0.001)
    var sw_sheet:=Image.load_from_file(sw_base+"calibrated.png")
    assert(sw_sheet.get_size()==Vector2i(768,144))
    for n in range(8):sw_frames.append(ImageTexture.create_from_image(sw_sheet.get_region(Rect2i(n*96,0,96,144))))
    ne_idle=ImageTexture.create_from_image(Image.load_from_file("res://mosslight/model_review/neris-walk-NE-neutral.png"))
    var ne_base:=base.replace("neris-stance/","neris-NE-travel/")
    var ne_meta:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(ne_base+"manifest.json"))
    assert(ne_meta.fps==12 and ne_meta.speed==24)
    assert(absf(Vector2(ne_meta.velocity[0],ne_meta.velocity[1]).length()-24)<0.001)
    var ne_sheet:=Image.load_from_file(ne_base+"calibrated.png")
    assert(ne_sheet.get_size()==Vector2i(768,144))
    for n in range(8):ne_frames.append(ImageTexture.create_from_image(ne_sheet.get_region(Rect2i(n*96,0,96,144))))
    nw_idle=ImageTexture.create_from_image(Image.load_from_file("res://mosslight/model_review/neris-walk-NW-neutral.png"))
    var nw_base:=base.replace("neris-stance/","neris-NW-travel/")
    var nw_meta:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(nw_base+"manifest.json"))
    assert(nw_meta.fps==12 and nw_meta.speed==24)
    assert(absf(Vector2(nw_meta.velocity[0],nw_meta.velocity[1]).length()-24)<0.001)
    var nw_sheet:=Image.load_from_file(nw_base+"calibrated.png")
    assert(nw_sheet.get_size()==Vector2i(768,144))
    for n in range(8):nw_frames.append(ImageTexture.create_from_image(nw_sheet.get_region(Rect2i(n*96,0,96,144))))
    if OS.get_cmdline_user_args().has("--palette"):
        var palette_base:=base.replace("neris-stance/","neris-coat-palette/")
        var palette_meta:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(palette_base+"manifest.json"))
        assert(palette_meta.records.size()==4)
        for record in palette_meta.records:
            var original_path:=ProjectSettings.globalize_path("res://../"+str(record.source))
            var candidate_path:=palette_base+str(record.heading)+"-"+str(record.kind)+".png"
            assert(FileAccess.get_sha256(original_path)==record.source_sha256,"Stale palette source; regenerate candidate")
            assert(FileAccess.get_sha256(candidate_path)==record.output_sha256,"Palette candidate hash mismatch")
            var candidate:=Image.load_from_file(candidate_path)
            var original:=Image.load_from_file(original_path)
            assert(candidate.get_size()==original.get_size())
            for y in range(candidate.get_height()):
                for x in range(candidate.get_width()):
                    assert(candidate.get_pixel(x,y).a==original.get_pixel(x,y).a)
            if record.kind=="idle":
                if record.heading=="E":east_idle=ImageTexture.create_from_image(candidate)
                else:west_idle=ImageTexture.create_from_image(candidate)
            else:
                var target:Array[Texture2D]=east_frames if record.heading=="E" else west_frames
                target.clear()
                for n in range(8):target.append(ImageTexture.create_from_image(candidate.get_region(Rect2i(n*96,0,96,144))))
        label.text+="\nBurgundy side-coat candidate (unapproved)."
    sprite.texture=idle
    driver=Driver.new();driver.tick=tick;root.add_child(driver)
    if OS.get_cmdline_user_args().has("--check"):
        await create_timer(0.1).timeout
        var start:=body.position.y
        press(true);await create_timer(0.4).timeout
        assert(moving and body.position.y>start+15 and phase>0.3)
        press(false);await create_timer(0.1).timeout
        var stopped:=body.position.y
        await create_timer(0.1).timeout
        assert(not moving and body.position.y==stopped and sprite.texture==idle and phase==0)
        press(true);await create_timer(0.12).timeout
        assert(moving and phase>0 and phase<0.25)
        body.position.y=469;await create_timer(0.15).timeout
        assert(body.position.y==470 and not moving and sprite.texture==idle)
        press(false);body.position.y=380
        press(true,KEY_UP);await create_timer(0.25).timeout
        assert(moving and facing==-1 and body.position.y<370 and north_frames.has(sprite.texture))
        press(false,KEY_UP);await create_timer(0.1).timeout
        assert(not moving and sprite.texture==north_idle)
        press(true,KEY_UP);press(true,KEY_DOWN);await create_timer(0.1).timeout
        assert(not moving and sprite.texture==north_idle)
        press(false,KEY_DOWN);body.position.y=331;await create_timer(0.15).timeout
        assert(body.position.y==330 and not moving and sprite.texture==north_idle)
        press(false,KEY_UP);body.position.y=380
        press(true,KEY_DOWN);await create_timer(0.1).timeout
        assert(facing==1 and moving and frames.has(sprite.texture))
        press(false,KEY_DOWN);await create_timer(0.1).timeout
        var start_x:=body.position.x
        press(true,KEY_RIGHT);await create_timer(0.25).timeout
        assert(facing==2 and moving and east_frames.has(sprite.texture))
        assert(absf(body.position.x-start_x-phase*48.0)<0.05)
        press(false,KEY_RIGHT);await create_timer(0.1).timeout
        var stopped_east:=body.position
        assert(sprite.texture==east_idle and phase==0)
        press(true,KEY_RIGHT);press(true,KEY_LEFT);await create_timer(0.1).timeout
        assert(not moving and body.position==stopped_east)
        press(false,KEY_LEFT);body.position.x=549;await create_timer(0.15).timeout
        assert(body.position.x==550 and not moving and sprite.texture==east_idle)
        press(false,KEY_RIGHT);press(true,KEY_R);await create_timer(0.1).timeout
        press(false,KEY_R);assert(body.position==Vector2(320,380))
        start_x=body.position.x
        press(true,KEY_LEFT);await create_timer(0.25).timeout
        assert(moving and facing==-2 and west_frames.has(sprite.texture))
        assert(absf(start_x-body.position.x-phase*48.0)<0.05)
        press(false,KEY_LEFT);await create_timer(0.1).timeout
        var stopped_west:=body.position
        assert(not moving and phase==0 and sprite.texture==west_idle)
        press(true,KEY_LEFT);press(true,KEY_RIGHT);await create_timer(0.1).timeout
        assert(not moving and body.position==stopped_west and sprite.texture==west_idle)
        press(false,KEY_RIGHT);press(true,KEY_UP);press(true,KEY_DOWN);await create_timer(0.1).timeout
        assert(not moving and body.position==stopped_west)
        press(false,KEY_UP);press(false,KEY_DOWN);body.position.x=101;await create_timer(0.15).timeout
        assert(body.position.x==100 and not moving and sprite.texture==west_idle)
        press(false,KEY_LEFT);press(true,KEY_R);await create_timer(0.1).timeout
        press(false,KEY_R);assert(body.position==Vector2(320,380))
        press(true,KEY_RIGHT);await create_timer(0.1).timeout
        assert(moving and facing==2 and east_frames.has(sprite.texture))
        press(false,KEY_RIGHT);press(true,KEY_LEFT);await create_timer(0.1).timeout
        assert(moving and facing==-2 and west_frames.has(sprite.texture) and phase<0.2)
        press(false,KEY_LEFT);await create_timer(0.1).timeout
        assert(not moving and sprite.texture==west_idle)
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(base+"four-direction-playable-godot.png")==OK)
        press(true,KEY_UP);await create_timer(0.1).timeout
        assert(facing==-1 and moving and north_frames.has(sprite.texture))
        press(false,KEY_UP);await create_timer(0.1).timeout
        assert(sprite.texture==north_idle and not moving)
        assert(shadow.get_parent()==body and shadow.position==Vector2.ZERO)
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(base+"bidirectional-playable-godot.png")==OK)
        body.position=Vector2(320,380)
        var se_start:=body.position
        press(true,KEY_RIGHT);press(true,KEY_DOWN);await create_timer(0.25).timeout
        assert(moving and facing==3 and se_frames.has(sprite.texture))
        var travel:=body.position-se_start
        assert(absf(travel.x-travel.y)<0.01 and absf(travel.length()-phase*48)<0.05)
        press(false,KEY_DOWN);await create_timer(0.1).timeout
        assert(moving and facing==2 and east_frames.has(sprite.texture))
        press(true,KEY_DOWN);press(false,KEY_RIGHT);await create_timer(0.1).timeout
        assert(moving and facing==1 and frames.has(sprite.texture))
        press(true,KEY_RIGHT);await create_timer(0.1).timeout
        press(false,KEY_RIGHT);press(false,KEY_DOWN);await create_timer(0.1).timeout
        assert(not moving and facing==3 and sprite.texture==se_idle and phase==0)
        var se_stop:=body.position
        press(true,KEY_RIGHT);press(true,KEY_DOWN);press(true,KEY_UP);await create_timer(0.1).timeout
        assert(not moving and body.position==se_stop)
        press(false,KEY_UP);body.position=Vector2(550,400);await create_timer(0.1).timeout
        assert(not moving and body.position==Vector2(550,400) and sprite.texture==se_idle)
        body.position=Vector2(547,400);await create_timer(0.2).timeout
        assert(not moving and absf(body.position.x-550)<0.001 and absf(body.position.y-403)<0.001)
        body.position=Vector2(400,470);await create_timer(0.1).timeout
        assert(not moving and body.position==Vector2(400,470))
        press(false,KEY_RIGHT);press(false,KEY_DOWN);body.position=Vector2(320,380)
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(base+"five-direction-playable-godot.png")==OK)
        var sw_start:=body.position
        press(true,KEY_LEFT);press(true,KEY_DOWN);await create_timer(0.25).timeout
        assert(moving and facing==4 and sw_frames.has(sprite.texture))
        travel=body.position-sw_start
        assert(absf(travel.x+travel.y)<0.01 and absf(travel.length()-phase*48)<0.05)
        press(false,KEY_DOWN);await create_timer(0.1).timeout
        assert(moving and facing==-2 and west_frames.has(sprite.texture))
        press(true,KEY_DOWN);press(false,KEY_LEFT);await create_timer(0.1).timeout
        assert(moving and facing==1 and frames.has(sprite.texture))
        press(true,KEY_LEFT);await create_timer(0.1).timeout
        press(false,KEY_LEFT);press(false,KEY_DOWN);await create_timer(0.1).timeout
        assert(not moving and facing==4 and sprite.texture==sw_idle and phase==0)
        press(true,KEY_LEFT);press(true,KEY_DOWN);body.position=Vector2(103,400);await create_timer(0.2).timeout
        assert(not moving and absf(body.position.x-100)<0.001 and absf(body.position.y-403)<0.001)
        body.position=Vector2(400,470);await create_timer(0.1).timeout
        assert(not moving and body.position==Vector2(400,470) and sprite.texture==sw_idle)
        press(false,KEY_LEFT);press(false,KEY_DOWN);body.position=Vector2(320,380)
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(base+"six-direction-playable-godot.png")==OK)
        var ne_start:=body.position
        press(true,KEY_RIGHT);press(true,KEY_UP);await create_timer(0.25).timeout
        assert(moving and facing==5 and ne_frames.has(sprite.texture))
        travel=body.position-ne_start
        assert(travel.x>0 and travel.y<0 and absf(travel.x+travel.y)<0.01 and absf(travel.length()-phase*48)<0.05)
        press(false,KEY_UP);await create_timer(0.1).timeout
        assert(moving and facing==2 and east_frames.has(sprite.texture))
        press(true,KEY_UP);press(false,KEY_RIGHT);await create_timer(0.1).timeout
        assert(moving and facing==-1 and north_frames.has(sprite.texture))
        press(true,KEY_RIGHT);await create_timer(0.1).timeout
        press(false,KEY_RIGHT);press(false,KEY_UP);await create_timer(0.1).timeout
        assert(not moving and facing==5 and sprite.texture==ne_idle and phase==0)
        var ne_stop:=body.position
        press(true,KEY_RIGHT);press(true,KEY_UP);press(true,KEY_DOWN);await create_timer(0.1).timeout
        assert(not moving and body.position==ne_stop)
        press(false,KEY_DOWN);body.position=Vector2(547,400);await create_timer(0.2).timeout
        assert(not moving and body.position.distance_to(Vector2(550,397))<0.001)
        body.position=Vector2(400,333);await create_timer(0.2).timeout
        assert(not moving and body.position.distance_to(Vector2(403,330))<0.001 and sprite.texture==ne_idle)
        body.position=Vector2(400,330);await create_timer(0.1).timeout
        assert(not moving and body.position==Vector2(400,330))
        press(false,KEY_RIGHT);press(false,KEY_UP);body.position=Vector2(320,380)
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(base+"seven-direction-playable-godot.png")==OK)
        var nw_start:=body.position
        press(true,KEY_LEFT);press(true,KEY_UP);await create_timer(0.25).timeout
        assert(moving and facing==6 and nw_frames.has(sprite.texture))
        travel=body.position-nw_start
        assert(travel.x<0 and travel.y<0 and absf(travel.x-travel.y)<0.01 and absf(travel.length()-phase*48)<0.05)
        press(false,KEY_UP);await create_timer(0.1).timeout
        assert(moving and facing==-2 and west_frames.has(sprite.texture))
        press(true,KEY_UP);press(false,KEY_LEFT);await create_timer(0.1).timeout
        assert(moving and facing==-1 and north_frames.has(sprite.texture))
        press(true,KEY_LEFT);await create_timer(0.1).timeout
        press(false,KEY_LEFT);press(false,KEY_UP);await create_timer(0.1).timeout
        assert(not moving and facing==6 and sprite.texture==nw_idle and phase==0)
        var nw_stop:=body.position
        press(true,KEY_LEFT);press(true,KEY_UP);press(true,KEY_DOWN);await create_timer(0.1).timeout
        assert(not moving and body.position==nw_stop)
        press(false,KEY_DOWN);body.position=Vector2(103,400);await create_timer(0.2).timeout
        assert(not moving and body.position.distance_to(Vector2(100,397))<0.001)
        body.position=Vector2(400,333);await create_timer(0.2).timeout
        assert(not moving and body.position.distance_to(Vector2(397,330))<0.001 and sprite.texture==nw_idle)
        body.position=Vector2(400,330);await create_timer(0.1).timeout
        assert(not moving and body.position==Vector2(400,330))
        press(false,KEY_LEFT);press(false,KEY_UP);body.position=Vector2(320,380)
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(base+"eight-direction-playable-godot.png")==OK)
        if OS.get_cmdline_user_args().has("--palette"):
            press(true,KEY_LEFT);await create_timer(0.15).timeout
            press(false,KEY_LEFT);await create_timer(0.1).timeout
            assert(sprite.texture==west_idle and not moving)
            await RenderingServer.frame_post_draw
            assert(root.get_texture().get_image().save_png(base+"palette-playable-godot.png")==OK)
            print("NERIS_PALETTE_PLAYABLE_OK: four hash-checked geometry-preserving replacements")
        driver.set_process(false)
        body.position=Vector2(320,380)
        press(true,KEY_RIGHT);tick(0.125)
        assert(not running and moving and east_frames.has(sprite.texture))
        var run_start:=body.position.x
        press(true,KEY_SHIFT);tick(0.125)
        assert(running and moving and east_run_frames.has(sprite.texture))
        assert(absf(body.position.x-run_start-12)<0.001 and phase==0.125)
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(base+"east-run-playable-godot.png")==OK)
        run_start=body.position.x
        press(false,KEY_SHIFT);tick(0.125)
        assert(not running and east_frames.has(sprite.texture) and phase==0.125)
        assert(absf(body.position.x-run_start-6)<0.001)
        press(true,KEY_SHIFT);tick(0.0625)
        press(false,KEY_RIGHT);tick(0.125)
        assert(not running and not moving and sprite.texture==east_idle and phase==0)
        var held_shift_stop:=body.position
        tick(0.25);assert(body.position==held_shift_stop)
        press(true,KEY_RIGHT);press(true,KEY_UP);tick(0.125)
        assert(not running and facing==5 and ne_frames.has(sprite.texture))
        assert(absf(body.position.distance_to(held_shift_stop)-6)<0.001)
        press(false,KEY_UP);press(true,KEY_LEFT);tick(0.125)
        assert(not moving and not running)
        press(false,KEY_LEFT);body.position=Vector2(549,380);tick(0.125)
        assert(body.position.x==550)
        tick(0.125);assert(not running and not moving and sprite.texture==east_idle)
        press(false,KEY_RIGHT);press(false,KEY_SHIFT);press(true,KEY_R);tick(0.016)
        press(false,KEY_R);assert(body.position==Vector2(320,380) and shadow.position==Vector2.ZERO)
        print("NERIS_EAST_RUN_PLAYABLE_OK: Shift switching, 48px/s run, 24px/s walk, idle, diagonal fallback, conflicts and boundary")
        body.position=Vector2(320,380)
        press(true,KEY_LEFT);press(true,KEY_SHIFT);tick(0.125)
        assert(running and facing==-2 and west_run_frames.has(sprite.texture))
        assert(absf(body.position.x-308)<0.001)
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(base+"west-run-playable-godot.png")==OK)
        press(false,KEY_SHIFT);var west_run_x:=body.position.x;tick(0.125)
        assert(not running and west_frames.has(sprite.texture) and absf(body.position.x-west_run_x+6)<0.001)
        press(true,KEY_SHIFT);press(false,KEY_LEFT);press(true,KEY_RIGHT);tick(0.125)
        assert(running and facing==2 and east_run_frames.has(sprite.texture) and phase==0.125)
        press(false,KEY_RIGHT);press(true,KEY_LEFT);press(true,KEY_UP);var diagonal_start:=body.position;tick(0.125)
        assert(not running and facing==6 and nw_frames.has(sprite.texture))
        assert(absf(body.position.distance_to(diagonal_start)-6)<0.001)
        press(false,KEY_UP);tick(0.125)
        assert(running and facing==-2 and west_run_frames.has(sprite.texture))
        press(false,KEY_LEFT);tick(0.125)
        assert(not moving and not running and sprite.texture==west_idle and phase==0)
        press(true,KEY_LEFT);body.position=Vector2(101,380);tick(0.125);tick(0.125)
        assert(body.position.x==100 and not moving and not running and sprite.texture==west_idle)
        press(false,KEY_LEFT);press(false,KEY_SHIFT);body.position=Vector2(320,380)
        print("NERIS_WEST_RUN_PLAYABLE_OK: left run, release, east switch, diagonal fallback, idle and boundary")
        print("NERIS_PLAYABLE_OK: S/N/E/W/SE/SW/NE/NW movement at24px/s, facing idle, axis conflicts, reset, boundaries and shadow verified")
        quit()
func press(value:bool,key:int=KEY_SPACE)->void:
    var event:=InputEventKey.new();event.keycode=key;event.pressed=value;Input.parse_input_event(event);Input.flush_buffered_events()
