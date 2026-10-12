# M5.2.9 — Standard-body character pilot

Date: 2026-10-12. User authorized one body, separate clothing/equipment, materials, rig and movement. This supersedes the earlier research-only gate for this one-character slice. No roster expansion or running.

## Result and limits

One continuous adult male MPFB body, independent sweater/trousers/boots/back sword, retained UVs and source garment textures, 53-bone game-engine skeleton, restrained Idle and procedural IK Walk. Godot 4.7.2 imports and plays both actions. This is a technical pipeline prototype, not an accepted anime design or sale-ready asset. Bald white-clay anatomy is deliberate; hair, skin/eye art and fantasy costume design remain unfinished. Walk is in-place and still needs artistic timing, contact and travel-speed tuning. No claim of complete collision-free movement, cross-character reuse or eight-direction sprite delivery.

Local output root: `E:/projects/game-arts/.local/mpfb-pilot/character-v1/` (ignored).

| File | Purpose |
| --- | --- |
| `01-standard-body.blend` | Full anatomical base, editable MPFB shape keys, no clothes |
| `body-front.png`, `body-side.png`, `body-back.png` | Body review views |
| `02-dressed.blend` | First fitted clothing stage; retains initial overlap for comparison |
| `03-rigged.blend` | Initial rig/weight stage before corrections |
| `04-animated.blend` | Corrected outfit, rigid back sword, Idle/Walk and packed textures |
| `adventurer.glb` | Five weighted meshes, embedded textures and two actions |
| `godot-demo/project.godot` | Import into Godot, F6/F5 or run project |
| `godot-demo/godot-preview.png` | Actual engine screenshot |
| `godot-demo/walk-00.png` through `walk-23.png` | Actual engine walk-cycle capture |
| `body.json`, `rig.json`, `export.json` | Parameters, skeleton and geometry measurements |

Demo controls: Space toggles Idle/Walk; Left/Right turn the character. There is no player travel controller yet. To edit the complete body, open stage 01. Stage 04 hides covered lower anatomy with a reversible mask; the game export applies these masks to separate copies. Taking clothes off the exported GLB will reveal missing covered surfaces: re-export from the complete editable body for other outfits.

## Sources and attribution

