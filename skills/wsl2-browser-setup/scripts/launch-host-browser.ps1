param(
    [string]$BrowserPort = "9223",
    [string]$StartUrl = "https://example.com"
)

function Get-BrowserPath {
    $candidates = @(
        "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    return $null
}

$browser = Get-BrowserPath
if (-not $browser) {
    throw "No supported Windows browser found. Install Edge or Chrome."
}

$profileDir = "C:\temp\codex-host-browser-$BrowserPort"
New-Item -ItemType Directory -Force -Path $profileDir | Out-Null

$args = @(
    "--remote-debugging-port=$BrowserPort",
    "--user-data-dir=$profileDir",
    "--no-first-run",
    "--no-default-browser-check",
    "--new-window",
    $StartUrl
)

Start-Process -FilePath $browser -ArgumentList $args | Out-Null
Write-Output "Launched $browser with remote debugging on $BrowserPort"
