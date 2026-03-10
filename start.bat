@echo off
set SCRIPT=%~dp0launcher.ps1

:: Windows Terminal (wt.exe) - beste TUI-Unterstützung
where wt >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    wt.exe new-tab --title "PresentationBanana" powershell -NoExit -ExecutionPolicy Bypass -File "%SCRIPT%"
    exit /b 0
)

:: Fallback: PowerShell Core
where pwsh >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    pwsh -NoExit -ExecutionPolicy Bypass -File "%SCRIPT%"
    exit /b 0
)

:: Fallback: Windows PowerShell
where powershell >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    powershell -NoExit -ExecutionPolicy Bypass -File "%SCRIPT%"
    exit /b 0
)

echo Kein kompatibles Terminal gefunden.
pause
