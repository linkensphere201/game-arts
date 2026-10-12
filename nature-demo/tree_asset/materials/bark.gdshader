shader_type spatial;
uniform sampler2D color_map : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D normal_map : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D roughness_map : filter_linear_mipmap, repeat_enable;
uniform float wind_strength = 0.65;
uniform float wind_time_override = -1.0;
uniform float normal_strength = 0.4;
void vertex() {
    float h=clamp(VERTEX.y/5.3,0.0,1.0);
    float t=wind_time_override<0.0 ? TIME : wind_time_override;
    float gust=sin(t*1.1+MODEL_MATRIX[3].x*.5);
    vec2 push=vec2(.08,.035)*gust*wind_strength;
    VERTEX.xz+=push*h*h;
    NORMAL.y-=dot(NORMAL.xz,push)*(2.0*h/5.3);
    NORMAL=normalize(NORMAL);
}
void fragment() {
    ALBEDO=texture(color_map,UV).rgb;
    NORMAL_MAP=texture(normal_map,UV).rgb;
    NORMAL_MAP_DEPTH=normal_strength;
    ROUGHNESS=texture(roughness_map,UV).r;
}
