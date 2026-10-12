# M5.2.9.6 — White-body first action set

Date: 2026-10-12. User accepts the standard body, delegates rig assessment, and authorizes this first animation set. Clothing and character art are outside this slice. Earlier dressed-character trials remain references.

## Local deliverables

Root: `E:/projects/game-arts/.local/mpfb-pilot/action-set-v1/` (ignored, local only).

- `body-actions.blend`: editable complete body, 53-bone rig and ten named baked actions. Select StandardBodyRig and choose an action in Blender's Action Editor. Muted NLA tracks retain the individual clips.
- `body-actions.glb`: game copy, helper geometry removed, four normalized bone influences per vertex, ten clips with zero-based timestamps.
- `godot-demo/project.godot`: open with Godot 4.7.2 and run. The left panel selects all actions. Space pauses/resumes, the timeline scrubs, Left/Right orbit the camera. Looping locomotion can show calibrated travel or stay in place; one-shot clips hold their final pose. Blue floor disc marks the starting position; grid spacing is 0.5 m.
- `action-overview.png`, per-action GIFs and selected `*-phases.png`: actual Godot playback captures, not AI illustrations. GIFs repeat for inspection even when the corresponding engine action is a one-shot.
- `rig-audit.json`, `actions.json`, `motion-verification.json`, `godot-demo/engine-verification.json`: rig, contact targets, motion checks and imported-pose evidence.

| Clip | Duration | Behavior |
| --- | --- | --- |
| Idle | 3.2 s | Restrained chest expansion, planted feet; loops |
| Walk | 1.2 s | Alternating support/swing; loops; preview travel 0.5833 m/s |
| TurnLeft / TurnRight | 1.2 s each | Two-step 90-degree turn; root rotation retained |
| Run | 0.8 s | Shorter contact phase, flight interval and bent-arm swing; loops; preview travel 1.6875 m/s |
| Jump | 1.5 s | Anticipation crouch, takeoff, flight, landing compression and recovery; root height about 0.339 m |
| AttackLeft / AttackRight | 1.1 s each | Separate arm windup, downward/forward swing and recovery; no weapon or hitbox |
| HitLight | 1.1 s | Recoil and one short retreat step; moving foot retreats 0.16 m, root 0.08 m |
| HitHeavy | 3.0 s | Stronger recoil and five alternating retreat steps; root retreats 1.08 m |

The requested unspecified turn is interpreted as left/right 90 degrees. Heavy recoil uses five steps within the requested 4-5 range. Walk/Run are in-place clips with recommended travel speeds; Turn/Jump/Hit retain authored root motion. Do not apply root displacement twice in a future controller. This review project is not a gameplay controller or an AnimationTree with cross-action transitions.

## Rig assessment and implementation

The accepted complete white body is loaded from `.local/mpfb-pilot/body-rig-review/standard-body-rig-review.blend`. Source files are untouched. The supplied MPFB skeleton has 53 nonzero-length bones, exactly mirrored left/right rest joint positions and no unweighted visible vertices (13,380 checked). Deform-weight sums are approximately 0.999900-1.000000 before export normalization. The source audit does not constitute exhaustive anatomical or extreme-pose certification.

Use linear skinning for this set, matching glTF/Godot rather than relying on Blender-only preserve-volume deformation. Two-bone analytical limb solving produces reachable feet and controlled wrist trajectories; rotations are baked at 30 fps on the deform bones. No runtime IK or MPFB installation is required to play the GLB. MPFB is still required to regenerate the upstream anatomical body, not to load this action source.

Initial running targets exceeded leg reach; shorter stride and lower pelvis corrected this. Initial running arms spread too far and the overhead attack exposed shoulder bulging; wrist trajectory control, consistent elbow bend planes and clavicle-assisted arm elevation address those observations. A bounded symmetric correction transfers part of the nearby upper-arm weights to the clavicle on 754 source vertices, without changing the approved body shape or original rig file. Shoulder silhouette and hand posing still need artistic polish for close shots.

An initial NLA export retained a 1/30-second offset. Explicit `export_anim_slide_to_zero=True` fixes the clip time origin. Godot's default animation optimizer introduced up to 3.35 mm of ankle difference in Run after that fix; the generated import settings disable optimization/compression for this review. [Godot importer source](https://github.com/godotengine/godot/blob/master/editor/import/3d/resource_importer_scene.cpp) documents the node-level settings; this behavior was also measured locally. Keep those import settings when comparing frames exactly.

