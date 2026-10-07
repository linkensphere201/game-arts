# Project Overview

## Confirmed requirements — 2026-10-07

- Posters and cover images, rather than game sprites alone.
- Reference-image editing ("垫图编辑").
- Text generated in separate layers.
- Eventual API delivery.
- Local-deployable models preferred.

This side task coexists with the existing game-asset project. It does not replace the shared-rig3D character direction or restart cancelled Z-Image installation.

## Available foundation

Earlier project tests established RealVisXL V5.0 FP16 portrait generation at768x1024 (~24.1s), Realistic Vision V6.0 B1 at512x768 (~9.1s), and Animagine XL4.0 Opt at832x1216. These were specific portrait/character tests, not poster benchmarks or proof that additional ControlNet/IP-Adapter combinations fit. Current machine has8GB VRAM and approximately32GB RAM; Windows commit headroom is separately constrained. The parent project checks for10GiB available commit before loading, which is a guardrail rather than a universal model minimum.

## Working assumptions, not user decisions

Chinese and English text; initially digital sRGB output;2:3 vertical posters,16:9 covers and1:1 square variants. Working image generation around1MP, then compose/export at requested dimensions. Proposed examples:1080x1620,1920x1080 and1080x1080. Export resolution does not imply native model detail.

"Separate text" is provisionally interpreted as editable content/font/position plus independent transparent raster exports. PSD-native text, CMYK/bleed, automated copywriting, and arbitrary flattened-poster reconstruction are not promised in the initial slice.

## Open product choices

First use case (game promotion, product advertising, events, book/video covers); brand/style references; font families; maximum latency; target output dimensions; whether exact subject/logo preservation is mandatory; whether SVG/JSON is sufficient or native PSD is required. None blocks the present research.
