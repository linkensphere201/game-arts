# Ember Imp: Godot Sprite Lab

This project imports the finished local-AI-assisted character from `ember_imp/`. It no longer displays calibration art.

## Run

Open `project.godot` in Godot 4.7.2 and press F6/F5 (the main scene is `main.tscn`). The local exported executable is `../builds/ember-imp-demo.exe` and does not need the editor or generation tools.

- Idle / Walk buttons: select the animation.
- Left / Right arrow keys: move and face the character; release to return to the selected animation.
- Space or Pause / resume: pause playback.
- Background button: compare dark and light backgrounds.
- Slider: change playback speed from 0.25x to 2x.
- Preview: 5x main view, 1x reference and individual animation frames.

The five runtime asset files are copied from `../assets/ember-imp/` and verified byte-identical. See that folder's README for importing the asset independently. It works without ComfyUI, custom Godot plugins or generation scripts.

## Verification and Export

`-- --self-test` runs a short playback check; add `--test-seconds=60` for the longer run. This verifies that all ten frames advance. Fresh-project validation separately verifies relocation, timing and pause behavior. Structural PNG checks and screenshots are in `../validation/`.

The Windows export preset references the matching templates in ignored `../.local/export-templates/templates/`. Run the version-pinned Godot editor with `--headless --path demo --export-release "Windows Desktop" ../builds/ember-imp-demo.exe` from the repository root after local setup. Builds are ignored by Git.
