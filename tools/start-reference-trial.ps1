#requires -Version 7.0
# Isolated reference-conditioning research server; existing browser service is retained.
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$base=Join-Path $root '.local\reference-comfy'
$runtime=Join-Path $root '.local\comfy\ComfyUI_windows_portable'
$logs=Join-Path $root '.local\runs'
try { $s=Invoke-RestMethod http://127.0.0.1:8189/system_stats -TimeoutSec 2; if($s.system.comfyui_version){Write-Output 'Reference server already listening';exit 0} } catch {}
$job=Join-Path $logs 'reference-comfy.json'
if(Test-Path $job){$old=Get-Content $job -Raw | ConvertFrom-Json;if(Get-Process -Id $old.pid -ErrorAction SilentlyContinue){throw 'Existing reference PID alive; inspect before restart'}}
$weightDir=Join-Path $root '.local\models\reference-conditioning'
foreach($file in @('ip-adapter-plus_sd15.safetensors','CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors')){
 $meta=Get-Content (Join-Path $weightDir "$file.source.json") -Raw | ConvertFrom-Json
 $path=Join-Path $weightDir $file
 if((Get-Item $path).Length -ne $meta.bytes -or (Get-FileHash $path -Algorithm SHA256).Hash.ToLower() -ne $meta.sha256){throw "Unverified weight: $file"}
}
# Do not run concurrent GPU jobs or interrupt queued user work.
$q=Invoke-RestMethod http://127.0.0.1:8188/queue
if($q.queue_running.Count -gt 0 -or $q.queue_pending.Count -gt 0){throw 'Main server has queued work; wait before reference trial'}
Invoke-RestMethod http://127.0.0.1:8188/free -Method Post -ContentType application/json -Body '{"unload_models":true,"free_memory":true}' | Out-Null
& "$runtime\python_embeded\python.exe" -s (Join-Path $root 'tools/run-comfy.py') --check-memory
if($LASTEXITCODE -ne 0){throw 'Memory preflight failed'}
New-Item -ItemType Directory -Force $base,(Join-Path $base 'custom_nodes'),(Join-Path $base 'user') | Out-Null
$projectPath=$root.Replace('\','/')
@"
reference_trial:
    base_path: $projectPath
    checkpoints: .local/models
    clip_vision: .local/models/reference-conditioning
    ipadapter: .local/models/reference-conditioning
    custom_nodes: .local/reference-adapter-source
"@ | Set-Content (Join-Path $base 'paths.yaml') -Encoding utf8
$argsList=@('-s','ComfyUI/main.py','--windows-standalone-build','--listen','127.0.0.1','--port','8189','--base-directory',$base,'--user-directory',(Join-Path $base 'user'),'--database-url','sqlite:///:memory:','--extra-model-paths-config',(Join-Path $base 'paths.yaml'),'--lowvram','--disable-dynamic-vram','--disable-async-offload','--disable-pinned-memory','--reserve-vram','1.5','--vram-headroom','2.0','--fp32-vae','--disable-all-custom-nodes','--whitelist-custom-nodes','ComfyUI_IPAdapter_plus-a0f451a5113cf9becb0847b92884cb10cbdec0ef')
$p=Start-Process "$runtime\python_embeded\python.exe" -ArgumentList $argsList -WorkingDirectory $runtime -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logs 'reference-comfy.log') -RedirectStandardError (Join-Path $logs 'reference-comfy.err') -PassThru
@{pid=$p.Id;port=8189;started=(Get-Date).ToString('o');base=$base} | ConvertTo-Json | Set-Content $job
Write-Output "Reference server PID $($p.Id)"
