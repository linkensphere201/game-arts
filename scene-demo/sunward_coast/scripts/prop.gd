@tool
extends Node3D
## Imported model stays linked; engine overrides belong to this wrapper.
@export var surface_override: Material:
	set(value):
		surface_override = value
		if is_inside_tree(): _apply_material(self)

func _ready() -> void:
	_apply_material(self)

func _apply_material(node: Node) -> void:
	if node is MeshInstance3D:
		node.material_override = surface_override
	for child in node.get_children():
		_apply_material(child)
