param (
  [Parameter(Position=0)][string]$action = 'help',
  [string]$siteDir = $PWD,
  [int]$port = 8000,
  [string]$hostname = "localhost"
)

$siteDir = Resolve-Path $siteDir
$root = Resolve-Path "$PSScriptRoot/.."
$pythonPath = Join-Path $root "lib/python/python.exe"

function RunCommand {
  param (
    [string]$command
  )

  Write-Host "Running: $command"

  & cmd start "" /d $siteDir /c $command
}

function CommandStart {

  $env:PYTHONPATH = "$root/include;$siteDir/lib/dependencies;"

  $command = "$root/lib/python/python.exe -m core.startup $siteDir --port $port --host $hostname --reload-includes $siteDir --reload-includes $root"
  RunCommand $command
}

function CommandHelp {
  Write-Host "Usage: ez [action] [options]"
  Write-Host ""
  Write-Host "Actions:"
  Write-Host "  start [siteDir] [options]  Start the web server"
  Write-Host "  help                       Show this help message"
  Write-Host ""
  Write-Host "Options:"
  Write-Host "  --port [port]              Port to run the server on"
  Write-Host "  --host [hostname]          Hostname to run the server on"
  Write-Host ""
  Write-Host "Examples:"
  Write-Host "  ez start"
  Write-Host "  ez start --port 8080"
  Write-Host "  ez start --port 8080 --host"
}

function CommandJSX {
  $command = "$pythonPath -m pip install --upgrade jsx --target ./core"

  RunCommand $command

  Get-ChildItem "./core" | Where{$_.Name -Match "jsx-.*\.dist-info"} | Remove-Item -Recurse -Force
}

& {
  switch ($action) {
    "start" { CommandStart }
    "help" { CommandHelp }
    "jsx" { CommandJSX }
    default { CommandHelp }
  }
}