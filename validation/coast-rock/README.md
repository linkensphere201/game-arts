# M3.6.1 grass validation

The production GLB has UV.y=1 at its 14 root vertices. Previous shader UV.y-squared weights therefore moved roots. Production wind now uses squared clamped mesh-local height (Y/0.55), giving zero displacement at root height regardless of time. This parameter is specific to the current 0.55 m tuft mesh.

`validate_grass_wind.gd` loads the real imported mesh and production shader, verifies root weights, then renders fixed times 0.0 and 1.5 at double wind strength. Captures `wind-0.0.png` and `wind-1.5.png` were inspected: root contacts stay on the fixed baseline while upper blades shift. Rendered frames differ. `wind-check-host.log`, `import.log` and `export.log` pass without reported errors. This checks deformation/root anchoring, not a physically simulated grass model.

The initial sandbox run had log/certificate/cache permission errors; host retry succeeded. Separate rock bake logs contain an exporter temp-directory permission failure, not a delivered realistic asset. Original runtime limestone remains in place. The user clarified rock work as exploratory and requested recording two future art routes. No real-rock sample or full material conversion is claimed.
