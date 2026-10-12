@tool
extends Node3D
@export var bark_material: Material
@export var leaf_material: Material
@export_range(0.0,2.0,0.05) var wind_strength := 0.65:
	set(value):
		wind_strength=value
		if _bark: _bark.set_shader_parameter("wind_strength",value)
		if _leaves: _leaves.set_shader_parameter("wind_strength",value)
@export_range(8.0,80.0,1.0) var lod_distance := 28.0
var _bark: ShaderMaterial
var _leaves: ShaderMaterial
func _ready() -> void:
	_bark=bark_material.duplicate() as ShaderMaterial
	_leaves=leaf_material.duplicate() as ShaderMaterial
	_bark.set_shader_parameter("wind_strength",wind_strength)
	_leaves.set_shader_parameter("wind_strength",wind_strength)
	apply($Near,false)
	apply($Far,true)
func apply(node: Node, far_model: bool) -> void:
	if node is MeshInstance3D:
		node.material_override=_bark if node.name.begins_with("Bark") else _leaves
		if far_model: node.visibility_range_begin=lod_distance
		else: node.visibility_range_end=lod_distance
	for child in node.get_children(): apply(child,far_model)
