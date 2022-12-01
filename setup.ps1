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


if (!(Test-Path ./.venv)) {
  Info "Creating virtual environment..."
  $venvOutput = (py -m venv .venv 2>&1) -join "`n"
  if ($LASTEXITCODE -ne 0) {
    Error "$venvOutput`n"
    Error "ERROR: Failed to create virtual environment."
    If(Test-Path ./.venv) {
      Remove-Item -Recurse -Force ./.venv
    }
    Exit 1
  }
}

Write-Output "import os;import sys;sys.path.insert(0, os.environ['VIRTUAL_ENV'].replace(os.sep + '.venv', '') + os.sep + 'src')" | Out-File -FilePath .venv\Lib\site-packages\dev.pth -Encoding ascii

Info "Installing dependencies..."
.venv\Scripts\Activate.ps1
$pipOutput = (pip install -r reqs.txt 2>&1) -join "`n"
if ($LASTEXITCODE -ne 0) {
  Error $pipOutput
  Write-Host " " -ForegroundColor $WHITE
  Error "ERROR: Failed to install dependencies."
  Exit 1
}
Success "Done"

Write-Output "
To activate the virtual environment, run:

    venv/Scripts/Activate.ps1


You can now run the app with:

    python3 src/main.py


or watch for changes with:

    watchfiles ""python3 src/main.py"" src
"
Info "Happy coding!
"