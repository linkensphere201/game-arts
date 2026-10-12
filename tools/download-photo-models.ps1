param([int]$Index = -1, [switch]$IncludeZImage)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$models = @(Get-Content "$PSScriptRoot/photo-models.json" -Raw | ConvertFrom-Json)
if ($Index -ge 0) { $models = @($models[$Index]) }
elseif (-not $IncludeZImage) { $models = @($models[0..2]) }
foreach ($model in $models) {
    $path = Join-Path $root $model.destination
    New-Item -ItemType Directory -Force (Split-Path $path -Parent) | Out-Null
    $model | ConvertTo-Json | Set-Content "$path.source.json"
    Write-Output "Downloading $($model.file)"
    if (-not (Test-Path $path) -or (Get-Item $path).Length -lt $model.bytes) {
        $url = "https://huggingface.co/$($model.repository)/resolve/$($model.revision)/$($model.file)"
        & curl.exe -L --fail --silent --show-error --retry 3 --connect-timeout 30 -C - -o $path $url
        if ($LASTEXITCODE -ne 0) { throw 'Download failed; partial file retained for resume' }
    }
    if ((Get-Item $path).Length -ne $model.bytes) { throw "Length mismatch: $path" }
    if ((Get-FileHash $path -Algorithm SHA256).Hash.ToLower() -ne $model.sha256) { throw "Hash mismatch: $path" }
    Write-Output "VERIFIED $($model.file)"
}
