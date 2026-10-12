$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$revision='2b7c1b397761bf5bd3cc42e5b39ec99314a75a96'
$name='animagine-xl-4.0-opt.safetensors'
$bytes=6938350040
$sha='6327eca98bfb6538dd7a4edce22484a1bbc57a8cff6b11d075d40da1afb847ac'
New-Item -ItemType Directory -Force "$root/.local/models" | Out-Null
$path="$root/.local/models/$name"
$url="https://huggingface.co/cagliostrolab/animagine-xl-4.0/resolve/$revision/$name"
@{repository='cagliostrolab/animagine-xl-4.0';revision=$revision;file=$name;bytes=$bytes;sha256=$sha} | ConvertTo-Json | Set-Content "$path.source.json"
if(-not(Test-Path $path) -or (Get-Item $path).Length -lt $bytes){
 & curl.exe -L --fail --silent --show-error --retry 2 --connect-timeout 30 -C - -o $path $url
 if($LASTEXITCODE -ne 0){throw 'Download failed; partial retained'}
}
if((Get-Item $path).Length -ne $bytes){throw 'Length mismatch; retained for inspection'}
if((Get-FileHash $path -Algorithm SHA256).Hash.ToLower() -ne $sha){throw 'Hash mismatch; retained for inspection'}
'ANIMAGINE_VERIFIED'
