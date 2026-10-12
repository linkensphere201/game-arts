"""Bounded local img2img pilot using owned old art only as a composition guide."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, shutil, time
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('generation', ROOT/'tools/generate-character.py')
gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--id',required=True)
    p.add_argument('--category',choices=['object','character'],default='object')
    p.add_argument('--source',required=True)
    p.add_argument('--description',required=True)
    p.add_argument('--negative-extra',default='')
    p.add_argument('--denoise',type=float,default=.6)
    p.add_argument('--seed',type=int,default=752001)
    p.add_argument('--portrait',action='store_true',help='512x768 canvas and 420x600 guide envelope')
    p.add_argument('--api',default='http://127.0.0.1:8188')
    p.add_argument('--comfy-base',default='.local/comfy/ComfyUI_windows_portable/ComfyUI')
    p.add_argument('--reference-weight',type=float,default=None)
    p.add_argument('--reference-source',default='production/pixel-rpg/model-sprite-study/segmented-source.png',help='Identity image for the selected character; defaults to historical Rowan input')
    p.add_argument('--reference-region',choices=['full','upper','torso'],default='full')
    p.add_argument('--dry-run',action='store_true',help='Prepare graph and inputs without loading or queueing models')
    a=p.parse_args()
    gen.API=a.api
    comfy_base=ROOT/a.comfy_base
    (comfy_base/'input').mkdir(parents=True,exist_ok=True)
    out=ROOT/'production/pixel-rpg/model-wave-01/guided';out.mkdir(exist_ok=True)
    name=f'{a.id}-{a.seed}'
    record_path=out/f'{name}{"-dry-run" if a.dry_run else ""}.json'
    if record_path.exists():
        raise RuntimeError('Run exists; inspect its prompt_id before choosing a new trial.')
    src=ROOT/a.source
    im=Image.open(src).convert('RGBA');im=im.crop(im.getbbox())
    width,height=(512,768) if a.portrait else (512,512)
    maxw,maxh=(420,600) if a.portrait else (360,360)
    scale=min(maxw/im.width,maxh/im.height)
    im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',(width,height),'white');canvas.paste(im,((width-im.width)//2,(height-im.height)//2),im)
    guide=out/f'{name}-guide.png';canvas.save(guide)
    input_name=f'mosslight_{name}_guide.png'
    shutil.copy2(guide,comfy_base/'input'/input_name)
    positive=a.description+', hand painted anime fantasy illustration, clean dark colored contour lines, beautiful cel shading, broad simple shadow shapes, warm upper left lighting, muted teal and warm brown and antique brass, white background, single complete object, centered with margin'
    negative='photo, photorealistic, 3d render, realistic, glossy, logo, emblem, circle, border, text, watermark, person, multiple objects, cropped, cut off, blurry'
    if a.category=='character':
        positive=a.description+', full body, chibi anime JRPG character illustration, approximately four heads tall, clean dark colored outlines, cel shading, warm upper left lighting, complete single figure, feet visible, plain white background'
        negative='photo, photorealistic, 3d render, logo, border, text, watermark, multiple people, character sheet, cropped, extra limbs, malformed hands, duplicate, long legs'
    if a.negative_extra:negative+=', '+a.negative_extra
    g=gen.graph(a.seed,positive,negative)
    g['5']={'class_type':'LoadImage','inputs':{'image':input_name}}
    g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
    g['6']['inputs'].update(latent_image=['9',0],denoise=a.denoise,steps=30,cfg=6)
    if a.reference_weight is not None:
        reference_path=ROOT/a.reference_source
        ref=Image.open(reference_path).convert('RGBA')
        if ref.getchannel('A').getextrema()==(255,255):
            # White-backed model illustrations otherwise waste most of CLIP's input.
            bounds=ref.convert('L').point(lambda value:255 if value<225 else 0).getbbox()
            if bounds:ref=ref.crop(bounds)
        ref=ref.crop(ref.getbbox());ref.thumbnail((448,448),Image.Resampling.LANCZOS)
        square=Image.new('RGB',(512,512),'white');square.paste(ref,((512-ref.width)//2,(512-ref.height)//2),ref)
        reference_name=f'{name}-identity-reference.png'
        square.save(out/reference_name)
        square.save(comfy_base/'input'/reference_name)
        g['10']={'class_type':'LoadImage','inputs':{'image':reference_name}}
        g['11']={'class_type':'CLIPVisionLoader','inputs':{'clip_name':'CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors'}}
        g['12']={'class_type':'IPAdapterModelLoader','inputs':{'ipadapter_file':'ip-adapter-plus_sd15.safetensors'}}
        g['13']={'class_type':'IPAdapterAdvanced','inputs':{'model':['1',0],'ipadapter':['12',0],'image':['10',0],'clip_vision':['11',0],'weight':a.reference_weight,'weight_type':'linear','combine_embeds':'concat','start_at':0.0,'end_at':0.85,'embeds_scaling':'V only'}}
        if a.reference_region in ['upper','torso']:
            mask=Image.new('RGB',(width,height),'black');draw=ImageDraw.Draw(mask)
            start,end=round(height*.56),round(height*.68)
            draw.rectangle((0,0,width,start),fill='white')
            for y in range(start,end):
                value=round(255*(end-y)/(end-start));draw.line((0,y,width,y),fill=(value,value,value))
            if a.reference_region=='torso':
                fade_start,fade_end=round(height*.27),round(height*.36)
                draw.rectangle((0,0,width,fade_start),fill='black')
                for y in range(fade_start,fade_end):
                    value=round(255*(y-fade_start)/(fade_end-fade_start));draw.line((0,y,width,y),fill=(value,value,value))
            mask_name=f'{name}-reference-mask.png';mask.save(out/mask_name);mask.save(comfy_base/'input'/mask_name)
            g['14']={'class_type':'LoadImage','inputs':{'image':mask_name}}
            g['15']={'class_type':'ImageToMask','inputs':{'image':['14',0],'channel':'red'}}
            g['13']['inputs']['attn_mask']=['15',0]
        g['6']['inputs']['model']=['13',0]
    g['8']['inputs']['filename_prefix']=name
    rec={'id':a.id,'arguments':vars(a),'canvas':[width,height],'source':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'guide_sha256':hashlib.sha256(guide.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending','note':'Procedural composition guide -> local model illustration; not accepted sprite.'}
    if a.reference_weight is not None:
        rec.update(reference_source=str(reference_path.relative_to(ROOT)),reference_source_sha256=hashlib.sha256(reference_path.read_bytes()).hexdigest(),reference_input_sha256=hashlib.sha256((out/reference_name).read_bytes()).hexdigest())
    def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
    save()
    if a.dry_run:
        print('WORKFLOW_PREPARED_NOT_EXECUTED',record_path,flush=True);return
    key=gen.request('/prompt',{'prompt':g,'client_id':'mosslight-guided-pilot'})['prompt_id']
    rec.update(prompt_id=key,state='queued');save();print('QUEUED',key,flush=True)
    start=time.monotonic()
    while time.monotonic()-start<900:
        history=gen.request('/history/'+key)
        if key in history:
            h=history[key];rec.update(state=h['status']['status_str'],history=h,seconds=time.monotonic()-start)
            if rec['state']=='success':
                f=h['outputs']['8']['images'][0]
                dest=out/f'{name}.png'
                shutil.copy2(comfy_base/'output'/f['subfolder']/f['filename'],dest)
                rec.update(output=str(dest.relative_to(ROOT)),output_sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
            save();print(rec['state'],flush=True)
            if rec['state']!='success':raise RuntimeError(record_path)
            return
        time.sleep(2)
    raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit automatically.')
if __name__=='__main__':main()
