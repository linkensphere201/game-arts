# Model-derived furniture studies

Drag `table.tscn`, `bookshelf.tscn`, `chair.tscn` or `bed.tscn` into a Godot 4 scene. Each includes its texture, nearest filtering and a StaticBody2D floor footprint on physics layer 1. Place their roots alongside the character under a Node2D with Y Sort Enabled. Root position is the bottom-center ground anchor. Keep scale at 1 for native pixels.

Copy this folder together with its sibling `model_review` folder; these four scenes only need the corresponding four PNGs. Texture references are relative, so the parent folder can be renamed or nested. They have no dependency on the demo scripts, model server, Python or internet at runtime. Collision shapes remain editable in Godot.

These are static art studies, without sitting/sleeping actions. Art acceptance, consistent camera/pixel density and broader furnishing coverage remain pending. Multiple placements do not count as distinct designs.

Rebuild generated scenes using `authoring/export_furniture_scenes.py` after producing the four source sprites. Sources and documentation are tracked; generated PNG/TSCN resources remain local under the repository's publication policy.