## Verification and practical limits

- Source checks compare solved ankle positions to requested trajectories, check zero foot drift in Idle, loop endpoint ankle agreement, locomotion contact-marker stability at specified travel speed, turn angles, jump height/return and one/five retreat lift events.
- Godot independently evaluates every exported frame and compares both foot-bone positions with the Blender samples. The threshold is 2 mm. Source markers are not a proof of full-foot contact or collision-free skin.
- Final measured imported ankle error is at most approximately 0.00000231 m (0.00231 mm); all ten clips pass. No loop endpoint ankle mismatch or unreachable leg target remains in the sampled source data. Idle foot-marker drift is zero; heavy recoil contains five measured lift events and 1.08 m root retreat.
- Actual viewport capture covers every clip at 20 fps, including endpoints. Inspect the phase sheets for anticipation, contact and recovery, and the GIFs for timing. Structural success and complete clip coverage are separate from final artistic acceptance.
- These are procedurally authored first-pass actions, not motion capture. Foot roll, pivot friction, finger grips, shoulder volume, impact force, motion blending and gameplay collision still need final polish or integration. No commercial-quality or full-body collision certification is claimed.
- Sandboxed editor/log-directory warnings are environment limitations; record test success using explicit verification markers and exit status. Actual viewport capture runs with access to the local GPU.

## Reproduce

1. Blender 4.5.14: `-b -t 4 --python-exit-code 1 -P tools/build-body-actions.py -- RIG_REVIEW_BLEND OUT`.
2. Python: `tools/verify-body-actions.py OUT`.
3. Python: `tools/package-body-actions.py OUT` (copies the generated GLB/manifest and writes the demo and import settings).
4. Godot: `--headless --path OUT/godot-demo --editor --import`.
5. Godot: `--headless --path OUT/godot-demo -- --verify` (nonzero exit on mismatched imported poses).
6. Godot: `--path OUT/godot-demo -- --capture`; then Python with Pillow: `tools/preview-body-actions.py OUT`.

Use a new OUT directory to preserve an accepted variant. Generated files are overwritten on rerun; no automatic file cleanup is performed. Source/scripts/docs only belong in Git; no generated models, screenshots, GIFs or downloaded assets are staged or pushed.

## 2026-10-12 — M5.2.9.6.5 restored-proportion body adaptation

Current action deliverables: `E:/projects/game-arts/.local/mpfb-pilot/restored-body-actions-v2/`. This supersedes action-set-v1 as the current-body preview; the previous body and action outputs remain intact. Input appearance is `restored-body/current-base-body.blend`, with rejected Manga_face=0 and proportion key=1.

`tools/fit-stylized-body-rig.py` accepts ORIGINAL_RIG_BLEND RESTORED_BODY_BLEND OUT. It maps all 13,380 body vertices bijectively using original Basis coordinates, transfers the original supplied weights, fits 53 rest bones with the exact approved proportion map, and joins neutral eyes with rigid head weights. Stored rest-shape mismatch is below 1e-9 m. No source file changes. The fitted authoring rig and adaptation report are in `restored-body-actions-v1/adapted-rig.blend` and `adaptation.json`; v1 action exports are an intermediate trial with unreachable walk wrist targets and must not be used for delivery.

Run the existing action builder using that adapted rig and the v2 output directory, then the existing verify/package/import/verify/capture/preview commands. Hand targets now scale with arm-chain length relative to the original 0.45140553 m chain; the new chain is approximately 0.41840475 m. Arm reach residuals are included in the existing reach check. This corrected the 0.0189 m unreachable wrist target found in the first walk trial. Ten clips retain prior durations and intended turn, jump and recoil behaviors.

Validation: 53 bones, 16,360 weighted vertices including eyes, zero unweighted vertices or zero-length bones, mirrored rest joints. All ten source motion checks pass, including hand/foot reach, stationary idle ankles, loop ankle endpoints, calibrated locomotion contact markers, +/-90 degree turns, jump return and one/five retreat steps. Godot every-frame imported foot error is at most 0.000000761 m. Actual GPU capture produced 318 frames and BODY_ACTIONS_CAPTURE_OK with empty error log. Overview and attack/locomotion phase views inspected. These verify adaptation and coverage, not polished animation: shoulder volume, finger grip, foot roll, physical impact and gameplay transitions still need refinement. No wardrobe, facial redesign or sprite batch.

