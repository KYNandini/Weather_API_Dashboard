# Quick Start Guide

## One-Time Setup (First Time Only)

### Option 1: Automated Setup (Recommended)
```powershell
.\setup.ps1
```
This script will:
- Create virtual environment
- Install all dependencies
- Create .env file
- Initialize database

### Option 2: Manual Setup
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Initialize database
python init_db.py
```

---

## Running the Application

### Development Mode (Testing)
```powershell
.\run_dev.ps1
```
- Uses Flask development server
- Auto-reloads on code changes
- Visit: http://localhost:5000

### Production Mode (Deployment)
```powershell
.\run_production.ps1
```
- Uses Waitress WSGI server
- Safe for production
- Visit: http://localhost:8000

---

## Configuration

Edit `.env` file with your settings:

```env
# Required
OPENWEATHER_API_KEY=your_api_key_here

# Optional
OPENWEATHER_CITY=Bengaluru
OPENWEATHER_UNITS=metric
```

Get free API key: https://openweathermap.org/api

---

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Make sure virtual environment is activated
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: ".env not found"
**Solution:** Create it from the example
```powershell
copy .env.example .env
```

### Issue: "API fetch failed"
**Solution:** Verify API key in .env is valid
```powershell
# Test the API key
$key = "your_api_key"
curl "https://api.openweathermap.org/data/2.5/forecast?q=Bengaluru&appid=$key&units=metric"
```

### Issue: "Port already in use"
**Solution:** Change port in the startup scripts or stop the other service

---

## Features Available

### Simple Dashboard (app.py)
- Manual weather entry
- Fetch from API
- Generate visualizations
- Export to CSV

### Full-Featured (app_production.py)
- User authentication
- Database storage
- Multiple users
- Weather alerts
- Email notifications
- Background scheduling

---

## Deployment

### Windows (IIS)
Use `app_production.py` with Waitress as WSGI server

### Linux/Cloud
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app_production:app
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["waitress-serve", "--port=8000", "app_production:app"]
```

---

## Support

For issues, check:
1. `.env` file is configured
2. Virtual environment is activated
3. All dependencies installed: `pip list`
4. API key is valid
5. Port is not in use
