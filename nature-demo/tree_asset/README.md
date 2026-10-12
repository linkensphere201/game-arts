# Coastal broadleaf tree 0.1.0

Copy only `tree_asset/` into a new Godot project. Instance `tree_realistic.tscn` or `tree_cartoon.tscn`. A branched trunk, textured leaf crown, per-instance wind and four tapered trunk collision sections are included. Colliders approximate the main stem; branches and foliage have no collision.

Near representation: 5,974 triangles, 1,122 leaf cards. Far representation: 3,070 triangles, 396 broader leaf cards. Shared full-quality bark geometry remains in both. Default switch distance is 28 m, using per-mesh visibility ranges, with a hard transition rather than crossfade; some crown change remains possible. Root position and full-tree silhouette should be reviewed in the buyer's camera. This is a bounded distant model, not proof of a frame-rate gain.

Five 1K textures per style: bark color/normal/roughness, leaf color-with-alpha and normal. Surface colors are sRGB; data maps are linear. Leaf alpha uses cutout threshold 0.45 and mipmaps. Backfaces and light transmission are approximated in the leaf shader. Cartoon treatment changes surface palette/regions and normal strength while retaining the same detailed structure; it remains an initial art-direction variant.

The wrapper applies bark and leaf materials to named mesh nodes separately. It duplicates those materials per instance so wind_strength edits do not leak to other trees. Trunk base uses zero-height wind weighting, upper branches bend more, and UV2.x adds tip flutter to leaf cards. Preserve Bark/Leaves node names when re-exporting. The base collision is static and does not animate with upper branches. Change lod_distance before instancing/loading the scene, or reload the scene after editing it in this version.

Editable source: art-source/nature/coastal-tree.blend; show LeavesFar to inspect the reduced canopy. Maps are separate PNGs. The generation recipe `nature-demo/authoring/build_tree.py` expects repository layout. Joint tubes overlap rather than form a sculpted watertight trunk; junction transitions and crown botanical accuracy need further art work. The first bark pass is procedurally authored, not a photogrammetric scan. Material maps are linked in Godot; Blender source opens as geometry unless the separate maps are assigned for preview.

## Provenance, support and limits

First local review sample, version 0.1.0, 2026-10-06. Tested target: Godot 4.7.2 Windows Forward+; other engines/renderers/platforms are unverified. Geometry and textures are authored locally through Blender and deterministic procedural scripts, with AI coding assistance. No downloaded art, image-model output or external runtime service is included. Realistic/cartoon are material study routes, not claims of photorealism or accepted commercial quality. Final asset redistribution/license terms are pending owner approval.

Keep the folder name at the project root: resource paths are absolute within this package. Allow Godot to import GLBs and PNGs before placing scenes. Models are geometry-only GLBs; use the supplied wrappers or reconnect the external maps manually in other tools. Generated outputs are local and excluded from source-only Git publication.
