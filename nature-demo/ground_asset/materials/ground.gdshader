shader_type spatial;
uniform sampler2D turf_color : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D soil_color : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D sand_color : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D turf_normal : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D soil_normal : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D sand_normal : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D turf_roughness : filter_linear_mipmap, repeat_enable;
uniform sampler2D soil_roughness : filter_linear_mipmap, repeat_enable;
uniform sampler2D sand_roughness : filter_linear_mipmap, repeat_enable;
uniform float repeats = 4.0;
uniform float wetness : hint_range(0.0,1.0) = 0.2;
uniform float normal_strength : hint_range(0.0,1.0) = 0.55;
varying vec3 layer_weights;
void vertex() { layer_weights=COLOR.rgb; }
void fragment() {
    vec3 w=max(layer_weights,vec3(0.0)); w/=max(dot(w,vec3(1.0)),0.0001);
    vec2 uv=UV*repeats;
    vec3 color=texture(turf_color,uv).rgb*w.r+texture(soil_color,uv).rgb*w.g+texture(sand_color,uv).rgb*w.b;
    float macro=0.95+0.05*sin(UV.x*17.0+sin(UV.y*11.0));
    float wet=w.b*wetness*smoothstep(0.65,1.0,UV.y);
    ALBEDO=color*macro*(1.0-0.35*wet);
    vec3 n=(texture(turf_normal,uv).rgb*2.0-1.0)*w.r
        +(texture(soil_normal,uv).rgb*2.0-1.0)*w.g+(texture(sand_normal,uv).rgb*2.0-1.0)*w.b;
    NORMAL_MAP=normalize(n)*0.5+0.5; NORMAL_MAP_DEPTH=normal_strength;
    ROUGHNESS=mix(texture(turf_roughness,uv).r*w.r+texture(soil_roughness,uv).r*w.g+texture(sand_roughness,uv).r*w.b,0.48,wet);
}
