param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet("install", "verify", "uninstall")]
    [string]$Action,
    [string]$Start,
    [string]$End,
    [string]$Timezone = "local",
    [ValidateRange(1, 120)]
    [int]$WarningMinutes = 10
)

$ErrorActionPreference = "Stop"
$taskPrefix = "AgentDesk-BedtimeDeviceGuard"
$installDirectory = Join-Path $env:LOCALAPPDATA "AgentDesk\bedtime-device-guard"
$configPath = Join-Path $installDirectory "config.json"
$deviceScript = Join-Path $installDirectory "device_guard.py"
$sourceDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

function Get-ClockMinutes([string]$Value) {
    $parsed = [DateTime]::ParseExact($Value, "HH:mm", [Globalization.CultureInfo]::InvariantCulture)
    return $parsed.Hour * 60 + $parsed.Minute
}

function Get-ClockString([int]$Minutes) {
    $normalized = (($Minutes % 1440) + 1440) % 1440
    return "{0:D2}:{1:D2}" -f [Math]::Floor($normalized / 60), ($normalized % 60)
}

if ($Action -eq "uninstall") {
    foreach ($suffix in @("Warning", "Shutdown")) {
        Unregister-ScheduledTask -TaskName "$taskPrefix-$suffix" -Confirm:$false -ErrorAction SilentlyContinue
    }
    if (Test-Path -LiteralPath $installDirectory) {
        Remove-Item -LiteralPath $installDirectory -Recurse -Force
    }
    Write-Output "Removed Windows bedtime device tasks and their local configuration."
    exit 0
}

if ($Action -eq "verify") {
    $missing = @()
    foreach ($suffix in @("Warning", "Shutdown")) {
        if (-not (Get-ScheduledTask -TaskName "$taskPrefix-$suffix" -ErrorAction SilentlyContinue)) {
            $missing += $suffix
        }
    }
    if (-not (Test-Path -LiteralPath $configPath) -or -not (Test-Path -LiteralPath $deviceScript)) {
        $missing += "files"
    }
    if ($missing.Count -gt 0) {
        Write-Error "Verification failed; missing: $($missing -join ', ')"
        exit 1
    }
    Write-Output "Windows bedtime warning and forced-shutdown tasks are installed."
    exit 0
}

if (-not $Start -or -not $End) {
    throw "install requires -Start HH:mm and -End HH:mm"
}
$startMinutes = Get-ClockMinutes $Start
$endMinutes = Get-ClockMinutes $End
if ($startMinutes -eq $endMinutes) {
    throw "Start and End must differ."
}
if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python 3 is required to install the device guard."
}

New-Item -ItemType Directory -Path $installDirectory -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $sourceDirectory "bedtime_guard.py") -Destination $installDirectory -Force
Copy-Item -LiteralPath (Join-Path $sourceDirectory "device_guard.py") -Destination $installDirectory -Force
$configJson = @{
    enabled = $true
    start = $Start
    end = $End
    timezone = $Timezone
    warning_minutes = $WarningMinutes
} | ConvertTo-Json
$utf8WithoutBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($configPath, $configJson, $utf8WithoutBom)

& py -3 $deviceScript check --platform windows --config $configPath | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "The local schedule or timezone could not be validated."
}

$python = (Get-Command py).Source
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 2)
$definitions = @(
    @{
        Name = "$taskPrefix-Warning"
        Time = Get-ClockString ($startMinutes - $WarningMinutes)
        Arguments = "-3 `"$deviceScript`" warn --platform windows --config `"$configPath`""
    },
    @{
        Name = "$taskPrefix-Shutdown"
        Time = Get-ClockString $startMinutes
        Arguments = "-3 `"$deviceScript`" enforce --platform windows --config `"$configPath`""
    }
)
foreach ($definition in $definitions) {
    $trigger = New-ScheduledTaskTrigger -Daily -At $definition.Time
    $taskAction = New-ScheduledTaskAction -Execute $python -Argument $definition.Arguments
    Register-ScheduledTask -TaskName $definition.Name -Action $taskAction -Trigger $trigger `
        -Settings $settings -Principal $principal -Force | Out-Null
}
Write-Output "Installed Windows bedtime warning and forced-shutdown tasks."
