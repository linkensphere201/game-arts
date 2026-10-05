"""Prepare a local model draft for pixel inspection. Uses local CPU postprocessing only."""
import argparse
from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]

def prepare(source, destination):
    image = Image.open(source).convert('RGB')
    rgb = np.array(image)
    # Remove only background-connected near-neutral light pixels, retaining enclosed horn highlights.
    light = (rgb.min(axis=2) > 80) & ((rgb.max(axis=2).astype(int) - rgb.min(axis=2)) < 55)
    labels, _ = ndimage.label(light)
    border = np.unique(np.concatenate((labels[0], labels[-1], labels[:, 0], labels[:, -1])))
    border = border[border != 0]
    foreground = ~np.isin(labels, border)
    # Art-directed floor mask for the selected seed 420052; preserve the two feet.
    if '420052' in source.name:
        foreground[250:, :] &= ~light[250:, :]
        foreground[450:, :] = False
        raw = ~np.isin(labels, border) & ~light
        foreground[450:472, 108:176] = raw[450:472, 108:176]
        foreground[450:454, 278:352] = raw[450:454, 278:352]
    components, count = ndimage.label(foreground)
    if not count:
        raise ValueError('No foreground found; inspect the draft and segmentation')
    sizes = np.bincount(components.ravel()); sizes[0] = 0
    foreground = components == sizes.argmax()
    alpha = Image.fromarray((foreground * 255).astype('uint8'))
    rgba = image.convert('RGBA'); rgba.putalpha(alpha)
    bbox = alpha.getbbox()
    crop = rgba.crop(bbox)
    scale = min(54 / crop.width, 52 / crop.height)
    resized = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.NEAREST)
    # Quantize visible colors consistently; retain binary transparency separately.
    reduced = resized.convert('RGB').quantize(colors=31, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGBA')
    reduced.putalpha(resized.getchannel('A').point(lambda p: 255 if p >= 128 else 0))
    canvas = Image.new('RGBA', (64, 64))
    origin = ((64 - reduced.width) // 2, 56 - reduced.height)
    canvas.alpha_composite(reduced, origin)
    destination.mkdir(parents=True, exist_ok=True)
    canvas.save(destination / 'canonical.png')
    rgba.save(destination / 'segmented-source.png')
    canvas.resize((512, 512), Image.Resampling.NEAREST).save(destination / 'canonical-preview.png')
    (destination / 'cleanup.json').write_text(json.dumps({'source': str(source), 'source_bbox': bbox, 'final_origin': origin, 'final_size': reduced.size, 'method': 'border-connected light background removal; largest component; nearest resize; 31-color quantization; fixed 64x64 canvas', 'manual_review_required': True}, indent=2), encoding='utf-8')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('source', type=Path)
    p.add_argument('destination', type=Path)
    args = p.parse_args()
    prepare(args.source, args.destination)
