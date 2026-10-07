param(
    [string]$Layout = 'production/poster-demo/layout.json',
    [string]$Output = '.local/poster-cover/svg-demo/v1',
    [string]$LayerId,
    [string]$Text,
    [string]$NodePath = "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe",
    [string]$ModulePath = "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$cache = Join-Path $root '.local/poster-cover/fontconfig'
New-Item -ItemType Directory -Force $cache | Out-Null
$fontDir = [Security.SecurityElement]::Escape((Join-Path $env:WINDIR 'Fonts').Replace('\','/'))
$cacheDir = [Security.SecurityElement]::Escape($cache.Replace('\','/'))
$config = Join-Path $cache 'fonts.conf'
"<fontconfig><dir>$fontDir</dir><cachedir>$cacheDir</cachedir></fontconfig>" | Set-Content $config -Encoding utf8
$env:FONTCONFIG_FILE = $config
$env:FONTCONFIG_PATH = $cache
$env:NODE_PATH = $ModulePath
$arguments = @((Join-Path $PSScriptRoot 'compose-poster.cjs'), $Layout, $Output)
if ($LayerId) { $arguments += @($LayerId, $Text) }
& $NodePath @arguments
if ($LASTEXITCODE -ne 0) { throw "Poster rendering failed with exit code $LASTEXITCODE" }
