extends Node2D
## Rectangular cutaway room: width in 256px bays, depth in 32px floor rows.
@export_range(1,8) var bays:int=3
@export_range(2,32) var depth:int=14
var modules:Array[Node2D]=[]

func piece(id:String,at:Vector2) -> void:
	var node=load("res://mosslight/timber_kit/"+id+".tscn").instantiate()
	node.position=at;add_child(node);modules.append(node)

func _ready() -> void:
	texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	var width:=bays*256
	var height:=depth*32
	var floor_rect:=TextureRect.new()
	floor_rect.texture=load("res://mosslight/model_ground/wood.png")
	floor_rect.size=Vector2(width,height)
	floor_rect.stretch_mode=TextureRect.STRETCH_TILE
	add_child(floor_rect)
	for x in range(bays):piece("back",Vector2(x*256,-128))
	piece("corner_left",Vector2(-16,-128))
	piece("corner_right",Vector2(width,-128))
	for y in range(depth):
		piece("side",Vector2(-16,y*32))
		piece("side",Vector2(width,y*32))
	for x in range(bays*8):piece("front",Vector2(x*32,height))
	piece("front_corner",Vector2(-16,height))
	piece("front_corner",Vector2(width,height))
