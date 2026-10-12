# Ivara mesh and automatic-rig trial

Date: 2026-10-11. Task: M5.2.8.1. Status: bounded inspection and deformation experiment complete; visual rig acceptance failed. Shared walk/Godot integration remain outstanding.

## Source and preservation

Input: `production/pixel-rpg/tripo-3d-dl/ch_ivara.glb` (user-generated Tripo model).
SHA256 before and after both experiments: `ad34dd59e95a82ba22928b1d590bdb3d14c56a7fb5d5cf7feef1e9bf0e635f51`.
The original was not changed. All geometry editing happened in an imported in-memory copy and separate output files.

## Measured results

| Item | Result |
|---|---|
| Original mesh | 1,011,340 vertices; 1,951,153 triangles; no vertex groups or armature modifier |
| Textures | Three embedded 4096 x 4096 images: base color, normal, metallic/roughness |
| Raw connected components | 352; this includes seam-split vertices and is not a body-part count |
| After merging vertices within 0.000001 model units on a copy | 975,568 vertices, 6 boundary edges, 9 nonmanifold edges (boundary edges included) |
| Decimation trial | 59,999 triangles, approximately 96.9% reduction |
| Approximate skeleton | 20 bones; torso/head, arms/hands, legs/feet and a three-segment tail |
| Automatic weights | All reduced-mesh vertices have positive weights; this does not establish correct anatomical influence |
| Export | trial.blend 15,502,369 bytes; trial.glb 10,026,316 bytes |
| Export round trip | 20 bones and Deformation_Test_NOT_Walk action survived GLB re-import; measurable vertex displacement 0.12696 model units between frames 1 and 17 |

## Visual assessment

Five original textured views were rendered. A visible gap separates the legs; portions of the arms are visibly separated from the torso. Hands sit close to the belt/pouches and thighs, and the tail joins close to the pelvis. These are weight-assignment risk areas. This inspection does not prove that every hidden surface is free of bridges, intersections or anatomical fusion. No anatomical adhesion was conclusively diagnosed from connectivity alone.

At 640 x 800, the reduced resting copy retains the broad silhouette and textured appearance. This is not a close-up topology/normal-map bake acceptance test. Tiny fingers, hair tips and accessories remain areas to inspect.

The diagnostic action bends one thigh/knee and swings arms. Comparing rest and stress views shows unwanted chest/jacket movement during arm movement. Automatically assigned weights and estimated joint landmarks are not accepted for production. The action is deliberately named NOT_Walk: it is a rest-stress-rest diagnostic, without alternating gait, foot locking, grounded motion or polished timing. The tail chain is approximately placed, not validated along its curved centerline. Facial and individual-finger bones are absent.

GLB export warned that more than four joint influences exist; it retained/normalized the four largest. The round-trip previews are rendered from that actual exported file. A sampler warning was also emitted, so texture settings should be checked in the target engine. Godot import/performance and cross-character action reuse have not been tested in this slice.

## Local evidence

- Original front/right/back/left/oblique renders and inspection.json: `.local/ivara-rig-study/2026-10-11-inspection/`.
- Editable Blender trial, GLB, rest/stress renders, metrics and animated `deformation-preview.gif`: `.local/ivara-rig-study/2026-10-11-rig/`.
- Source scripts: `tools/inspect-character-glb.py`, `tools/trial-ivara-rig.py`, `tools/preview-ivara-trial.py`.

Scripts run in Blender 4.5.14 background mode with four CPU threads. No model download, cloud upload or original-file replacement. Sandbox Blender startup exited immediately without output; the permitted elevated execution succeeded. The initial background launch produced empty logs; successful runs were monitored through terminal sessions instead. The GIF was assembled locally from nine round-trip frames with Pillow at 170 ms per frame, as a slowed inspection preview.

Reproduce using a fresh output directory for each trial:

```powershell
& 'E:/shared-resources/tools/blender/blender-4.5.14-windows-x64/blender.exe' -b -t 4 -P tools/inspect-character-glb.py -- production/pixel-rpg/tripo-3d-dl/ch_ivara.glb .local/ivara-rig-study/new-inspection
& 'E:/shared-resources/tools/blender/blender-4.5.14-windows-x64/blender.exe' -b -t 4 -P tools/trial-ivara-rig.py -- production/pixel-rpg/tripo-3d-dl/ch_ivara.glb .local/ivara-rig-study/new-rig
& 'E:/shared-resources/tools/blender/blender-4.5.14-windows-x64/blender.exe' -b -t 4 -P tools/preview-ivara-trial.py -- .local/ivara-rig-study/new-rig
```

## Next production gate

Correct joint landmarks and isolate torso/arm/hand/pouch influences; locate the remaining nonmanifold edges and assess whether they affect deformation. Repeat shoulder/elbow/hip/knee stress poses. Repair topology only where the observed deformation requires it. Fit and validate the tail separately. Once those poses pass, build one grounded walk cycle, test Godot playback, and only then render eight headings or reuse the rig across appearances. Do not expand the roster from this unaccepted automatic-weight result.

