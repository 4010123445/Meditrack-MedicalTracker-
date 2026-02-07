$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath
python main.py
Read-Host "Press Enter to close"
