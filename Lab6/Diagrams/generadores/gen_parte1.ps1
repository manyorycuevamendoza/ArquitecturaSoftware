$ErrorActionPreference = 'Stop'
$sourcePath = Join-Path $PSScriptRoot 'gen_parte1.source.ps1'
$env:LAB6_UTF8_BOOTSTRAPPED = '1'
$env:LAB6_DIAGRAM_GENERATOR_ROOT = $PSScriptRoot
$source = [System.IO.File]::ReadAllText(
    $sourcePath,
    [System.Text.Encoding]::UTF8
)
Invoke-Expression $source
