param(
    [string]$BrowserPort = "9223",
    [string]$BridgePort = "9333"
)

$scriptPath = Join-Path $PSScriptRoot "ensure-portproxy.ps1"
$arguments = @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", "`"$scriptPath`"",
    "-BrowserPort", $BrowserPort,
    "-BridgePort", $BridgePort
)

Start-Process -FilePath "powershell.exe" -Verb RunAs -ArgumentList $arguments -Wait | Out-Null
Write-Output "Admin bridge setup finished"