## 2026-10-12 — M5.2.9.6.6 Quaternius four-clip experiment

User authorizes a small Quaternius Universal Animation Library trial and asks how its rig differs. Downloaded only the free Standard ZIP from https://quaternius.itch.io/universal-animation-library through its public free-download flow. Bundled License.txt declares CC0 1.0. ZIP SHA256: cc73fc4e495b82958207316596317a3f40b9fa38065bde1027937452da537724. Stored under `.local/quaternius-pilot/`; no payment, account sign-in or paid Source pack used.

Actual non-root-motion GLB contains 43 animations including A_TPose. Source skeleton has 65 bones; all 53 target MPFB bones map, with root/Root and Head/head capitalization differences. The 12 source-only bones are ten finger-tip `_04_leaf` bones and two `ball_leaf` bones. Source rest is T-pose; target rest is A-pose with adjusted proportions. The standard export does not establish what authoring controllers the artist used. Extra endpoint bones do not explain animation quality; anticipation, weight shift, timing and torso participation are the main observed differences.

Trial clips: Walk_Loop, Sprint_Loop, Punch_Cross and Sword_Attack, retargeted as Q_Walk, Q_Sprint, Q_Punch_Cross and Q_Sword_Attack. Source GLB imported into Blender at 24 fps and saved as `.local/quaternius-pilot/source-import.blend`; source action durations sampled in seconds and baked at 30 fps. `tools/retarget-quaternius-pilot.py` takes CURRENT_ACTION_BLEND SOURCE_IMPORT_BLEND OUT; maps rest directions/rolls, scales pelvis displacement and matches lowest skinned foot height vertically while preserving source flight. This is not horizontal foot locking or complete contact solving. Current-body shape and source files remain unchanged.

Current output: `.local/quaternius-pilot/retarget-v2/` with editable body-actions.blend, GLB, selectable Godot demo, four GIFs, phase sheets, actions.json and retarget-report.json. First v1 trial is superseded: imported auxiliary object obscured Blender renders and Godot stripped the Loop suffix, causing action lookup failure. v2 hides imported references and uses unambiguous clip names. Preview labels now accept per-clip names while preserving the prior ten-action demo.

Verification: all 53 target bones mapped; source duration retained; vertical foot-floor residual below 0.00000011 m; Godot imported ankle positions checked each sampled frame (maximum difference 0.000001456 m). Four actual GPU clips captured with BODY_ACTIONS_CAPTURE_OK and empty error log. Inspected overview and sword phases. GLB exporter normalizes the largest four skin influences; bone-position verification does not establish pixel-identical skinning. Visual finding: stronger sprint lean and sword anticipation/follow-through than the procedural test. Shoulder/waist deformation, grip and horizontal foot contact still require cleanup. Sword preview intentionally has no weapon. Current established ten-action set remains available; no full-library replacement approved.

## 2026-10-12 — M5.2.9.6.7 animation methodology and motion acquisition

Recorded at user request. A usable skeleton and valid export do not establish convincing animation. The missing central capability is a repeatable source of coordinated motion, followed by retargeting and artistic cleanup. Procedural per-bone curves remain useful for technical tests, not the default quality baseline.

Method:
1. Acquire a reference or reusable motion: a licensed animation library, performed video, or motion capture.
2. Establish readable key poses: anticipation, extreme/contact, follow-through and recovery.
3. Tune timing and spacing, including holds and acceleration; coordinate feet, pelvis, torso, shoulders and hands.
4. Correct contacts, planted feet, balance, inertia, loops and transitions on the target body.
5. Review silhouette and skin deformation from the gameplay camera, then bake the deform skeleton and validate in Godot.
6. Store the cleaned action with frame rate, duration, rest-pose mapping, root-motion convention and contact intervals so it can be reused across characters.

An authoring control rig (IK/FK handles and constraints) is distinct from the baked deform skeleton exported to a game. The inspected Quaternius export does not prove the author's exact control setup or whether each action was keyed or captured.

