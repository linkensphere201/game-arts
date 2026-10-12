extends SceneTree
class MotionDriver extends Node:
    var tick:Callable
    func _process(delta:float)->void:tick.call(delta)
var rear:=OS.get_cmdline_user_args().has("--rear")
var contact:=OS.get_cmdline_user_args().has("--contact")
var weighted:=OS.get_cmdline_user_args().has("--weight") or contact
var elapsed:=0.0
var actors:Array[Sprite2D]=[]
var markers:Array[ColorRect]=[]
var textures:Array=[]
var manifest:Dictionary
var trace:Array=[]
func _initialize()->void:call_deferred("review")
func tick(delta:float)->void:
    elapsed+=delta
    var absolute:=int(floor(elapsed*float(manifest.fps)))
    var frame:=absolute%8
    var entry:Dictionary=manifest.frames[frame]
    var world_feet:Array=[]
    for i in range(2):
        actors[i].texture=textures[i][frame]
        actors[i].position=Vector2(64+i*320,(200 if rear else 70)+elapsed*float(manifest.speed)*2)
        var sole:float=entry.naive_sole if i==0 and not weighted else entry.locked_sole
        var x:=39 if entry.support=="left" else 55
        markers[i].position=actors[i].position+Vector2(x*2,sole*2)
        world_feet.append((markers[i].position.y-(200 if rear else 70))/2)
    trace.append({"time":elapsed,"frame":frame,"stance":absolute/4,"naive_y":world_feet[0],"locked_y":world_feet[1]})
func review()->void:
    root.size=Vector2i(640,550);root.content_scale_size=root.size
    var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/neris-stance/")
    if rear:base=base.replace("neris-stance/","neris-rear-stance/")
    manifest=JSON.parse_string(FileAccess.get_file_as_string(base+"manifest.json"))
    var bg:=ColorRect.new();bg.size=Vector2(640,550);bg.color=Color("ded8c7");root.add_child(bg)
    for y in range(80,490,32):
        var line:=ColorRect.new();line.position=Vector2(0,y);line.size=Vector2(640,1);line.color=Color("c4bfaf");root.add_child(line)
    for i in range(2):
        var sheet:=Image.load_from_file(base+((["weighted.png","coordinated-weighted.png"] if contact else ["locked.png","weighted.png"] if weighted else ["naive.png","locked.png"])[i]))
        assert(sheet!=null and sheet.get_size()==Vector2i(768,144))
        var frames:Array=[]
        for n in range(8):
            var pixels:=sheet.get_region(Rect2i(n*96,0,96,144))
            var entry:Dictionary=manifest.frames[n]
            var x0:=28 if entry.support=="left" else 49
            var x1:=48 if entry.support=="left" else 68
            var sole:=100+pixels.get_region(Rect2i(x0,100,x1-x0,44)).get_used_rect().end.y
            assert(sole==int(entry.naive_sole if i==0 and not weighted else entry.locked_sole))
            frames.append(ImageTexture.create_from_image(pixels))
        textures.append(frames)
        var label:=Label.new();label.text=(["Previous contact arms","Coordinated contact arms"] if contact else ["Fixed torso / locked foot","Torso sway / same locked foot"] if weighted else ["Forward travel / no correction","Support foot corrected"])[i];label.position=Vector2(20+i*320,20);label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
        var actor:=Sprite2D.new();actor.centered=false;actor.scale=Vector2(2,2);actor.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(actor);actors.append(actor)
        var marker:=ColorRect.new();marker.size=Vector2(4,3);marker.color=Color("d76541") if i==0 else Color("26785a");root.add_child(marker);markers.append(marker)
    var note:=Label.new();note.text="24 px/s, 12 fps. Markers follow support soles. Gait art remains unapproved.";note.position=Vector2(10,515);note.add_theme_color_override("font_color",Color("33352e"));root.add_child(note)
    var driver:=MotionDriver.new();driver.tick=tick;root.add_child(driver)
    for i in range(32):
        await create_timer(0.0833).timeout
        await RenderingServer.frame_post_draw
        var error:=root.get_texture().get_image().save_png(base+("contact-travel-%02d.png" if contact else "weight-travel-%02d.png" if weighted else "travel-%02d.png")%i);assert(error==OK)
    driver.set_process(false)
    var file:=FileAccess.open(base+("contact-runtime-trace.json" if contact else "weight-runtime-trace.json" if weighted else "runtime-trace.json"),FileAccess.WRITE);assert(file!=null);file.store_string(JSON.stringify(trace));file.close()
    assert(elapsed>2.0)
    assert(actors[0].position.y<104 if rear else actors[0].position.y>166)
    print("NERIS_TRAVEL_CAPTURE_OK: actual forward travel and pixel-verified support soles recorded")
    quit()
