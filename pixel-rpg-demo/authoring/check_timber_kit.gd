extends SceneTree
func _initialize() -> void:call_deferred("check")
func check() -> void:
	for dims in [Vector2i(1,6),Vector2i(3,14)]:
		var room=load("res://mosslight/timber_room.gd").new()
		room.bays=dims.x;room.depth=dims.y;room.position=Vector2(200,200)
		root.add_child(room)
		await physics_frame
		await physics_frame
		var width:int=dims.x*256
		var height:int=dims.y*32
		# Probe seams and corners, not just module centers.
		var blocked=[Vector2(-8,0),Vector2(-8,32),Vector2(width+8,32),Vector2(-8,height+8),Vector2(width+8,height+8),Vector2(32,height+8),Vector2(width/2.0,-8)]
		for local in blocked:
			var query:=PhysicsPointQueryParameters2D.new();query.position=room.position+local
			assert(not room.get_world_2d().direct_space_state.intersect_point(query).is_empty(),"Wall seam open: "+str(local))
		var query:=PhysicsPointQueryParameters2D.new();query.position=room.position+Vector2(width/2.0,height/2.0)
		assert(room.get_world_2d().direct_space_state.intersect_point(query).is_empty(),"Floor blocked")
		room.queue_free()
		await process_frame
	print("TIMBER_KIT_QA_OK: two room dimensions, back/side/front seams, corners, open floor")
	quit()