Recommended acquisition strategy, not yet a production-tool decision: retain the existing CC0 Quaternius samples as the baseline; use video capture to fill custom-action gaps; route both through the same standard-body retarget/cleanup/export process. Realistic captured motion may still need stylized anticipation, timing and exaggeration.

Video is a measurement/estimation source, not a finished animation. Single-view footage leaves depth, occluded limbs and axial twist ambiguous. Estimated 3D landmarks still require orientation solving, constraints, smoothing and contact/root-motion treatment before becoming reusable bone animation.

Proposed next experiment (not implemented): one 5-10 second, fixed-camera, full-body clip with a slow weight shift and one punch/recovery. Compare video, inferred skeleton and current white body side by side. Measure setup/inference/cleanup time, jitter, occlusion failures, foot sliding and pose readability against the existing Quaternius sample. Defer jump, full turns and fast sword motion until the simpler clip works. See context/research-notes.md for candidate tools and limitations.

## 2026-10-12 — M5.2.9.6.8 expanded Quaternius review delivered

User approves the mapping proposed after checking the downloaded library. Added --expanded to tools/retarget-quaternius-pilot.py; the original four-clip invocation remains supported. Uses the same unchanged current-body and Quaternius source Blender files. Ten source clips now retarget to the current 53-bone white body: Idle, Walk, Jog_Fwd, Sprint, Jump_Start, Jump (source Jump_Loop), Jump_Land, Punch_Jab, Punch_Cross and Sword_Attack. Retained the original TurnLeft, TurnRight, HitLight and HitHeavy actions and their sample metadata in the same 14-clip review.

Jab is labeled left-hand and Cross right-hand: source hand path lengths are 1.140/0.483 m (left/right) for Jab and 0.371/1.402 m for Cross; phase renders support the identification. This is an inspection heuristic, not a universal attack classifier. No mirroring required. Preview UI now scrolls; overview generator supports multiple rows.

Current local output: .local/quaternius-pilot/expanded-v1/
- body-actions.blend and body-actions.glb: editable source and 14 baked clips.
- godot-demo/project.godot: selectable, pausable, scrubbable preview.
- pilot-overview.png, per-clip GIFs and phase sheets: actual Godot captures.
- actions.json, retarget-report.json, godot-demo/engine-verification.json: provenance and verification.
- build.log/build.err and capture.log/capture.err: process logs.

Reproduce with Blender background script arguments: CURRENT_ACTION_BLEND SOURCE_IMPORT_BLEND OUT --expanded. CURRENT_ACTION_BLEND must have adjacent actions.json containing the retained turn/hit samples. Package with tools/package-body-actions.py OUT; import the Godot project, run -- --verify, then -- --capture; build GIFs with tools/preview-quaternius-pilot.py OUT.

Verification: Python syntax check passed; source hashes preserved; all ten retargets meet vertical foot-height residual <1e-5 m. Godot imports all 14 clips with 53 bones and maximum sampled ankle discrepancy 0.000001456 m. Actual capture completed with BODY_ACTIONS_CAPTURE_OK and empty stderr; generated all GIFs with expected frame counts. Inspected overview and Jab phase sheet.

Limits: adaptation review, not final animation acceptance. Horizontal foot locking, shoulder/waist skin cleanup, fist/grip polish and transitions remain. Jump phases are separate playable clips, not a stitched physics-driven jump. Walk/run are in-place source motions without calibrated gameplay travel speeds. Old turn/hit drafts are preserved as provisional coverage, not upgraded Quaternius actions. No wardrobe, new motion capture, full library migration or push.

## 2026-10-12 — M5.2.9.6.9 two-step lateral heavy-hit revision

User changes heavy-hit intent from 4-5 backward steps to exactly two steps with upper-body imbalance toward one side. Added tools/build-heavy-stagger.py, taking EXPANDED_BODY_BLEND OUT. It replaces only HitHeavy with HitHeavy_Stagger2 in a new copy; all thirteen other clips, source mesh/weights and original deliverables remain unchanged.

Motion: 1.9 s; rapid lean toward the character's left with backward recoil, asymmetrical arms catching balance, left-foot recovery step at 0.23-0.69 s, right-foot step at 0.77-1.23 s, then a small counter-sway and settling. Root finishes 0.41 m backward and 0.14 m sideways. Peak measured head-to-lower-spine lateral angle is 24.33 degrees. Lowered pelvis and analytic two-bone leg solving preserve planted ankle positions. This is authored motion with an intended balance-loss silhouette, not a physically simulated center-of-mass solution.

