extends SceneTree
func _initialize() -> void:
	call_deferred("build")
func build() -> void:
	root.add_child(load("res://model_world.gd").new())
