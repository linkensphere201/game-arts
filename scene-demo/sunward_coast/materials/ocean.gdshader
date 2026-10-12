shader_type spatial;
render_mode cull_disabled;
uniform vec4 shallow_color : source_color = vec4(0.10, 0.56, 0.49, 1.0);
uniform vec4 deep_color : source_color = vec4(0.025, 0.22, 0.34, 1.0);
uniform float wave_speed : hint_range(0.0, 2.0) = 0.7;
uniform float foam_strength : hint_range(0.0, 1.0) = 0.72;
uniform vec2 sea_origin = vec2(0.0, -450.0);
varying vec3 world_pos;
varying vec2 coast_position;
float shoreline(float x) { return -7.0 + 2.5*sin(x*0.13) + 1.1*sin(x*0.31); }
float hash21(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise2(vec2 p) {
    vec2 cell = floor(p);
    vec2 f = fract(p);
    vec2 u = f*f*(3.0-2.0*f);
    return mix(mix(hash21(cell),hash21(cell+vec2(1.0,0.0)),u.x),
               mix(hash21(cell+vec2(0.0,1.0)),hash21(cell+vec2(1.0,1.0)),u.x),u.y);
}
void vertex() {
    world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
    coast_position = VERTEX.xz + sea_origin;
}
void fragment() {
    vec2 p = coast_position;
    float t = TIME * wave_speed;
    float offshore = shoreline(p.x) - p.y + 1.0;
    float broad = noise2(p*0.12 + vec2(t*0.035,-t*0.045));
    float detail = noise2(p*0.85 + vec2(t*0.10,t*0.14));
    float swell = sin(dot(p,vec2(0.65,0.92))+t+broad*3.0);
    float cross_wave = sin(dot(p,vec2(-0.86,0.34))-t*0.73+detail*1.4);
    float distance_to_camera = length(world_pos-CAMERA_POSITION_WORLD);
    float detail_fade = 1.0-smoothstep(25.0,130.0,distance_to_camera);
    vec3 base = mix(shallow_color.rgb,deep_color.rgb,smoothstep(0.0,45.0,offshore));
    base *= 0.94 + 0.12*broad;
    // One irregular advancing front, with small remnants behind it.
    float front = 0.55 + 0.55*sin(t*0.85+p.x*0.08) + (broad-0.5)*0.85;
    float width = 0.10 + detail*0.23;
    float edge = 1.0-smoothstep(width,width+0.16,abs(offshore-front));
    float breakup = smoothstep(0.28,0.65,noise2(vec2(p.x*1.45,offshore*2.1-t*0.25)));
    float wash = smoothstep(0.68,0.85,detail)*(1.0-smoothstep(0.8,3.0,offshore))*0.25;
    float foam = (edge*breakup+wash)*smoothstep(-0.3,0.25,offshore);
    float highlight = smoothstep(0.78,0.99,swell*cross_wave)*0.045*detail_fade;
    ALBEDO = mix(base+highlight,vec3(0.89,0.95,0.88),clamp(foam*foam_strength,0.0,1.0));
    NORMAL_MAP = vec3(0.5+swell*0.045*detail_fade,0.5+cross_wave*0.035*detail_fade,1.0);
    ROUGHNESS = mix(0.38,0.7,clamp(foam,0.0,1.0));
    SPECULAR = 0.35;
}