Current review: .local/quaternius-pilot/stagger-v1/body-actions.blend, body-actions.glb, godot-demo/project.godot and HitHeavy_Stagger2.gif. Full overview and per-clip previews also generated. Previous expanded-v1 remains available.

Validation: exactly one lift interval per foot, zero leg reach error, planted-ankle inter-frame drift 0.000000147 m. All fourteen clips pass Godot ankle comparison; new heavy-hit max error 0.000000744 m. Other clips retain their prior errors and sample metadata. Actual GPU capture and preview generation complete with empty stderr; inspected new heavy-hit phase sheet. Foot-bone checks do not certify sole roll or mesh collision. Visual approval and transitions remain pending.

### 2026-10-12 — M5.2.9.6.9 deeper hip/knee flexion

User requests more thigh/calf bending during heavy-hit imbalance. Current review moves to .local/quaternius-pilot/stagger-v2; v1 preserved. Pelvis lowering now uses an impact-and-footfall compression envelope, peaking at 0.155 m rather than about 0.090 m, with up to 0.025 m backward hip offset. This deepens hip/knee flexion while ankle targets remain grounded. Two steps, 1.9 s timing, lateral torso lean and final root displacement remain unchanged.

Checks: one lift per foot; zero reach error; support ankle drift 0.000000203 m; heavy-hit Godot ankle error 0.000000832 m. Recorded peak knee flexion 87.61/83.15 degrees (left/right, including swing). Other thirteen clip manifests match v1 exactly. Actual Godot capture completes with empty stderr; GIF/phase sheet generated and inspected. Current preview: stagger-v2/HitHeavy_Stagger2.gif. Visual acceptance and transitions remain pending.

### 2026-10-12 — M5.2.9.6.9 standalone Windows preview

Exported the current stagger-v2 Godot review to builds/body-action-review/body-action-review.exe (110,763,784 bytes), using the existing local Windows release template, embedded PCK, actions.json inclusion and capture/report exclusion. Local export preset is retained in stagger-v2/godot-demo/export_presets.cfg. No Godot installation is needed to run the EXE. Actual OpenGL GPU startup smoke test with --quit-after 120 exited 0 with no logged errors. This is a startup test, not a new full visual acceptance. EXE remains local/ignored; no push.

### 2026-10-12 — M5.2.9.6.10 shoulder correction delivered

Current review: .local/quaternius-pilot/shoulder-v1. Close rear/side render experiments compared original, attenuated clavicles, attenuated humeral twist, and both. Clavicle correction visibly reduces the posterior/superior shoulder prominence; twist-only correction does not. tools/fix-walk-shoulders.py scales only Q_Walk local clavicle rotations toward rest by 0.2, preserving the time-varying component. No mesh or weight changes; other actions remain intact. This is a targeted current-body correction, not a general retarget calibration for all rigs.

Source hash unchanged, foot sample comparison passes, all fourteen Godot clips verify with max ankle discrepancy 0.000001456 m. Actual GPU captures and GIFs complete with empty stderr; inspected side closeup and walk phase sheet. New EXE builds/body-action-review/body-action-review-shoulder.exe passes actual GPU startup and automatic exit (code 0). Previous body-action-review.exe remains the older build. Source project is shoulder-v1/godot-demo/project.godot. New GIF is shoulder-v1/Q_Walk.gif. User visual acceptance pending; not a full collision/skin certification.

### 2026-10-12 — M5.2.9.6.11 natural arms delivered

Added tools/fix-walk-arms.py, using shoulder-v1 as input and writing a separate copy. Only Q_Walk upper-arm, forearm, hand and finger channels change. Analytic arm solving preserves the elbow bend plane; wrist distance is 98.8% of arm-chain length, small fore/aft swing follows the opposite leg, fingers return to relaxed rest. Current fixed 0.10 m lateral wrist offset relative to each shoulder avoids discontinuous frame-by-frame clearance corrections. arms-v1 was an intermediate adaptive-offset trial; arms-v2 is current.