- MPFB 2.0.18, official `makehumancommunity/mpfb2`, commit `d0a32e57a7f915cb2f2b95410e2117648c7bbb7e`. [Source](https://github.com/makehumancommunity/mpfb2). Pinned archive: `https://codeload.github.com/makehumancommunity/mpfb2/zip/d0a32e57a7f915cb2f2b95410e2117648c7bbb7e`; SHA256 `b50c69cea33cce250ca49d838079904da7fb84a21943f3cb7fc5a9bb3e0165f8`.
- MPFB software license is GPL-3.0; do not confuse this with the CC0 base/assets policy. [Official generated-model FAQ](https://static.makehumancommunity.org/mpfb/faq/can_i_sell_models.html).
- Official CC0 packs from `https://files2.makehumancommunity.org/asset_packs/{pack}/{pack}_cc0.zip`: `shirts01`, `pants01`, `shoes01`, `equipment01`.
- Selected assets: `toigo_fisherman_sweater`, `toigo_wool_pants`, `toigo_ankle_boots_male`, `joepal_crude_sword`. Each selected `.mhclo` header declares CC0; preserve the downloaded asset metadata. Sword author: Joel Palmius. Clothing headers credit MRT. These existing assets are adapted, not newly authored original wardrobe designs.
- No standalone MakeHuman application installed. MPFB loads the MakeHuman-compatible body/assets directly. No existing character source was modified.

## Reproduction

Tools: existing Blender 4.5.14 at `E:/shared-resources/tools/blender/blender-4.5.14-windows-x64/blender.exe`; existing Godot 4.7.2 at `E:/shared-resources/tools/godot/Godot_v4.7.2-stable_win64_console.exe`.

Extract pinned source under `.local/mpfb-pilot/source/` and each asset zip under `.local/mpfb-pilot/assets/{pack}/`, preserving archive folders. Set `BLENDER_USER_RESOURCES=E:/projects/game-arts/.local/mpfb-pilot/blender-user` for isolated extension registration. Scripts register the source as `bl_ext.mpfb_pilot.mpfb`; no global addon installation is needed.

Run in order with Blender `-b -t 4 -P SCRIPT -- ARGS`:

1. `tools/mpfb-character-pilot.py ROOT OUT`: base and three views.
2. `tools/mpfb-dress-pilot.py ROOT OUT`: fit assets, add built-in `game_engine` rig and interpolate clothing weights.
3. `tools/mpfb-animate-pilot.py OUT`: fix lower sweater clearance, mask covered legs, attach rigid sword weights, make Idle/IK Walk, retain editable source and export separate meshes.
4. Python `tools/package-mpfb-demo.py OUT`: package generated GLB and authored Godot demo source.
5. Godot `--headless --path OUT/godot-demo --editor --import`; then `--headless --path OUT/godot-demo -- --verify`.
6. Godot `--path OUT/godot-demo -- --capture` renders a full 24-frame cycle and exits.

Here ROOT is the absolute `.local/mpfb-pilot` path; OUT is its `character-v1` child. Scripts can overwrite generated outputs when rerun; retain a separate OUT directory for future accepted variants. Blender may leave backup `.blend1` files; do not clean these without authorization.

## Verification

- White body: 19,158 source vertices including MakeHuman fitting helpers; 13,380 visible body vertices; approximately 1.554 m height with this macro configuration. Helpers are masked, not part of the exported visible body.
- Corrected game export: 5 mesh objects, 53 bones, 15,856 mesh vertices and 31,418 triangles before glTF UV/normal vertex splitting; no target triangle budget or LOD claimed.
- Initial sweater/pants overlap and incorrect knee pole direction were observed in actual renders and corrected. Only sampled poses reviewed; remaining gait/skin deformation is a prototype.
- Godot verification checks named Idle/Walk actions, 53 bones and actual foot movement: Idle sampled displacement 0.0 m; Walk sampled displacement 0.0815455 m. `MPFB_GODOT_ANIMATION_OK` passed.
- Actual GPU viewport captured with `MPFB_GODOT_CAPTURE_OK`; material meshes and back sword visibly present.
- Exporter reports truncating vertices with more than four bone influences and choosing the first sampler where material nodes share a texture. These need closer deformation/material comparison before final asset acceptance.
- Sandboxed Godot editor/log directory access emitted environment errors; runtime animation checks passed. Unsandboxed actual capture completed with an empty error log. No geometry, model weights, downloaded resources or generated demo artifacts are committed.

Next: review the single standard body's proportions and replace the placeholder wardrobe/face styling, polish one grounded walk, then render eight headings and evaluate sprite readability. Do not expand the roster before this baseline is accepted.

## 2026-10-12 — M5.2.9.2.1 stylized base-body proportion variant

User approved a Zelda: Breath of the Wild / Tears of the Kingdom inspired proportion study. This is an original generic MPFB body adaptation, not a reconstruction of Link. Target approximately 6-6.5 heads tall; 6.25 at the explicitly authored chin plane. The ratio is a design target, not an official Nintendo specification or automated anatomical measurement.

Created a separate static helper-free mesh with Basis and Manga_6_25_heads shape keys. Retained the original 1.553595 m height and 13,380 visible vertices/UV topology; enlarged the head, shortened the torso, narrowed the waist and slightly lengthened/slimmed the legs. Original body source SHA256 verified unchanged: 1662f3691a90d228169010faf54ed83b6b237137114646bee1d930ad96495520. Original source object is hidden in the new file for reference; all earlier body, rig and animation files remain intact.

Local outputs: `.local/mpfb-pilot/stylized-body-v1/stylized-base-body.blend`, `proportions-overview.png`, front/side/back/three-quarter/game-view renders and `proportions.json`. Reproduce using `tools/build-stylized-body.py` with the original `character-v1/01-standard-body.blend` and an output directory; run `tools/preview-stylized-body.py` to compose the actual render comparison.

Technical generation and proportion previews complete; user visual acceptance pending. Face remains a provisional realistic MPFB face and needs separate stylization. No new rig, fitted wardrobe, collision verification or animation retargeting is claimed. Review proportions first; then refit joint positions, weights and motion contacts. The old action-set remains valid only for its original body. This variant is not a drop-in replacement for the MPFB fitting-helper source.

## 2026-10-12 — M5.2.9.2.2 manga face geometry

User authorizes facial geometry adjustment and specifies lower forehead, short chin, large eyes and a tapered oval face. Added independent Manga_face shape key relative to Manga_6_25_heads. Enlarged eyelid openings, simplified nose/lip volume, tapered the jaw, raised the lower-face/chin region and compressed the upper cranium. Added neutral white ellipsoid eyeballs with scale drivers for the face slider. Both comparison rows include eyes; lighting and cameras are matched.

Current candidate: `.local/mpfb-pilot/stylized-face-v4/stylized-body-face.blend`; comparison `face-comparison.png`; per-view before/after renders, full-body render and `face-report.json`. Tools: `tools/build-stylized-face.py` and `tools/preview-stylized-face.py`. Earlier v1-v3 are preserved iteration artifacts, not the delivery candidate. Fixed first-trial eye protrusion and a centerline deformation defect before delivery.

The facial shape key retains 13,380 body vertices and existing topology; the body below z=1.27 m is unchanged. Input proportion-study file hash remains unchanged. Head shortening changes total height and head ratio slightly; do not treat the earlier 6.25-head landmark value as a measured value of this new face. This is a static white-clay sculpt candidate with visual acceptance pending, not a final character likeness, facial-expression rig or validated blink system. Bone/action adaptation remains pending. No clothing/texture changes.

## 2026-10-12 — M5.2.9.2.2 rejected; pre-face appearance restored

User rejected the manga face as unnatural and requested the before appearance. M5.2.9.2.2 is rejected/superseded, not awaiting approval. Current editable body: `.local/mpfb-pilot/restored-body/current-base-body.blend`, with Manga_face=0 and Manga_6_25_heads=1. Neutral test eyes retained to match the before comparison; no new facial deformation active. The original proportion-only file remains `.local/mpfb-pilot/stylized-body-v1/stylized-base-body.blend`. Prior face trials retained as inactive experiments. Do not continue facial stylization without a new user request.
