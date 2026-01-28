# Deployment Guide

## Project Status ✅

Your Weather API Dashboard is now **production-ready**. All components have been tested and configured.

---

## Quick Reference

| Component | Status | Location |
|-----------|--------|----------|
| Environment Setup | ✅ Ready | `.env` + `.env.example` |
| Dependencies | ✅ Installed | `requirements.txt` |
| Development Server | ✅ Configured | `run_dev.ps1` |
| Production Server | ✅ Configured | `run_production.ps1` |
| Database | ✅ Initialized | `instance/weather_dashboard.db` |
| Logging | ✅ Enabled | All `.py` files |
| Error Handling | ✅ Implemented | API, Database, Networking |

---

## Setup Checklist

- [x] Dependencies installed (`waitress` added for production)
- [x] Database initialized for production app
- [x] Environment variables configured in `.env`
- [x] Error handling with logging implemented
- [x] Startup scripts created for easy launching
- [x] API timeout handling added
- [x] Connection error handling added

---

## How to Run

### First Time Setup
```powershell
.\setup.ps1
```

### Subsequent Runs

**Development (Testing & Development):**
```powershell
.\run_dev.ps1
```
- Auto-reloads on code changes
- Port: 5000
- Perfect for development

**Production (Deployment):**
```powershell
.\run_production.ps1
```
- Uses Waitress (professional WSGI server)
- Port: 8000
- Safe for production use

---

## Configuration

### Required: Edit `.env` File

```powershell
notepad .env
```

Must have:
```env
OPENWEATHER_API_KEY=your_key_here
```

Get free key: https://openweathermap.org/api

### Optional Settings
```env
OPENWEATHER_CITY=Bengaluru
OPENWEATHER_UNITS=metric
DEBUG=False
```

---

## Features Overview

### Development App (`app.py`)
- ✅ Simple dashboard
- ✅ Manual data entry
- ✅ API integration
- ✅ CSV export
- ✅ Visualization

### Production App (`app_production.py`)
- ✅ User authentication
- ✅ Multi-user support
- ✅ Database persistence
- ✅ Weather alerts
- ✅ Email notifications
- ✅ Background scheduling

---

## Troubleshooting

### "Module not found" Error
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "API key not working"
1. Generate new key: https://openweathermap.org/api
2. Update `.env` file
3. Restart app

### "Port already in use"
Edit `run_dev.ps1` or `run_production.ps1` and change port number

### "Database locked"
Close all instances of the app and try again

### View Logs
Logs print to console. For persistent logs, add to `.env`:
```env
LOG_LEVEL=DEBUG
```

---

## Deployment Options

### Windows IIS
1. Install Python
2. Create virtual environment
3. Install dependencies
4. Use `waitress` or FastCGI handler

### AWS/Azure/Google Cloud
```bash
# Linux deployment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:8000 app_production:app
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python init_db.py
EXPOSE 8000
CMD ["waitress-serve", "--port=8000", "--threads=4", "app_production:app"]
```

### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
```

---

## Testing

Verify everything works:

```powershell
# Test development app
python -c "import app; print('✓ Development app OK')"

# Test production app
python -c "import app_production; print('✓ Production app OK')"

# Check dependencies
pip list

# Test database
python init_db.py
```

---

## Project Files

```
Weather_API_Dashboard/
├── app.py                  # Development app
├── app_production.py       # Production app (with DB, auth)
├── weather_dashboard.py    # CLI dashboard
├── requirements.txt        # Dependencies (NOW includes waitress)
├── .env                    # Configuration (your API key)
├── .env.example            # Configuration template
├── init_db.py              # Database initializer
├── setup.ps1               # Automated setup script
├── run_dev.ps1             # Development launcher
├── run_production.ps1      # Production launcher
├── QUICK_START.md          # Quick reference
├── INSTALLATION.md         # Installation guide
├── README.md               # Main documentation
├── instance/
│   └── weather_dashboard.db  # SQLite database
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
└── README_PRODUCTION.md    # Production features guide
```

---

## What's Been Configured

✅ **Production WSGI Server** - `waitress` for safe deployment
✅ **Error Handling** - Connection, timeout, API errors
✅ **Logging** - Info, error, warning messages
✅ **Database** - SQLite initialized
✅ **Startup Scripts** - One-click launch
✅ **Environment Config** - `.env` with all options
✅ **Documentation** - Complete guides

---

## Ready for Deployment! 🚀

Your project is fully configured and ready to run on any system with Python 3.8+.

Just ensure:
1. ✅ Python 3.8+ installed
2. ✅ `.env` file configured with API key
3. ✅ Run `setup.ps1` on new machines

**Start now:**
```powershell
.\run_dev.ps1       # Development
.\run_production.ps1  # Production
```

---

## Support

- **API Issues?** Check https://openweathermap.org/api
- **Python Issues?** Ensure Python 3.8+ with `python --version`
- **Database Issues?** Delete `instance/weather_dashboard.db` and run `python init_db.py`
- **Port Issues?** Change port in startup scripts

**All errors are logged to console - check the output for clues!**
