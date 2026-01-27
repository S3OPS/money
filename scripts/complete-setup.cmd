@echo off
setlocal

set "SCRIPT_DIR=%~dp0"

where bash >nul 2>nul
if %ERRORLEVEL%==0 (
    bash "%SCRIPT_DIR%complete-setup.sh" %*
    exit /b %ERRORLEVEL%
)

if exist "%ProgramFiles%\Git\bin\bash.exe" (
    "%ProgramFiles%\Git\bin\bash.exe" "%SCRIPT_DIR%complete-setup.sh" %*
    exit /b %ERRORLEVEL%
)

if exist "%ProgramFiles(x86)%\Git\bin\bash.exe" (
    "%ProgramFiles(x86)%\Git\bin\bash.exe" "%SCRIPT_DIR%complete-setup.sh" %*
    exit /b %ERRORLEVEL%
)

echo Bash is required to run scripts\complete-setup.sh.
echo Install Git Bash (https://gitforwindows.org) or use WSL.
echo Then run: ./scripts/complete-setup.sh
exit /b 1
