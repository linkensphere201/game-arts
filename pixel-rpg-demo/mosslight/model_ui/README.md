# Model-derived interface study

Use `theme.tres` as the Theme of a Godot Control subtree. It supplies the panel background and Button normal, hover, pressed, disabled and keyboard-focus styles. Keep Texture Filter set to Nearest on the subtree. The button states reuse the same model-derived panel with modulation; they are not five independently painted UI assets. Text uses Godot's default font and is not a custom font deliverable.

`panel.tres` can also be assigned directly to a Panel's `panel` style override. Its 96x96 texture uses 12px nine-patch corners and content margins. Use at least 24x24 plus the required content size; avoid scaling the Control node itself. Copy `theme.tres`, `panel.tres` and `panel.png` together: their relative resource paths allow relocating the folder.

Generate the panel with `export_panel_style.py`, then run Godot with `--script res://authoring/export_ui_theme.gd`. Verify with `check_panel_style.gd` and `check_ui_theme.gd`; both accept `--capture=` after `--`.

This is a UI foundation study. Inventory/shop/dialogue flows, additional controls, accessibility review and final art acceptance are unfinished.
