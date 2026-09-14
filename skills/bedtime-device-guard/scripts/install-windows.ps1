$ErrorActionPreference = "Stop"

$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Error "Python 3 is required to install the bedtime guard."
    exit 1
}
& py -3 (Join-Path $scriptDirectory "install_guard.py") install @args
exit $LASTEXITCODE
