shader_type spatial;
render_mode cull_disabled;
varying vec3 world_pos;
float shoreline(float x) { return -7.0 + 2.5*sin(x*0.13) + 1.1*sin(x*0.31); }
void vertex() {
    world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}
void fragment() {
    float offshore = shoreline(world_pos.x) - world_pos.z - 0.5;
    float ripple = sin(world_pos.x*1.1 + world_pos.z*1.9 + TIME*1.4)
        * sin(world_pos.x*0.63-world_pos.z*1.2+TIME*0.8);
    vec3 shallow = vec3(0.12, 0.64, 0.57);
    vec3 deep = vec3(0.025, 0.26, 0.39);
    ALBEDO = mix(shallow, deep, smoothstep(1.0, 65.0, offshore));
    float band = sin(offshore*2.2 - TIME*1.5 + sin(world_pos.x*1.4)*0.24);
    float foam = smoothstep(0.87, 1.0, band) * (1.0-smoothstep(0.0, 5.0, offshore));
    foam *= smoothstep(-1.0, 0.4, offshore);
    float sparkle = pow(max(ripple,0.0), 16.0)*0.19;
    ALBEDO = mix(ALBEDO + sparkle, vec3(0.88,0.95,0.82), foam*0.87);
    NORMAL = normalize(vec3(ripple*0.075, ripple*0.055, 1.0));
    ROUGHNESS = 0.24;
    SPECULAR = 0.55;
}
