extends SceneTree
## M3.4.3: exercise imported collision, a walking capsule, and camera controls.
var failures: Array[String] = []

func check(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
		printerr("FAIL ",message)

func _initialize() -> void:
	call_deferred("run_checks")

func run_checks() -> void:
	var demo: Node3D = load("res://levels/coast.tscn").instantiate()
	root.add_child(demo)
	await physics_frame
	await physics_frame
	var camera: Camera3D = demo.get_node("Camera")
	var first := camera.position
	var key := InputEventKey.new()
	key.keycode = KEY_2
	key.pressed = true
	demo._unhandled_input(key)
	check(camera.position.distance_to(first) > 5.0,"Viewpoint 2 must change camera")
	key.keycode = KEY_H
	demo._unhandled_input(key)
	check(not demo.hud.visible,"H hides interface")
	demo._unhandled_input(key)
	check(demo.hud.visible,"H restores interface")
	var space := demo.get_world_3d().direct_space_state
	var hits := 0
	for z in [1.0,5.0,9.0,13.0,17.0]:
		for x in [-10.0,0.0,6.0,10.0]:
			var ray := PhysicsRayQueryParameters3D.create(Vector3(x,30,z),Vector3(x,-5,z))
			var hit := space.intersect_ray(ray)
			check(not hit.is_empty(),"Ground collision at %s,%s"%[x,z])
			if not hit.is_empty():
				hits += 1
				check(hit.normal.y > 0.6,"Ground normal faces up")
	var player := CharacterBody3D.new()
	var collider := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.3
	capsule.height = 1.8
	collider.shape = capsule
	player.add_child(collider)
	root.add_child(player)
	player.position = Vector3(3.3,6.0,15.0)
	player.floor_snap_length = 0.4
	var grounded := 0
	var min_y := 100.0
	for i in range(600):
		await physics_frame
		var desired_x := 2.0+2.0*sin((player.position.z-0.5)*0.17)
		player.velocity.x = clampf((desired_x-player.position.x)*2.0,-2,2)
		player.velocity.z = -1.4
		player.velocity.y -= 18.0/60.0
		player.move_and_slide()
		if i > 90 and player.is_on_floor(): grounded += 1
		min_y = minf(min_y,player.position.y)
	check(player.position.z < 2.0,"Capsule traverses at least 13m toward beach")
	check(min_y > 0.8,"Capsule does not fall through terrain")
	check(grounded > 450,"Capsule remains grounded on rolling terrain")
	print("COAST_VALIDATION ",JSON.stringify({"ray_hits":hits,"capsule_final":str(player.position),"grounded_frames":grounded,"minimum_y":min_y,"failures":failures}))
	quit(0 if failures.is_empty() else 1)
