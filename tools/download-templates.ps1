#requires -Version 7.0
$ErrorActionPreference='Stop'
$root=(Join-Path (Split-Path $PSScriptRoot -Parent) '.local')
if (-not (Test-Path "$root\downloads\templates.tpz") -or (Get-Item "$root\downloads\templates.tpz").Length -ne 1281349702) {
& curl.exe -L --fail --retry 3 -C - -o "$root\downloads\templates.tpz" 'https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_export_templates.tpz'
if ($LASTEXITCODE -ne 0) { throw 'Template download failed' }
}
$hash=(Get-FileHash "$root\downloads\templates.tpz" -Algorithm SHA512).Hash.ToLower()
$line=Get-Content "$root\downloads\godot-sha512.txt" | Where-Object { $_ -match 'Godot_v4.7.2-stable_export_templates.tpz$' }
if (-not $line.StartsWith($hash)) { throw 'Template checksum mismatch' }
& 'C:\Program Files\NVIDIA Corporation\NVIDIA App\7z.exe' x -tzip "$root\downloads\templates.tpz" "-o$root\export-templates" 'templates/windows_debug_x86_64.exe' 'templates/windows_release_x86_64.exe' -y
if ($LASTEXITCODE -ne 0) { throw 'Template extraction failed' }
Write-Output 'TEMPLATES_COMPLETE'
