extends SceneTree
## Native theme derived from the local-model panel; no additional generated art count.
func _initialize() -> void:
	var panel:=load("res://mosslight/model_ui/panel.tres") as StyleBoxTexture
	assert(panel!=null)
	var theme:=Theme.new()
	theme.set_stylebox("panel","Panel",panel)
	theme.set_stylebox("panel","PanelContainer",panel)
	var colors:={"normal":Color.WHITE,"hover":Color(1.15,1.15,1.10),"pressed":Color(.75,.85,.80),"disabled":Color(.60,.64,.62)}
	for state in colors:
		var box:=panel.duplicate() as StyleBoxTexture
		box.modulate_color=colors[state]
		theme.set_stylebox(state,"Button",box)
	var focus:=StyleBoxFlat.new()
	focus.bg_color=Color.TRANSPARENT
	focus.border_color=Color("e4cf8a")
	focus.set_border_width_all(2)
	focus.set_expand_margin_all(2)
	theme.set_stylebox("focus","Button",focus)
	for state in ["font_color","font_hover_color","font_pressed_color","font_focus_color"]:
		theme.set_color(state,"Button",Color("f2e8cb"))
	theme.set_color("font_disabled_color","Button",Color("9aab9f"))
	theme.set_font_size("font_size","Button",18)
	var error:=ResourceSaver.save(theme,"res://mosslight/model_ui/theme.tres",ResourceSaver.FLAG_RELATIVE_PATHS)
	assert(error==OK)
	# This engine build retains res:// references despite FLAG_RELATIVE_PATHS.
	var path:="res://mosslight/model_ui/theme.tres"
	var text:=FileAccess.get_file_as_string(path)
	text=text.replace("path=\"res://mosslight/model_ui/","path=\"")
	assert(not text.contains("res://"),"Unexpected nonlocal theme dependency")
	var file:=FileAccess.open(path,FileAccess.WRITE)
	assert(file!=null)
	file.store_string(text)
	file.close()
	print("UI_THEME_EXPORT_OK: panel + four button states and visible keyboard focus")
	quit()
