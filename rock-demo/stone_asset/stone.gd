@tool
extends Node3D
## Style stays outside the imported GLB and survives geometry reimport.
@export var material: Material:
	set(value):
		material = value
		if is_inside_tree(): apply(self)
func _ready() -> void:
	apply(self)
func apply(node: Node) -> void:
	if node is MeshInstance3D: node.material_override = material
	for child in node.get_children(): apply(child)
