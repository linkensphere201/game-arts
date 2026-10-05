#requires -Version 7.0
param([switch]$IncludeSDXL)
$ErrorActionPreference = 'Stop'
$root = (Join-Path (Split-Path $PSScriptRoot -Parent) '.local\models')
New-Item -ItemType Directory -Force $root | Out-Null
$specs = @(
 @{Repo='stabilityai/stable-diffusion-xl-base-1.0'; Revision='462165984030d82259a11f4367a4eed129e94a7b'; File='sd_xl_base_1.0.safetensors'},
 @{Repo='nerijs/pixel-art-xl'; Revision='8bf4a4d9ea283e00a51fafda8e0539f8248ea037'; File='pixel-art-xl.safetensors'},
 @{Repo='Lykon/DreamShaper'; Revision='228d79cb20811466f5c5710aa91f05dabd0b8a14'; File='DreamShaper_8_pruned.safetensors'}
)
if (-not $IncludeSDXL) { $specs = @($specs | Where-Object Repo -EQ "Lykon/DreamShaper") }
foreach ($spec in $specs) {
 $info = Invoke-RestMethod "https://huggingface.co/api/models/$($spec.Repo)/revision/$($spec.Revision)?blobs=true"
 $fileInfo = $info.siblings | Where-Object rfilename -EQ $spec.File
 $revision = $info.sha
 @{repo=$spec.Repo;revision=$revision;file=$spec.File;metadata=$fileInfo} | ConvertTo-Json -Depth 6 | Set-Content "$root\$($spec.File).source.json"
 Write-Output "Downloading $($spec.File) revision $revision"
 if (-not (Test-Path "$root\$($spec.File)") -or (Get-Item "$root\$($spec.File)").Length -ne $fileInfo.size) {
 & curl.exe -L --fail --retry 3 --connect-timeout 30 -C - -o "$root\$($spec.File)" "https://huggingface.co/$($spec.Repo)/resolve/$revision/$($spec.File)"
 if ($LASTEXITCODE -ne 0) { throw 'Model download failed' }
 }
 $hash = (Get-FileHash "$root\$($spec.File)" -Algorithm SHA256).Hash.ToLower()
 if ($fileInfo.lfs.sha256 -and $hash -ne $fileInfo.lfs.sha256) { throw 'Model checksum mismatch' }
 Write-Output "Verified $($spec.File) $hash"
}
Write-Output 'MODELS_COMPLETE'
