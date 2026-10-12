#requires -Version 7.0
# Bounded local support weights for DreamShaper / SD1.5 reference-conditioning trials.
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$target=Join-Path $root '.local\models\reference-conditioning'
New-Item -ItemType Directory -Force $target | Out-Null
$revision='018e402774aeeddd60609b4ecdb7e298259dc729'
$files=@(
 @{Remote='models/ip-adapter-plus_sd15.safetensors';Name='ip-adapter-plus_sd15.safetensors';Bytes=98183288;SHA256='a1c250be40455cc61a43da1201ec3f1edaea71214865fb47f57927e06cbe4996'},
 @{Remote='models/image_encoder/model.safetensors';Name='CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors';Bytes=2528373448;SHA256='6ca9667da1ca9e0b0f75e46bb030f7e011f44f86cbfb8d5a36590fcd7507b030'}
)
foreach($entry in $files){
 $path=Join-Path $target $entry.Name
 $url="https://huggingface.co/h94/IP-Adapter/resolve/$revision/$($entry.Remote)"
 @{repository='h94/IP-Adapter';revision=$revision;file=$entry.Remote;bytes=$entry.Bytes;sha256=$entry.SHA256;url=$url} | ConvertTo-Json | Set-Content "$path.source.json"
 Write-Output "START $($entry.Name) expected $($entry.Bytes) bytes"
 if(-not(Test-Path -LiteralPath $path) -or (Get-Item -LiteralPath $path).Length -ne $entry.Bytes){
  & curl.exe -L --fail --silent --show-error --retry 2 --connect-timeout 30 -C - -o $path $url
  if($LASTEXITCODE -ne 0){throw "Download failed: $($entry.Name); retain partial for resume"}
 }
 if((Get-Item -LiteralPath $path).Length -ne $entry.Bytes){throw 'Length mismatch'}
 if((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower() -ne $entry.SHA256){throw 'Hash mismatch; retained file needs inspection'}
 Write-Output "VERIFIED $($entry.Name)"
}
Write-Output 'REFERENCE_MODELS_VERIFIED'
