shader_type spatial;
uniform float detail_strength : hint_range(0.0, 1.0) = 0.35;
varying vec3 local_position;
float hash21(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
float noise2(vec2 p) {
    vec2 i=floor(p), f=fract(p); f=f*f*(3.0-2.0*f);
    return mix(mix(hash21(i),hash21(i+vec2(1,0)),f.x),mix(hash21(i+vec2(0,1)),hash21(i+vec2(1,1)),f.x),f.y);
}
void vertex() { local_position=VERTEX; }
void fragment() {
    float broad=noise2(local_position.xz*0.6);
    float fine=noise2(local_position.xz*12.0);
    float camera_distance=length(VERTEX);
    float fade=1.0-smoothstep(8.0,45.0,camera_distance);
    float shore=-7.0+2.5*sin(local_position.x*0.13)+1.1*sin(local_position.x*0.31);
    float beach=local_position.z-shore;
    float wet=(1.0-smoothstep(1.2,3.6,beach));
    ALBEDO=COLOR.rgb*(1.0+detail_strength*((broad-0.5)*0.32+(fine-0.5)*0.13*fade));
    ALBEDO=mix(ALBEDO,ALBEDO*vec3(0.67,0.72,0.76),wet*0.65);
    ROUGHNESS=mix(0.96,0.55,wet);
}
