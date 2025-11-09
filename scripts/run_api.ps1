# Activate virtual environment and start the API (PowerShell).

param(
    [string]$VenvPath = ".\.venv"
)

$activateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
if (-Not (Test-Path $activateScript)) {
    Write-Error "Virtual environment not found at $VenvPath"
    exit 1
}

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& $activateScript

Write-Host "Starting CalmMind API..." -ForegroundColor Cyan
uvicorn app.main:app --reload

