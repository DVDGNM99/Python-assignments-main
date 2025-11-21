# tools\make_shortcut.ps1


$ErrorActionPreference = "Stop"

$ScriptPath  = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptPath

$TargetBat = Join-Path $ProjectRoot "scripts\run_launcher.bat"
$IconPath  = Join-Path $ProjectRoot "assets\icon.ico"

$Desktop   = [Environment]::GetFolderPath('Desktop')  
$Shortcut  = Join-Path $Desktop "Chem-Reporter.lnk"

# Sanity check
if (-not (Test-Path $TargetBat)) { throw "Missing file: $TargetBat" }
if (-not (Test-Path $IconPath))  { Write-Host "Warning: icon not found, using default"; $IconPath = $TargetBat }

$WshShell = New-Object -ComObject WScript.Shell
$Lnk = $WshShell.CreateShortcut($Shortcut)
$Lnk.TargetPath = $TargetBat
$Lnk.WorkingDirectory = $ProjectRoot
$Lnk.IconLocation = $IconPath
$Lnk.WindowStyle = 1
$Lnk.Save()

Write-Host "Shortcut created:" $Shortcut
ii $Desktop  
