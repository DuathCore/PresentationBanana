# Stellt sicher dass User-PATH (npm, etc.) verfügbar ist
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' +
            [System.Environment]::GetEnvironmentVariable('Path','User')

Set-Location $PSScriptRoot

Write-Host ''
Write-Host '  PresentationBanana' -ForegroundColor Yellow
Write-Host '  Tipp: /presentation-banana eintippen' -ForegroundColor Cyan
Write-Host ''

claude --dangerously-skip-permissions
