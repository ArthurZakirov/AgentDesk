$wslConfigPath = Join-Path $HOME ".wslconfig"
$content = @"
[wsl2]
networkingMode=mirrored
dnsTunneling=true
"@

Set-Content -Path $wslConfigPath -Value $content -NoNewline
Write-Output "Wrote $wslConfigPath"
