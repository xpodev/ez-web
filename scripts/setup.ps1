$RED = [ConsoleColor]::Red
$GREEN = [ConsoleColor]::Green
$YELLOW = [ConsoleColor]::Yellow
$BLUE = [ConsoleColor]::Blue

$WHITE = [ConsoleColor]::White

function Error {
  param (
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message
  )

  Write-Host "$Message" -ForegroundColor $RED -NoNewline
  Write-Host " " -ForegroundColor $WHITE
}

function Warning {
  param (
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message
  )

  Write-Host "$Message" -ForegroundColor $YELLOW -NoNewline
  Write-Host " " -ForegroundColor $WHITE
}

function Success {
  param (
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message
  )

  Write-Host "$Message" -ForegroundColor $GREEN -NoNewline
  Write-Host " " -ForegroundColor $WHITE
}

function Info {
  param (
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message
  )

  Write-Host "$Message" -ForegroundColor $BLUE -NoNewline
  Write-Host " " -ForegroundColor $WHITE
}

if (!(Get-Command "pip" -ErrorAction SilentlyContinue)) {
  Error "pip is not installed. Please install it and try again."
  Exit 1
}

function Load {
    param(
      [ScriptBlock]$function,
      [string]$Label,
      [string]$LabelColor = "White",
      [string[]]$PassArgs = @()
    )

    $job = Start-Job -ScriptBlock ${function} -ArgumentList $PassArgs -Init ([ScriptBlock]::Create("Set-Location $PSScriptRoot"))

    $symbols = @("-", "\", "|", "/")
    $i = 0;
    while ($job.State -eq "Running") {
        $symbol =  $symbols[$i]
        Write-Host -NoNewLine "`r$Label $symbol" -ForegroundColor $LabelColor
        Start-Sleep -Milliseconds 100
        $i++
        if ($i -eq $symbols.Count){
            $i = 0;
        }   
    }

    if ($job.State -eq "Completed") {
        Write-Host `b"OK" -ForegroundColor $GREEN
    } else {
      Write-Host -NoNewLine `b"Failed" -ForegroundColor $RED
      $error = Receive-Job $job
      Write-Host $error
      return 1
    }
}

$rootDir = Split-Path -Path $PSScriptRoot -Parent
$pythonPath = Join-Path $rootDir "lib/python/python.exe"

function InstallEmbeddablePython {
  param (
    [Parameter(Mandatory=$true)][string]$rootDir,
    [Parameter(Mandatory=$true)][string]$pythonPath
  )

  if (Test-Path $pythonPath) {
    return
  }

  $arcitecture = if ([System.Environment]::Is64BitProcess) { "amd64" } else { "win32" }
  $isArm = (Get-WmiObject -Class Win32_Processor | Select-Object -First 1).Name -match "arm"
  if ($isArm) {
    $arcitecture = "arm64"
  }
  $pythonVersion = "3.11.8"
  $pythonUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-embed-$arcitecture.zip"

  $pythonZip = Join-Path $env:TEMP "python.zip"

  $webClient = New-Object System.Net.WebClient
  $webClient.DownloadFile($pythonUrl, $pythonZip)

  $destinationPath = Join-Path $rootDir "lib/python"

  if (!(Test-Path $destinationPath)) {
    New-Item -ItemType Directory -Path $destinationPath
  }

  Expand-Archive -Path $pythonZip -DestinationPath $destinationPath
  Remove-Item -Path $pythonZip

  # python311._pth file causes issues with PYTHONPATH
  $py311PthFile = Join-Path $destinationPath  "python311._pth"
  Remove-Item -Path $py311PthFile
}

function InstallPip {
  param (
    [Parameter(Mandatory=$true)][string]$pythonPath
  )
  $pipPath = Join-Path (Split-Path -Path $pythonPath -Parent) "Scripts/pip.exe"
  if (Test-Path $pipPath) {
    return
  }

  $pipDownloadUrl = "https://bootstrap.pypa.io/get-pip.py"
  
  $pythonDir = Split-Path -Path $pythonPath -Parent
  $pipScript = Join-Path $pythonDir "get-pip.py"

  $webClient = New-Object System.Net.WebClient
  $webClient.DownloadFile($pipDownloadUrl, $pipScript)

  & $pythonPath $pipScript
}

function InstallDependencies {
  param (
    [Parameter(Mandatory=$true)][string]$pythonPath
  )

  $requiremnets = @("sqlalchemy", "argon2-cffi", "python-dotenv", "fastapi", "python-socketio", "uvicorn", "pyYAML")

  $requiremnets | ForEach-Object {
    & $pythonPath -m pip install $_
  }  
}

function InstallCoreModules {
  param (
    [Parameter(Mandatory=$true)][string]$rootDir,
    [Parameter(Mandatory=$true)][string]$pythonPath
  )

  $coreModules = @("jsx")

  $coreModulesPath = Join-Path $rootDir "core"
  $coreModules | ForEach-Object {
    & $pythonPath -m pip install $_ --target $coreModulesPath
    Get-ChildItem -Path $coreModulesPath -Filter "$_*" -Recurse | Where-Object { $_.Name -match ".*\.dist-info" } | Remove-Item -Recurse -Force
  }
}

Load -function ${function:InstallEmbeddablePython} -Label "Installing Python" -LabelColor $BLUE -PassArgs $rootDir, $pythonPath
Load -function ${function:InstallPip} -Label "Installing pip" -LabelColor $BLUE -PassArgs $pythonPath
Load -function ${function:InstallDependencies} -Label "Installing dependencies" -LabelColor $BLUE -PassArgs $pythonPath
Load -function ${function:InstallCoreModules} -Label "Installing core modules" -LabelColor $BLUE -PassArgs $rootDir, $pythonPath

Write-Output "
You can now run the app with:

    ./scripts/dev.ps1 <path_to_site_dir>
"
Info "Happy coding!
"