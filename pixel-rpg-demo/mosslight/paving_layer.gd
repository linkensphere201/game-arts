extends TileMapLayer
## Reusable 32px corner-connected paving overlay. Underlay grass separately.
func _ready():
    texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
    tile_set=load("res://mosslight/model_ground/paving.tres") as TileSet
    assert(tile_set!=null and tile_set.get_source_count()==1)

func paint_vertices(vertices: Dictionary, bounds: Rect2i):
    # Each tile shares its corner occupancy with adjacent tiles.
    for y in range(bounds.position.y,bounds.end.y):
        for x in range(bounds.position.x,bounds.end.x):
            var code := 0
            var corners := [Vector2i(x,y),Vector2i(x+1,y),Vector2i(x,y+1),Vector2i(x+1,y+1)]
            for i in range(4):
                if vertices.has(corners[i]):code|=1<<i
            set_cell(Vector2i(x,y),0,Vector2i(code%4,code/4))