## Follow-up: low-poly elements and covered breathing (2026-10-11)

Tasks M5.2.8.1.1-M5.2.8.1.3. User clarified the immediate preview: hide outerwear/equipment, retain the inner outfit, keep feet fixed and test gentle breathing. User additionally requested fewer polygons for debugging and independently accessible clothing/body objects.

### Results and limits

- Reduced the 59,999-triangle copy to **19,999 triangles**. The assembled front render retains the broad silhouette and texture design at the inspected resolution. No production LOD, close-up normal-map or animation-retopology acceptance is implied.
- Split all 19,999 triangles exactly once into seven surface objects: head/hair/horns 5,425; jacket 3,400; equipment 3,293; inner-front surface 1,044; trousers/boots 5,125; hands 651; tail 1,061. Each object can be independently hidden and exported. Selection is spatial/color-assisted; some boundaries are ragged or misassigned. These are editable separation drafts, not clean closed standalone garments. Hair/head remain grouped; trousers/boots remain grouped.
- Hiding jacket/guards/belt exposes missing shoulders, arms, back and waist surfaces. This confirms the source does not provide a conveniently separable complete body under those selected clothing areas. It does not establish all hidden internal geometry or diagnose all adhesion.
- Built a separate **4,348-triangle white mannequin proxy**, exported as eight mesh objects. This is newly constructed approximate anatomy for fitting, with primitive hand/head forms and separate limb joins. It is not recovered original anatomy, a finished character body, or a ready-to-rig continuous retopology.
- The earlier skeleton landmarks and first hiding attempt used an incorrect torso-center estimate. Measurements show a substantial offset from the tail-inclusive mesh center. This study translates the working surface by (+0.067, +0.065, 0) model units; the original source is unchanged. The prior rig is not automatically repaired by this translation.
- A temporary dark covered torso/sleeve shell fills absent surfaces for the breathing test while retaining the original inner-front details. This exposes jagged selection boundaries and lacks accepted garment fit. The rejected initial shell/selection drafts are retained under `.local/ivara-rig-study/2026-10-11-breathing/`, not presented as final assets.
- Breathing is a localized shape key, **four-second cycle**, with maximum authored displacement **0.0018433 model units** (roughly 0.19% of character height). No armature/root/leg motion. Evaluated foot vertices at rest and peak inhale have **zero displacement**. A 24-frame close-up GIF uses a four-second loop. This is a covered movement study, not a polished idle animation or skeleton-reuse validation.
- Exported seven independent surface GLBs, one assembled GLB (7 meshes, 19,999 triangles, 8,319,672 bytes), and one proxy mannequin GLB (8 meshes, 4,348 triangles, 94,696 bytes). Individual textured exports repeat the original embedded atlas; triangle reduction does not proportionally reduce texture memory. Static exports intentionally omit animation. Breathing shape keys/actions remain in `elements.blend`.

### Files and inspection

All generated outputs: `.local/ivara-rig-study/2026-10-11-elements/`.

- `elements-review.blend`: assembled original-looking 20k surface groups selected on opening; independent parts in collection `10_Separated_original_surfaces_20k`. Hide individual objects using the Outliner. Proxy objects are in `20_NEW_white_mannequin_proxy`, initially hidden; expand that collection and toggle its objects' eye icons in the Outliner, hiding the other groups for a clear view. The white proxy is independent of the original surfaces.
- `elements.blend`: covered breathing study; play frames 1-96 at 24 FPS. Frame 97 repeats frame 1. The four-second breathing close-up is `breathing-closeup.gif`.
- `parts/assembled_20k.glb`, `parts/outer_jacket.glb`, `parts/equipment.glb`, `parts/inner_front.glb`, and `parts/NEW_white_mannequin_proxy.glb`, plus head/limb/tail files.
- `20k-assembled.png`, `white-mannequin.png`, `elements-overview.png`, `hidden-surfaces-only.png`, `covered-breath-rest.png`, `covered-breath-inhale.png` document appearance and incomplete boundary cleanup.
- `elements.json` and `exports.json` contain measured results. Rechecked original GLB SHA256: unchanged. Input trial.blend SHA256: `2aa7c8b2cda6bc1a311edfdedcbea04a2f09a5954f816fc1855ca3e3b89136b9`, unchanged.

Reproduction: run `tools/ivara-element-study.py` in Blender with the original trial.blend and a fresh output directory, then run `tools/package-ivara-elements.py` with that directory. Source scripts are Ivara-specific study tools, not a general clothing/body extraction algorithm. Previous rig files remain intact. Next gate is boundary cleanup, garment underside/thickness and anatomically fitted continuous body topology; automatic separation alone does not satisfy that gate.
