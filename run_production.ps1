# Production Server Startup Script
# Uses Waitress WSGI server (safe for production)

Write-Host "Starting Weather Dashboard - Production Mode" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Virtual environment not activated. Activating now..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Copy .env.example to .env and configure your API key" -ForegroundColor Yellow
    exit 1
}

# Check if waitress is installed
$waitress = pip show waitress 2>$null
if (-not $waitress) {
    Write-Host "Installing waitress..." -ForegroundColor Yellow
    pip install waitress
}

Write-Host "Starting Waitress production server..." -ForegroundColor Cyan
Write-Host "Open: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press CTRL+C to stop" -ForegroundColor Yellow
Write-Host ""

waitress-serve --port=8000 --threads=4 app_production:app
