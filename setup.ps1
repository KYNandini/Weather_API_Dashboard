# Complete Setup Script
# Runs all necessary setup steps

Write-Host "Weather Dashboard - Complete Setup" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""

# Step 1: Create virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
} else {
    Write-Host "Virtual environment already exists" -ForegroundColor Gray
}

# Step 2: Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Step 3: Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Step 4: Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Step 5: Create .env file if not exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "WARNING: Edit .env file and add your OpenWeatherMap API key!" -ForegroundColor Red
} else {
    Write-Host ".env file already exists" -ForegroundColor Gray
}

# Step 6: Create instance folder for database
if (-not (Test-Path "instance")) {
    Write-Host "Creating instance folder..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path "instance" -Force | Out-Null
}

Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=============" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file and add your OPENWEATHER_API_KEY"
Write-Host "2. Run: .\run_dev.ps1 (for development)"
Write-Host "3. Or run: .\run_production.ps1 (for production)"
Write-Host ""
