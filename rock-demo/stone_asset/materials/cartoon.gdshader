shader_type spatial;
render_mode diffuse_toon, specular_toon;
uniform sampler2D albedo_map : source_color, filter_linear_mipmap;
uniform sampler2D normal_map : hint_normal, filter_linear_mipmap;
uniform sampler2D roughness_map : filter_linear_mipmap;
uniform vec4 shadow_tint : source_color = vec4(0.20, 0.25, 0.32, 1.0);
uniform vec4 light_tint : source_color = vec4(0.59, 0.56, 0.46, 1.0);
void fragment() {
    vec3 color = texture(albedo_map, UV).rgb;
    float value = dot(color, vec3(0.2126,0.7152,0.0722));
    float regions = 0.25 + 0.28 * smoothstep(0.12, 0.15, value)
        + 0.30 * smoothstep(0.22, 0.25, value) + 0.17 * smoothstep(0.33, 0.36, value);
    ALBEDO = mix(shadow_tint.rgb, light_tint.rgb, regions);
    NORMAL_MAP = texture(normal_map, UV).rgb;
    NORMAL_MAP_DEPTH = 0.25;
    ROUGHNESS = mix(0.8, 0.96, texture(roughness_map, UV).r);
    METALLIC = 0.0;
    SPECULAR = 0.25;
}
