# Development Server Startup Script
# This runs Flask development server (use for testing only)

Write-Host "Starting Weather Dashboard - Development Mode" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Virtual environment not activated. Activating now..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "WARNING: .env file not found!" -ForegroundColor Red
    Write-Host "Copy .env.example to .env and configure your API key" -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting Flask development server..." -ForegroundColor Cyan
Write-Host "Open: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Press CTRL+C to stop" -ForegroundColor Yellow
Write-Host ""

python app.py
