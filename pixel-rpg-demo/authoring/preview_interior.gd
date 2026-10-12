extends SceneTree
## Standalone interactive furniture room entry point.
func _initialize() -> void:
    call_deferred("build")
func build() -> void:
    root.add_child(load("res://model_interior.gd").new())
