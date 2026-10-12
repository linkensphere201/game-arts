extends Node2D
## Pixel-stepped contact shadow. Place in a ground layer below Y-sorted objects.
@export var half_size := Vector2(20, 6)
@export_range(0.0, 1.0) var opacity := 0.20

func _draw() -> void:
	# Three nested silhouettes soften the edge without filtered image pixels.
	for layer in range(3):
		var factor := 1.0-float(layer)*0.21
		var radius_x := maxf(1.0, half_size.x*factor)
		var radius_y := maxi(1, roundi(half_size.y*factor))
		for y in range(-radius_y, radius_y):
			var normalized := (float(y)+0.5)/float(radius_y)
			var span := maxi(1, roundi(radius_x*sqrt(maxf(0.0,1.0-normalized*normalized))))
			draw_rect(Rect2(-span,y,span*2,1),Color(0.10,0.15,0.12,opacity*0.5))
