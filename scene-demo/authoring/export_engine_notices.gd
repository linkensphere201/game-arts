extends SceneTree
func _initialize() -> void:
	var folder := ProjectSettings.globalize_path("res://sunward_coast/docs/")
	DirAccess.make_dir_recursive_absolute(folder)
	var file := FileAccess.open(folder+"GODOT_NOTICES.txt",FileAccess.WRITE)
	file.store_string("Godot Engine " + Engine.get_version_info().string + "\n\n" + Engine.get_license_text())
	file.store_string("\n\nTHIRD-PARTY COPYRIGHTS\n")
	for entry in Engine.get_copyright_info():
		file.store_string("\n"+str(entry)+"\n")
	file.store_string("\n\nTHIRD-PARTY LICENSE TEXTS\n")
	var licenses := Engine.get_license_info()
	for name in licenses:
		file.store_string("\n"+name+"\n"+licenses[name]+"\n")
	file.close()
	print("ENGINE_NOTICES_EXPORTED")
	quit()