Verification: each sampled frame checks weighted hand vertices against the lateral torso/leg envelope within their height band (15 mm padding); minimum measured gap is 0.023716 m. This conservative axis separation check is not a complete whole-body triangle-collision test. All fourteen Godot ankle comparisons pass, other thirteen clip manifests are unchanged, actual GPU capture finishes with empty stderr, phase-sheet visual review confirms lowered hands beside thighs. Source hash preserved; no body/weight edit. Final visual acceptance remains with the user.

Current files: .local/quaternius-pilot/arms-v2/body-actions.blend, body-actions.glb, godot-demo/project.godot, Q_Walk.gif and arm-verification.json. Standalone EXE: builds/body-action-review/body-action-review-natural-arms.exe; actual GPU startup exits 0 without logged errors. Earlier EXEs remain older variants, not the current delivery.

### 2026-10-12 — M5.2.9.6.11 relaxed hands, upright torso and more elbow flexion

User requests three walk refinements: softly curled hands instead of open palms/fists, less forward torso lean, and more elbow flexion. Current review is arms-v3. Updated the walk correction to distribute 12/18/10 degrees of finger curl across joints, use gentler thumb flexion/inward adjustment, align the lower-spine-to-neck axis to 2 degrees forward in the sagittal plane, and shorten the arm target to 95.5% of chain length. Measured elbow flexion is about 34.58 degrees; wrist side offset stays constant, avoiding clearance-driven lateral jumps.

All sample posture assertions pass, minimum hand-envelope gap is 0.046201 m, foot samples remain unchanged and all fourteen Godot imports pass. Other thirteen clip manifests match arms-v2. Actual playback capture completes with empty stderr; inspected hand closeups from two views and full side view. Finger curl is partial, not a fist; body is visibly more upright. These checks do not establish complete mesh collision clearance.

Current files: .local/quaternius-pilot/arms-v3/Q_Walk.gif and godot-demo/project.godot. Latest standalone build is builds/body-action-review/body-action-review-relaxed-walk.exe; GPU startup test exits 0 without logged errors. Previous builds preserved. User visual acceptance pending.

## 2026-10-13 — M5.2.9.6.12 independent hand-pose library

Current output: `.local/quaternius-pilot/hands-v13/`; EXE: `builds/body-action-review/body-action-review-hand-poses.exe`.

- `HandPose_Relaxed` and `HandPose_Fist`: finger-only Blender action assets, 30 local quaternion channels each (both hands), plus `hand-poses.json` for programmatic reuse. Apply only the finger channels to a compatible body action; these presets are specific to StandardBodyRig and are not universal across arbitrary rigs.
- Relaxed uses a rest-bone palm plane, progressive partial finger curl and mild adduction. It replaces previous walk fingers while preserving the approved upper body and legs.
- Fist copies the existing Q_Sword_Attack right-hand grip at frame 1, then mirrors it in anatomical rest space. This implements the user's correction to the procedural thumb. It retains grip space; a tightly compressed punch fist is a separate future refinement.
- HandReview_Relaxed and HandReview_Fist are full-body static review clips for export, not the finger-only assets. In the demo, scroll to the bottom for the two closeup buttons and right-hand checkbox; use arrow keys to orbit.

Rebuild using Blender 4.5.14 with `--python-exit-code 1`:

```text
blender -b --python-exit-code 1 -P tools/build-hand-poses.py -- .local/quaternius-pilot/arms-v3/body-actions.blend <new-output-directory>
blender -b --python-exit-code 1 -P tools/verify-hand-poses.py -- .local/quaternius-pilot/arms-v3/body-actions.blend <new-output-directory>/body-actions.blend
python tools/package-body-actions.py <new-output-directory>
```

Then import/verify/capture with the existing Godot review procedure. Use the `blender-orbit-review` skill from `E:/projects/skills` for deterministic eight-view geometry checks. It does not certify appearance automatically: open and inspect each sheet, both sides, and animation extremes.

Evidence: hands-v13 contains fist left/right orbit sheets, hand-verification.json, engine verification, actual GPU captures and Q_Walk.gif. Unchanged relaxed left/right and walk frames 1/21 were reviewed in hands-v12. Minimum sampled lateral gap is 12.1 mm; no complete mesh collision test is claimed. Mesh/weights and unrelated motion are unchanged. Low-poly finger creases remain visible close up; user visual acceptance pending.
