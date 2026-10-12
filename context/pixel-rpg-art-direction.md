# Mosslight Journey: unified world art direction

## Decision and scope (2026-10-07, M5.2.3)

The user requested 10-20 characters referencing Re:Zero, explicitly chose original characters inspired by temperament and professions, then expanded the reference to items and the entire visual theme. Set the working humanoid roster to 16, replacing the earlier 12-humanoid planning count. This is a design target, not 16 delivered characters. Keep eight directions and square-grid three-quarter top-down. Existing enemies/animals/environments/UI scope remains; matching humanoid portrait target becomes 16. With eight enemies and four animals unchanged, the revised idle/walk estimate is 28 x 80 = 2,240 frame slots.

The reference informs a coherent ensemble of travelers, household staff, knights, merchants and magic users. Designs, names, insignia, costumes and relationships remain original. Do not build one-to-one renamed replicas. Source: [official Re:Zero character directory](https://re-zero-anime.jp/tv/character/), checked during the preceding reference discussion; the supplied Chinese Fandom URL was unavailable to the research tool. No official artwork is embedded in our delivered assets.

## Shared art rules

- Native tiles 32 x 32; character cells 48 x 64, foot anchor (24,56); inventory cells 32 x 32. Direction order S,SE,E,NE,N,NW,W,SW.
- Dark colored outlines, hard pixel edges, nearest sampling. Upper-left light; warm highlights and blue-grey shadows. Cloth, wood, metal and crystal must read differently.
- Palette families: teal textiles/crystal, brass hardware, warm plaster, brown timber/leather and muted steel. Shared materials do not require every character to wear identical colors.
- Original guild motif: a brass seed-shaped diamond. Repeat it on badges, selected equipment, magic containers, books and guild signage; ordinary bread/herbs retain plain utilitarian forms.
- Wood-framed plaster shops and stone foundations, teal shingles, glass bottles with wooden stoppers, brass keys/lanterns, parchment documents and leather-bound books.
- Reuse actual item pixels for inventory slots and shop merchandise. Weapon hand-held designs need their own appropriate-scale pose treatment; an icon is not proof of equipment animation.
- Preserve identity across views: asymmetric equipment stays on its intended side and is depth-sorted. This remains an art-review item in the current overlay-based character study.

## Working original roster

| ID | Name | Role | Planned distinguishing design |
|---|---|---|---|
| CH01 | Rowan | Traveling scout | Short teal cape, auburn hair, diagonal harness, left satchel |
| CH02 | Sylva | Grove scholar | Pointed ears, split traveling robe, wooden crystal staff |
| CH03 | Bren | Town warden | Broad steel pauldrons, split teal tabard, compact sidearm |
| CH04 | Osric | Veteran swordsman | Grey beard, weathered long cape, narrow silhouette |
| CH05 | Mira | Apothecary/healer | Rolled sleeves, herb pouch, practical apron |
| CH06 | Tovin | Caravan merchant | Layered waistcoat, ledger, travel hat |
| CH07 | Neris | Estate steward | Long tailored coat, keys, pinned hair |
| CH08 | Pella | Innkeeper | Broad apron, tied kerchief, serving pouch |
| CH09 | Garran | Blacksmith | Heavy gloves, leather apron, wide stance |
| CH10 | Edda | Farmer | Straw hat, short overalls, work boots |
| CH11 | Lio | Young courier | Small build, cropped jacket, oversized letter bag |
| CH12 | Vessa | Archivist | Modest spectacles, book harness, straight robe |
| CH13 | Soren | Court envoy | Structured mantle, document case, restrained decoration |
| CH14 | Fenn | Trail guide | Hood folded back, short poncho, rope coil |
| CH15 | Ivara | Relic investigator | Asymmetric utility coat, protective gauntlet, relic case |
| CH16 | Dulce | Traveling musician | Flared short coat, original string instrument, ribboned case |

CH01-CH04 are first studies, not final accepted designs. Other entries are specifications only. Party selection can include the healer; the first four studies were selected for silhouette diversity rather than final battle-party membership.

## M5.2.3 deliverable and review

`pixel-rpg-demo/authoring/build_theme.py` generates four eight-direction idle/walk studies (320 frame slots), twelve item designs, a guild shop, an apothecary stall and a street floor. `build_theme_scene.gd` builds a separate Godot street scene. The earlier sample remains available as main.tscn.

Current limitations: shared underlying body/head rig; small angular limbs; simplistic cloak/robe secondary movement and facing occlusion; buildings are single-view sprites with no enterable interior; street floor is a demonstration image, not a modular production tileset; the UI demonstrates item appearance but no inventory logic. Do not count these as the finished M7 or M8 deliveries. Color and motif cohesion is demonstrated; commercial-reference detail and animation quality remain unaccepted.

Next art pass: individually author hair/face shapes and side/back garment silhouettes, refine cloth/armor movement and contact poses, improve architectural wear and vegetation, then compare gameplay-scale motion before expansion.

## M5.2.4 superseding character contract

The user rejected the shared-head/body baseline. Current character construction is specified in pixel-rpg-demo/MODULAR-CHARACTERS.md and authoring/character-parts.json: independently selectable appearance parts, species, build and profession clothing; eight-direction idle/walk/run and separate shadow. Earlier names/role sketches are historical proposals, with recipe outfit/species/build authoritative for the current sample. Environment/item cohesion remains the intended art direction. Sixteen presets are now implemented as modular studies, but portraits/battle actions and final art acceptance remain outstanding.

## M5.2.5 visual route correction

User accepts the mechanics but rejects the procedural raster aesthetic. Current visual direction is local DreamShaper illustration -> retained design -> sprite cleanup -> consistent directions/poses, documented in pixel-rpg-demo/MODEL-ART-STUDY.md. User praised the newly generated illustrations. Earlier modular samples remain technical scaffolding, not accepted final art; class/species/build specifications remain applicable.

## M5.2.6 unified style gate (2026-10-07)

The user explicitly reiterates that the entire pack must share one art style. Treat this as a cross-category acceptance requirement, not only a prompt keyword or shared teal palette.

- Visual anchor: the praised local illustration direction, with `production/pixel-rpg/candidates/mosslight_chibi_731212_00001_.png` as the working study reference. This particular seed is an assistant-selected anchor, not a user-approved final sprite.
- Drawing: clean dark colored contours, broad cel-shaded forms, warm upper-left highlights and cool shadows. Reject photorealistic surfaces, glossy 3D renders and vector-logo treatments.
- Proportions: approximately 3.5-4 heads for ordinary humanoids, preserving real width/mass differences for the requested body types. Species, age and profession remain mandatory; style transfer must not turn a male elder or muscular dragonborn into the reference swordswoman.
- Projection: square-grid orthographic top-down, with consistent visible top surfaces and ground contact. Portrait camera does not automatically qualify as gameplay camera; reject isometric/low-angle buildings beside top-down sprites.
- Materials: matching wood, leather, cloth, plaster, brass and crystal treatment throughout characters, buildings and items. Permit profession and hair accents; do not recolor every asset teal.
- Pixel finish: judge contours, shading clusters and detail density at actual gameplay size. The 96x128 character conversion study and batch target sizes are provisional; they do not silently replace the earlier engine grid contract.
- Gate: first assemble one character, one building, one prop and one item on a common scene-scale review board. Review them together and fix mismatches before further broad replacement generation. Do not count a successful model run as accepted art.

The first batch failed this gate. Exact per-asset issues are recorded in `pixel-rpg-demo/authoring/model-wave-01-review.json`; no current batch source is selected for delivery. Shared female-reference img2img trials also failed to preserve male age/build/identity. Retain all candidates as evidence; retry a bounded cross-category pilot with category-appropriate composition guides, not unrestricted batch rerolls.

## Directional garments are part of identity (M5.2.7, 2026-10-07)

User rejects turning only the person while retaining front-facing clothing. Every direction must reconstruct the same garment in that view: back-of-cape drape, rear skirt folds, rear boot shafts/seams/heels, and correct accessory occlusion. Front chest clasp and belt buckle must not appear through the cape on a rear view. Side views need actual garment thickness and overlap; mirroring or deforming the frontal painting alone is insufficient. Rear-only structures are still required to match the front's design, palette, proportions and detail quality.
