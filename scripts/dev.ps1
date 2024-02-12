param (
  [Parameter(Mandatory=$true)][string]$siteDir,
  [int]$port = 8000,
  [string]$hostname = "localhost"
)

$siteDir = Resolve-Path $siteDir

$root = $PSScriptRoot.Replace("\scripts", "")
$env:EZ_PYTHONPATH = "$root/core;$siteDir/lib/dependencies;"

$command = "$root/lib/python/python.exe $root/core/main.py $siteDir --port $port --host $hostname"

Write-Host "$command"
& cmd start "" /d $siteDir /c $command
