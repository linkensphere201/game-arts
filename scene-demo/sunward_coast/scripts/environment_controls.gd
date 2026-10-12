@tool
extends Node3D
## Settings affect only this environment instance; shared files are never mutated.
@export_category("Environment / 环境")
@export_range(0.2, 1.8, 0.05) var sunlight: float = 0.95:
	set(value):
		sunlight = value
		refresh()
@export_range(-80.0, -10.0, 1.0) var sun_elevation: float = -38.0:
	set(value):
		sun_elevation = value
		refresh()
@export_category("Meadow / 草地")
@export_range(0.2, 1.0, 0.05) var grass_density: float = 1.0:
	set(value):
		grass_density = value
		refresh()
@export_range(10.0, 100.0, 1.0) var grass_distance: float = 55.0:
	set(value):
		grass_distance = value
		refresh()
@export_range(0.0, 2.0, 0.05) var wind_strength: float = 0.8:
	set(value):
		wind_strength = value
		refresh()
@export var grass_tip: Color = Color(0.57,0.68,0.22):
	set(value):
		grass_tip = value
		refresh()
@export_category("Water / 海水")
@export var shallow_water: Color = Color(0.10,0.56,0.49):
	set(value):
		shallow_water = value
		refresh()
@export var deep_water: Color = Color(0.025,0.22,0.34):
	set(value):
		deep_water = value
		refresh()
@export_range(0.0,2.0,0.05) var wave_speed: float = 0.7:
	set(value):
		wave_speed = value
		refresh()
@export_range(0.0,1.0,0.05) var foam_strength: float = 0.72:
	set(value):
		foam_strength = value
		refresh()
var _prepared := false
var _grass_material: ShaderMaterial
var _water_material: ShaderMaterial
var _grass_batches: Array[MultiMeshInstance3D] = []
var _flower_batches: Array[MultiMeshInstance3D] = []

func _ready() -> void:
	var sea := get_node_or_null("Sea") as MeshInstance3D
	if sea == null: return
	_water_material = sea.get_active_material(0).duplicate() as ShaderMaterial
	sea.material_override = _water_material
	var grasses := get_node_or_null("GrassPatches")
	if grasses != null:
		for child in grasses.get_children():
			var batch := child as MultiMeshInstance3D
			if batch == null: continue
			batch.multimesh = batch.multimesh.duplicate()
			if _grass_material == null:
				_grass_material = batch.multimesh.mesh.surface_get_material(0).duplicate() as ShaderMaterial
			batch.material_override = _grass_material
			_grass_batches.append(batch)
	var flowers := get_node_or_null("Wildflowers")
	if flowers != null:
		for child in flowers.get_children():
			if child is MultiMeshInstance3D: _flower_batches.append(child)
	_prepared = true
	refresh()

func refresh() -> void:
	if not _prepared: return
	var sun := get_node_or_null("AfternoonSun") as DirectionalLight3D
	if sun != null:
		sun.light_energy = sunlight
		sun.rotation_degrees.x = sun_elevation
	if _grass_material != null:
		_grass_material.set_shader_parameter("wind_strength",wind_strength)
		_grass_material.set_shader_parameter("tip_color",grass_tip)
	for batch in _grass_batches:
		batch.multimesh.visible_instance_count = int(batch.multimesh.instance_count*grass_density)
		batch.visibility_range_end = grass_distance
		batch.visibility_range_end_margin = 6.0
	for batch in _flower_batches:
		batch.visibility_range_end = grass_distance
	_water_material.set_shader_parameter("shallow_color",shallow_water)
	_water_material.set_shader_parameter("deep_color",deep_water)
	_water_material.set_shader_parameter("wave_speed",wave_speed)
	_water_material.set_shader_parameter("foam_strength",foam_strength)
