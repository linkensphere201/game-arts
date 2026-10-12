extends SceneTree
## Export and round-trip the native editor terrain resource.
const BITS := [TileSet.CELL_NEIGHBOR_TOP_LEFT_CORNER,TileSet.CELL_NEIGHBOR_TOP_RIGHT_CORNER,TileSet.CELL_NEIGHBOR_BOTTOM_LEFT_CORNER,TileSet.CELL_NEIGHBOR_BOTTOM_RIGHT_CORNER]
func _initialize():
    var tiles := TileSet.new()
    tiles.tile_size=Vector2i(32,32)
    tiles.add_terrain_set()
    tiles.set_terrain_set_mode(0,TileSet.TERRAIN_MODE_MATCH_CORNERS)
    tiles.add_terrain(0)
    tiles.set_terrain_name(0,0,"Paving")
    tiles.set_terrain_color(0,0,Color("bcb198"))
    var atlas := TileSetAtlasSource.new()
    atlas.texture=load("res://mosslight/model_ground/paving-corners.png")
    assert(atlas.texture!=null)
    atlas.texture_region_size=Vector2i(32,32)
    tiles.add_source(atlas,0)
    for code in range(16):
        var at := Vector2i(code%4,code/4)
        atlas.create_tile(at)
        var data := atlas.get_tile_data(at,0)
        data.terrain_set=0
        data.terrain=0 if code else -1
        for i in range(4):data.set_terrain_peering_bit(BITS[i],0 if (code&(1<<i)) else -1)
    var path := "res://mosslight/model_ground/paving.tres"
    assert(ResourceSaver.save(tiles,path)==OK)
    var restored := ResourceLoader.load(path,"TileSet",ResourceLoader.CACHE_MODE_IGNORE) as TileSet
    assert(restored!=null and restored.get_terrain_set_mode(0)==TileSet.TERRAIN_MODE_MATCH_CORNERS)
    var saved_atlas := restored.get_source(0) as TileSetAtlasSource
    for code in range(16):
        var data := saved_atlas.get_tile_data(Vector2i(code%4,code/4),0)
        for i in range(4):assert(data.get_terrain_peering_bit(BITS[i])==(0 if (code&(1<<i)) else -1))
    var layer := TileMapLayer.new()
    layer.tile_set=restored
    root.add_child(layer)
    var cells: Array[Vector2i]=[]
    for y in range(6):
        for x in range(8):
            if x<3 or y>2:cells.append(Vector2i(x,y))
    layer.set_cells_terrain_connect(cells,0,0,false)
    assert(layer.get_used_cells().size()>=cells.size())
    var checked := 0
    for at in layer.get_used_cells():
        var data := layer.get_cell_tile_data(at)
        assert(data!=null)
        for edge in [Vector2i.RIGHT,Vector2i.DOWN]:
            var other := layer.get_cell_tile_data(at+edge)
            if other==null:continue
            var pairs := [[1,0],[3,2]] if edge==Vector2i.RIGHT else [[2,0],[3,1]]
            for pair in pairs:
                assert(data.get_terrain_peering_bit(BITS[pair[0]])==other.get_terrain_peering_bit(BITS[pair[1]]))
                checked+=1
    print("EDITOR_TERRAIN_QA_OK: saved/reloaded 16 tiles; terrain brush L-shape, ",checked," shared corner checks")
    quit()
