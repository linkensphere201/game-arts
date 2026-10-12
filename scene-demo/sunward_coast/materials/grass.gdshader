shader_type spatial;
render_mode cull_disabled;
uniform vec4 root_color : source_color = vec4(0.16, 0.30, 0.07, 1.0);
uniform vec4 tip_color : source_color = vec4(0.57, 0.68, 0.22, 1.0);
uniform float wind_strength : hint_range(0.0, 2.0) = 0.8;
// Mesh-local meters: do not use UV.y, which flips during glTF export.
uniform float blade_max_height = 0.55;
uniform float wind_time_override = -1.0;
varying float blade_height;
void vertex() {
    blade_height = clamp(VERTEX.y / blade_max_height, 0.0, 1.0);
    float bend_weight = blade_height * blade_height;
    float wind_time = wind_time_override < 0.0 ? TIME : wind_time_override;
    vec3 world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
    float breeze = sin(world.x * 0.48 + world.z * 0.27 + wind_time * 1.7);
    VERTEX.x += breeze * bend_weight * 0.12 * wind_strength;
    VERTEX.z += cos(world.z * 0.36 + wind_time * 1.3) * bend_weight * 0.05 * wind_strength;
}
void fragment() {
    ALBEDO = mix(root_color.rgb, tip_color.rgb, blade_height) * COLOR.rgb;
    ROUGHNESS = 0.95;
    NORMAL = FRONT_FACING ? NORMAL : -NORMAL;
}
