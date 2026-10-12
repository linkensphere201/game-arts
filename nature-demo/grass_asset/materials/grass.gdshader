shader_type spatial;
render_mode cull_disabled;
uniform sampler2D color_map : source_color, filter_linear_mipmap;
uniform sampler2D normal_map : hint_normal, filter_linear_mipmap;
uniform vec4 tint : source_color = vec4(1.0);
uniform float wind_strength : hint_range(0.0,2.0) = 0.65;
uniform float wind_time_override = -1.0;
uniform float normal_strength = 0.25;
varying float bend;
void vertex() {
    // UV2.x is explicit root-to-tip weight, independent of texture UV and blade height.
    bend=clamp(UV2.x,0.0,1.0);
    float blade_height=max(1.0-UV2.y,0.01); // glTF V flip for the auxiliary height channel.
    vec3 anchor=MODEL_MATRIX[3].xyz;
    float t=wind_time_override < 0.0 ? TIME : wind_time_override;
    float gust=sin(anchor.x*1.7+anchor.z*0.6+t*1.7)*0.7+sin(t*0.7+anchor.z)*0.3;
    vec2 push=vec2(0.075,0.028)*gust*wind_strength;
    VERTEX.xz+=push*bend*bend;
    // Inverse-transpose of this local shear keeps normals aligned with bending.
    NORMAL.y-=dot(NORMAL.xz,push)*(2.0*bend/blade_height);
    NORMAL=normalize(NORMAL);
}
void fragment() {
    ALBEDO=texture(color_map,UV).rgb*tint.rgb*COLOR.rgb;
    ROUGHNESS=0.88;
    NORMAL_MAP=texture(normal_map,UV).rgb;
    NORMAL_MAP_DEPTH=normal_strength;
    NORMAL=FRONT_FACING ? NORMAL : -NORMAL;
    BACKLIGHT=ALBEDO*0.12;
}
