# Component catalog

16 props plus one terrain. Dimensions are Blender X/Y/Z (width/depth/height), in meters; Godot uses Y-up. Counts are source geometry, before exporter vertex splitting. They are not rendered scene totals.

| Asset | Vertices | Triangles | Dimensions (m) |
|---|---:|---:|---|
| limestone | 42 | 80 | 2.58 / 1.835 / 1.656 |
| coastal_tree | 742 | 1392 | 4.28 / 3.901 / 5.606 |
| tree_windswept | 742 | 1392 | 4.076 / 3.715 / 5.06 |
| tree_sapling | 742 | 1392 | 2.65 / 2.415 / 3.313 |
| shrub | 210 | 400 | 2.05 / 1.956 / 1.12 |
| grass_tuft | 35 | 21 | 0.452 / 0.363 / 0.55 |
| daisy | 86 | 144 | 0.324 / 0.265 / 0.535 |
| rock_flat | 42 | 80 | 2.121 / 1.721 / 0.561 |
| rock_tall | 42 | 80 | 1.604 / 1.36 / 1.605 |
| shrub_low | 84 | 160 | 2.327 / 1.3 / 0.88 |
| grass_short | 35 | 21 | 0.384 / 0.308 / 0.319 |
| flower_blue | 86 | 144 | 0.324 / 0.265 / 0.722 |
| coastal_bench | 264 | 484 | 2.0 / 0.625 / 1.31 |
| driftwood | 28 | 48 | 1.917 / 0.603 / 0.349 |
| pebbles | 210 | 400 | 0.881 / 0.667 / 0.16 |
| beach_reeds | 35 | 21 | 0.339 / 0.272 / 0.88 |
| terrain | 6521 | 12430 | 40.0 / 36.0 / 5.79 |

The assembled High scene contains 6,202 grass tufts and 184 flowers in spatial MultiMesh batches. Five trees anchor the composition. Ground, water and plants use shared palettes and distance-reduced shader detail. Props use placement origins near their ground contact; irregular terrain/rock bounds are not modular grid tiles. See README.md for collision and reimport limits.
