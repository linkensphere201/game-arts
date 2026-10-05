shader_type spatial;
render_mode cull_disabled;
uniform vec4 root_color : source_color = vec4(0.16, 0.30, 0.07, 1.0);
uniform vec4 tip_color : source_color = vec4(0.57, 0.68, 0.22, 1.0);
varying float blade_height;
void vertex() {
    blade_height = UV.y;
    vec3 world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
    float breeze = sin(world.x * 0.48 + world.z * 0.27 + TIME * 1.7);
    VERTEX.x += breeze * UV.y * UV.y * 0.12;
    VERTEX.z += cos(world.z * 0.36 + TIME * 1.3) * UV.y * UV.y * 0.05;
}
void fragment() {
    ALBEDO = mix(root_color.rgb, tip_color.rgb, blade_height) * COLOR.rgb;
    ROUGHNESS = 0.95;
    NORMAL = FRONT_FACING ? NORMAL : -NORMAL;
}
