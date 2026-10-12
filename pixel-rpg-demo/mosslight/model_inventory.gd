extends PanelContainer
## Reusable asset browser: selection/description only, not gameplay inventory state.
signal selection_changed(item_id: String)
const ITEMS := [
	["sword","Sword","A simple traveler's blade."],
	["shield","Shield","A teal shield with a brass rim."],
	["herb","Herb","Leaves for an alchemist's supplies."],
	["coin","Coin","A brass coin bearing a diamond mark."],
	["potion","Potion","A small bottle of teal liquid."],
	["crystal","Crystal","A faceted crystal for a mage's supplies."],
	["book","Book","A bound book with a decorated cover."],
	["key","Key","A brass key with a round bow."],
	["scroll","Scroll","Parchment tied with a teal ribbon."],
	["bread","Bread","A small loaf for the journey."],
	["pouch","Pouch","A leather pouch tied with teal cord."],
	["axe","Hand axe","A travel axe with a teal-wrapped wooden grip."],
	["ring","Gem ring","An antique brass ring set with a teal gem."],
	["mushroom","Mushroom","A woodland ingredient for crafting recipes."],
]
var buttons:Array[Button]=[]
var selected_id:=""
var details:Label

func _ready() -> void:
	theme=load("res://mosslight/model_ui/theme.tres")
	texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	custom_minimum_size=Vector2(398,242)
	var column:=VBoxContainer.new()
	column.add_theme_constant_override("separation",6)
	add_child(column)
	var title:=Label.new()
	title.text="Item collection"
	title.add_theme_color_override("font_color",Color("f2e8cb"))
	column.add_child(title)
	var grid:=GridContainer.new()
	grid.columns=6
	grid.add_theme_constant_override("h_separation",4)
	grid.add_theme_constant_override("v_separation",4)
	column.add_child(grid)
	for i in range(ITEMS.size()):
		var button:=Button.new()
		button.icon=load("res://mosslight/model_review/"+ITEMS[i][0]+".png")
		assert(button.icon!=null and button.icon.get_size()==Vector2(32,32))
		button.custom_minimum_size=Vector2(56,56)
		button.toggle_mode=true
		button.tooltip_text=ITEMS[i][1]
		button.pressed.connect(select.bind(i))
		grid.add_child(button);buttons.append(button)
	details=Label.new()
	details.custom_minimum_size=Vector2(370,55)
	details.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	details.add_theme_color_override("font_color",Color("f2e8cb"))
	column.add_child(details)
	select(0)

func select(index:int) -> void:
	assert(index>=0 and index<ITEMS.size())
	for i in range(buttons.size()):buttons[i].set_pressed_no_signal(i==index)
	selected_id=ITEMS[index][0]
	details.text=ITEMS[index][1]+"\n"+ITEMS[index][2]
	selection_changed.emit(selected_id)

func _unhandled_key_input(event:InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode==KEY_ESCAPE:
		var owner:=get_viewport().gui_get_focus_owner()
		if owner!=null and is_ancestor_of(owner):
			owner.release_focus()
			get_viewport().set_input_as_handled()
