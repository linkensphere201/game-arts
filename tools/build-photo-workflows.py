"""Build ordinary portrait workflows from the running ComfyUI node schema."""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = (
    "Photograph of a 30-year-old woman wearing a blue denim jacket over a white "
    "crew-neck shirt, head and shoulders portrait, natural skin texture, "
    "soft window daylight, simple grey studio background, realistic photography."
)
NEGATIVE = "cartoon, anime, illustration, blurry, distorted face, text, watermark"


def make_graph(kind):
    graph = {}

    def node(i, name, **inputs):
        graph[str(i)] = {"class_type": name, "inputs": inputs}

    if kind == "z-image-turbo":
        node(1, "UNETLoader", unet_name="z_image_turbo_int8_convrot.safetensors", weight_dtype="default")
        node(2, "CLIPLoader", clip_name="qwen_3_4b_fp8_mixed.safetensors", type="lumina2", device="default")
        node(3, "VAELoader", vae_name="ae.safetensors")
        node(4, "ModelSamplingAuraFlow", model=["1", 0], shift=3.0, sampling="flow")
        node(5, "CLIPTextEncode", clip=["2", 0], text=PROMPT)
        node(6, "ConditioningZeroOut", conditioning=["5", 0])
        node(7, "EmptySD3LatentImage", width=768, height=1024, batch_size=1)
        model, vae, steps, cfg, sampler, schedule = ["4", 0], ["3", 0], 8, 1.0, "res_multistep", "simple"
    else:
        sdxl = kind == "realvisxl"
        checkpoint = "RealVisXL_V5.0_fp16.safetensors" if sdxl else "Realistic_Vision_V6.0_NV_B1_fp16.safetensors"
        node(1, "CheckpointLoaderSimple", ckpt_name=checkpoint)
        node(5, "CLIPTextEncode", clip=["1", 1], text=PROMPT)
        node(6, "CLIPTextEncode", clip=["1", 1], text=NEGATIVE)
        node(7, "EmptyLatentImage", width=768 if sdxl else 512, height=1024 if sdxl else 768, batch_size=1)
        vae = ["1", 2]
        if not sdxl:
            node(3, "VAELoader", vae_name="vae-ft-mse-840000-ema-pruned.safetensors")
            vae = ["3", 0]
        model, steps, cfg, sampler, schedule = ["1", 0], 25, 5.0, "dpmpp_2m", "karras"
    node(8, "KSampler", model=model, positive=["5", 0], negative=["6", 0], latent_image=["7", 0],
         seed=778201, steps=steps, cfg=cfg, sampler_name=sampler, scheduler=schedule, denoise=1.0)
    node(9, "VAEDecode", samples=["8", 0], vae=vae)
    node(10, "SaveImage", images=["9", 0], filename_prefix=f"photo_models/{kind}")
    return graph


def ui_workflow(graph, schema):
    nodes, links, lookup = [], [], {}
    positions = {1: (0, 0), 2: (0, 230), 3: (0, 460), 4: (360, 0),
                 5: (360, 170), 6: (360, 440), 7: (360, 650),
                 8: (800, 0), 9: (800, 430), 10: (1190, 0)}
    for key, item in graph.items():
        definition = schema[item["class_type"]]
        widget_values, inputs = [], []
        specs = dict(definition["input"].get("required", {}))
        specs.update(definition["input"].get("optional", {}))
        for name, spec in specs.items():
            if name not in item["inputs"]:
                continue
            value = item["inputs"][name]
            if isinstance(value, list):
                inputs.append({"name": name, "type": spec[0], "link": None})
            else:
                widget_values.append(value)
                if len(spec) > 1 and isinstance(spec[1], dict) and spec[1].get("control_after_generate"):
                    widget_values.append("fixed")
        height = {"CLIPTextEncode": 240, "KSampler": 320, "SaveImage": 450}.get(item["class_type"], 170)
        node = {"id": int(key), "type": item["class_type"], "pos": positions[int(key)],
                "size": [350, height],
                "flags": {}, "order": len(nodes), "mode": 0, "inputs": inputs,
                "outputs": [{"name": typ, "type": typ, "links": []} for typ in definition["output"]],
                "properties": {"Node name for S&R": item["class_type"]}, "widgets_values": widget_values}
        nodes.append(node)
        lookup[key] = node
    for key, item in graph.items():
        for slot, socket in enumerate(lookup[key]["inputs"]):
            source, out_slot = item["inputs"][socket["name"]]
            output = lookup[source]["outputs"][out_slot]
            assert output["type"] == socket["type"]
            link = len(links) + 1
            socket["link"] = link
            output["links"].append(link)
            links.append([link, int(source), out_slot, int(key), slot, socket["type"]])
    return {"last_node_id": 10, "last_link_id": len(links), "nodes": nodes, "links": links,
            "groups": [], "config": {}, "extra": {}, "version": 0.4}


if __name__ == "__main__":
    with urllib.request.urlopen("http://127.0.0.1:8189/object_info") as response:
        schema = json.load(response)
    destination = ROOT / "production/workflows"
    destination.mkdir(parents=True, exist_ok=True)
    for kind in ("realvisxl", "realistic-vision", "z-image-turbo"):
        graph = make_graph(kind)
        workflow = ui_workflow(graph, schema)
        path = destination / f"{kind}-portrait.json"
        path.write_text(json.dumps(workflow, indent=2) + "\n", encoding="utf-8")
        print(path)
