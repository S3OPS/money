Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $scriptDir 'complete-setup.sh'

$bash = Get-Command bash -ErrorAction SilentlyContinue
if ($null -eq $bash) {
    $gitBash = Join-Path ${env:ProgramFiles} 'Git\bin\bash.exe'
    if (-not (Test-Path $gitBash)) {
        $gitBash = Join-Path ${env:ProgramFiles(x86)} 'Git\bin\bash.exe'
    }
    if (Test-Path $gitBash) {
        $bash = Get-Command $gitBash
    }
}

if ($null -eq $bash) {
    Write-Error "Bash is required to run scripts\complete-setup.sh. Install Git Bash (https://gitforwindows.org) or use WSL."
}

& $bash.Source $scriptPath @args
exit $LASTEXITCODE
