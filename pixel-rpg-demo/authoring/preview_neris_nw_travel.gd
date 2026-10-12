extends SceneTree
class Driver extends Node:
    var tick:Callable
    func _process(delta:float)->void:tick.call(delta)
var compact:=true
var elapsed:=0.0
var actors:Array[Sprite2D]=[]
var markers:Array[ColorRect]=[]
var frames:Array=[]
var trace:Array=[]
var manifest:Dictionary
func _initialize()->void:call_deferred("review")
func tick(delta:float)->void:
    elapsed+=delta
    var slot:=int(elapsed*float(manifest.fps));var frame:=slot%8;var row:Dictionary={"time":elapsed,"frame":frame,"stance":slot/4}
    for i in range(2):
        var velocity:=Vector2(float(manifest.velocity[0]),float(manifest.velocity[1]))
        actors[i].position=Vector2(350,140+i*305)+elapsed*velocity*2.0
        actors[i].texture=frames[i][frame]
        var anchor:Array=manifest.frames[frame].original_anchor if i==0 else manifest.frames[frame].corrected_anchor
        markers[i].position=actors[i].position+Vector2(anchor[0],anchor[1])*2.0
        var world:=(markers[i].position-Vector2(350,140+i*305))/2.0
        row["original" if i==0 else "calibrated"]=[world.x,world.y]
    trace.append(row)
func review()->void:
    root.size=Vector2i(760,780);root.content_scale_size=root.size
    var base:=ProjectSettings.globalize_path("res://../production/pixel-rpg/model-wave-01/guided/neris-NW-travel/")

    manifest=JSON.parse_string(FileAccess.get_file_as_string(base+"manifest.json"))
    var bg:=ColorRect.new();bg.size=Vector2(760,780);bg.color=Color("ded8c7");root.add_child(bg)
    for x in range(20,750,32):
        var line:=ColorRect.new();line.position=Vector2(x,40);line.size=Vector2(1,700);line.color=Color("c4bfaf");root.add_child(line)
    for i in range(2):
        var sheet:=Image.load_from_file(base+(["original.png","calibrated.png"][i]));var cells:Array=[]
        for n in range(8):
            var pixels:=sheet.get_region(Rect2i(n*96,0,96,144))
            var anchor:Array=manifest.frames[n].original_anchor if i==0 else manifest.frames[n].corrected_anchor
            assert(pixels.get_pixel(anchor[0],anchor[1]).a==1)
            cells.append(ImageTexture.create_from_image(pixels))
        frames.append(cells)
        var label:=Label.new();label.text=["NW original / total speed 24 px/s","NW two-axis correction / same speed"][i];label.position=Vector2(20,40+i*305);label.add_theme_color_override("font_color",Color("33352e"));root.add_child(label)
        var actor:=Sprite2D.new();actor.centered=false;actor.scale=Vector2(2,2);actor.position=Vector2(30,45+i*305);actor.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(actor);actors.append(actor)
        var marker:=ColorRect.new();marker.size=Vector2(4,3);marker.color=Color("d76541");root.add_child(marker);markers.append(marker)
    var driver:=Driver.new();driver.tick=tick;root.add_child(driver)
    for i in range(32):
        await create_timer(0.0833).timeout
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(base+"travel-%02d.png"%i)==OK)
    driver.set_process(false)
    var file:=FileAccess.open(base+"runtime-trace.json",FileAccess.WRITE);file.store_string(JSON.stringify(trace));file.close()
    assert(elapsed>2 and actors[1].position.x<283 and actors[1].position.y<378)
    print("NERIS_NW_TRAVEL_OK: measured actual northwest movement and pixel heel anchors")
    quit()
