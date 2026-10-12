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
uniform float repeats = 1.0;
uniform float turf_bias = 0.0;
uniform float edge_breakup = 0.32;
float hash21(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
float noise2(vec2 p) {
    vec2 i=floor(p); vec2 f=fract(p); f=f*f*(3.0-2.0*f);
    return mix(mix(hash21(i),hash21(i+vec2(1,0)),f.x),
        mix(hash21(i+vec2(0,1)),hash21(i+vec2(1,1)),f.x),f.y);
}
uniform float wetness : hint_range(0.0,1.0) = 0.2;
uniform float normal_strength : hint_range(0.0,1.0) = 0.55;
varying vec3 layer_weights;
void vertex() { layer_weights=COLOR.rgb; }
void fragment() {
    vec3 w=max(layer_weights,vec3(0.0)); w/=max(dot(w,vec3(1.0)),0.0001);
    float breakup=(noise2(UV*22.0)-0.5)*edge_breakup;
    float turf=clamp(w.r+turf_bias+breakup,0.0,1.0-w.b);
    w=vec3(turf,max(0.0,1.0-turf-w.b),w.b);
    vec2 uv=UV*repeats;
    vec3 color=texture(turf_color,uv).rgb*w.r+texture(soil_color,uv).rgb*w.g+texture(sand_color,uv).rgb*w.b;
    float macro=0.95+0.05*sin(UV.x*17.0+sin(UV.y*11.0));
    float wet=w.b*wetness*smoothstep(0.65,1.0,UV.y);
    ALBEDO=color*macro*(1.0-0.35*wet);
    vec3 n=(texture(turf_normal,uv).rgb*2.0-1.0)*w.r
        +(texture(soil_normal,uv).rgb*2.0-1.0)*w.g+(texture(sand_normal,uv).rgb*2.0-1.0)*w.b;
    NORMAL_MAP=normalize(n)*0.5+0.5; NORMAL_MAP_DEPTH=normal_strength;
    SPECULAR=0.18;
    ROUGHNESS=mix(texture(turf_roughness,uv).r*w.r+texture(soil_roughness,uv).r*w.g+texture(sand_roughness,uv).r*w.b,0.48,wet);
}
