#requires -Version 7.0
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$runtime=Join-Path $root '.local\comfy\ComfyUI_windows_portable'
$runDir=Join-Path $root '.local\runs'
New-Item -ItemType Directory -Force $runDir | Out-Null
$checkpoint=Join-Path $root '.local\models\DreamShaper_8_pruned.safetensors'
if (-not (Test-Path -LiteralPath $checkpoint)) {
 throw 'MVP checkpoint missing. Run tools/download-models.ps1 before starting ComfyUI.'
}
# Install a named workflow without replacing browser tabs or user edits.
$workflowDir=Join-Path $runtime 'ComfyUI\user\default\workflows'
New-Item -ItemType Directory -Force $workflowDir | Out-Null
$workflowPath=Join-Path $workflowDir 'Ember Imp - DreamShaper 8.json'
if (-not (Test-Path -LiteralPath $workflowPath)) {
 Copy-Item -LiteralPath (Join-Path $root 'production\workflows\ember-imp-dreamshaper.json') -Destination $workflowPath
}
Write-Output 'Open http://127.0.0.1:8188 -> Workflows -> Refresh -> Ember Imp - DreamShaper 8 -> Run. Do not use the Z-Image template for this MVP.'
try {
 $existing=Invoke-RestMethod 'http://127.0.0.1:8188/system_stats' -TimeoutSec 2
 if ($existing.system.comfyui_version) { Write-Output 'ComfyUI already listening on port 8188'; exit 0 }
} catch {}
& "$runtime\python_embeded\python.exe" -s (Join-Path $root 'tools/run-comfy.py') --check-memory
if ($LASTEXITCODE -ne 0) { throw 'ComfyUI launch blocked by the memory preflight; see the message above.' }
$models=(Join-Path $root '.local\models').Replace('\','/')
@"
game_arts:
    base_path: $models
    checkpoints: .
    loras: .
"@ | Set-Content "$runtime\ComfyUI\extra_model_paths.yaml" -Encoding utf8
$env:GAME_ARTS_READONLY_SAFETENSORS="0"
$p=Start-Process "$runtime\python_embeded\python.exe" -ArgumentList '-s ComfyUI/main.py --windows-standalone-build --listen 127.0.0.1 --port 8188 --lowvram --disable-dynamic-vram --disable-async-offload --disable-pinned-memory --reserve-vram 1.5 --vram-headroom 2.0 --fp32-vae --disable-all-custom-nodes' -WorkingDirectory $runtime -WindowStyle Hidden -RedirectStandardOutput "$runDir\comfy.stdout.log" -RedirectStandardError "$runDir\comfy.stderr.log" -PassThru
@{pid=$p.Id;started=(Get-Date).ToString('o');port=8188;host='127.0.0.1';runtime=$runtime} | ConvertTo-Json | Set-Content "$runDir\comfy.json"
Write-Output "ComfyUI PID $($p.Id); logs: $runDir"
