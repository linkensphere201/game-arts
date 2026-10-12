extends SceneTree
## Run in the original project or a fresh project containing only the furniture files.
func _initialize() -> void:
	call_deferred("check")

func check() -> void:
	var directory := "res://mosslight/furniture/"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--furniture-root="):directory=arg.trim_prefix("--furniture-root=")
	var world := Node2D.new()
	world.y_sort_enabled=true
	root.add_child(world)
	var index:=0
	for name in ["table","bookshelf","chair","bed"]:
		var packed:=load(directory+name+".tscn") as PackedScene
		assert(packed!=null,"Native scene cannot be loaded: "+name)
		var instance:=packed.instantiate() as Node2D
		instance.position=Vector2(220+index*240,300)
		world.add_child(instance)
		var sprite:=instance.get_node("Sprite") as Sprite2D
		assert(sprite.texture!=null and instance.texture_filter==CanvasItem.TEXTURE_FILTER_NEAREST)
		var body:=instance.get_node("Body") as StaticBody2D
		await physics_frame
		await physics_frame
		var query:=PhysicsPointQueryParameters2D.new()
		query.position=body.global_position
		query.collision_mask=1
		var hits:=world.get_world_2d().direct_space_state.intersect_point(query)
		assert(hits.size()==1 and hits[0].collider==body,"Missing/wrong footprint for "+name)
		query.position=instance.global_position+Vector2(0,24)
		assert(world.get_world_2d().direct_space_state.intersect_point(query).is_empty(),"Footprint extends beyond feet: "+name)
		index+=1
	print("FURNITURE_IMPORT_QA_OK: four independent native scenes, textures and actual physics footprints")
	quit()
