param(
    [string]$BrowserPort = "9223",
    [string]$BridgePort = "9333"
)

$ruleName = "Codex Host Browser $BridgePort"

netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=$BridgePort | Out-Null
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=$BridgePort connectaddress=127.0.0.1 connectport=$BrowserPort | Out-Null

netsh advfirewall firewall delete rule name="$ruleName" | Out-Null
netsh advfirewall firewall add rule name="$ruleName" dir=in action=allow protocol=TCP localport=$BridgePort | Out-Null

Write-Output "Configured portproxy 0.0.0.0:$BridgePort -> 127.0.0.1:$BrowserPort"
