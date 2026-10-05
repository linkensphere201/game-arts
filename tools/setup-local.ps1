#requires -Version 7.0
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot -Parent) '.local'
New-Item -ItemType Directory -Force "$root\downloads" | Out-Null
$items = @(
 @{Name='godot.zip'; Size=86013866; Url='https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_win64.exe.zip'},
 @{Name='godot-sha512.txt'; Size=5682; Url='https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/SHA512-SUMS.txt'},
 @{Name='comfy.7z'; Size=1994326521; Url='https://github.com/Comfy-Org/ComfyUI/releases/download/v0.38.0/ComfyUI_windows_portable_nvidia.7z'}
)
foreach ($item in $items) {
 if ((Test-Path "$root\downloads\$($item.Name)") -and (Get-Item "$root\downloads\$($item.Name)").Length -eq $item.Size) { continue }
 Write-Output "Downloading $($item.Name)"
 & curl.exe -L --fail --retry 3 --connect-timeout 30 -C - -o "$root\downloads\$($item.Name)" $item.Url
 if ($LASTEXITCODE -ne 0) { throw "Download failed: $($item.Name)" }
}
$hash = (Get-FileHash "$root\downloads\godot.zip" -Algorithm SHA512).Hash.ToLower()
$expected = Get-Content "$root\downloads\godot-sha512.txt" | Where-Object { $_ -match 'Godot_v4.7.2-stable_win64.exe.zip$' }
if (-not $expected.StartsWith($hash)) { throw 'Godot checksum mismatch' }
$comfyHash=(Get-FileHash "$root\downloads\comfy.7z" -Algorithm SHA256).Hash.ToLower()
if ($comfyHash -ne '8f137eac345707fd7e42bcf8e29377415243011ca15522a86aed6c77331fbd56') { throw 'Comfy checksum mismatch' }
Expand-Archive "$root\downloads\godot.zip" "$root\godot" -Force
New-Item -ItemType File -Force "$root\godot\_sc_" | Out-Null
$sevenZip = @('C:\Program Files\7-Zip\7z.exe', 'C:\Program Files\NVIDIA Corporation\NVIDIA App\7z.exe') | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $sevenZip) { throw '7-Zip executable required; select an installed 7z path before extraction' }
& $sevenZip x "$root\downloads\comfy.7z" "-o$root\comfy" -y
if ($LASTEXITCODE -ne 0) { throw 'Comfy extraction failed' }
Write-Output 'SETUP_DOWNLOADS_COMPLETE'
