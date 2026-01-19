# Installation Guide

Detailed step-by-step installation instructions for all platforms.

## Table of Contents
- [Requirements](#requirements)
- [Windows Installation](#windows-installation)
- [macOS Installation](#macos-installation)
- [Linux Installation](#linux-installation)
- [Troubleshooting](#troubleshooting)

## Requirements

- **Python:** 3.8 or higher ([Download](https://www.python.org/downloads/))
- **pip:** Latest version (usually included with Python)
- **Git:** For cloning repository ([Download](https://git-scm.com/))
- **Text Editor:** VSCode, PyCharm, Sublime, etc. (optional)
- **OpenWeatherMap API Key:** Free from https://openweathermap.org/api

## Windows Installation

### Step 1: Install Python

1. Download Python 3.8+ from https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation in PowerShell:
```powershell
python --version
pip --version
```

### Step 2: Clone Repository

Open PowerShell and run:
```powershell
git clone https://github.com/yourusername/Weather-API-Dashboard.git
cd Weather-API-Dashboard
```

Or download ZIP from GitHub and extract.

### Step 3: Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` in command prompt.

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- SQLAlchemy (database)
- Pandas (data processing)
- Matplotlib (visualization)
- Requests (HTTP client)
- And more...

### Step 5: Create Environment File

```powershell
cp .env.example .env
```

Edit `.env` file:
```
OPENWEATHER_API_KEY=your_api_key_here
SECRET_KEY=your-secret-key
```

### Step 6: Run Application

```powershell
python app_production.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 7: Open in Browser

Visit: `http://localhost:5000`

---

## macOS Installation

### Step 1: Install Python

Using Homebrew (recommended):
```bash
brew install python@3.11
```

Or download from https://www.python.org/downloads/

Verify:
```bash
python3 --version
pip3 --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/Weather-API-Dashboard.git
cd Weather-API-Dashboard
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Create Environment File

```bash
cp .env.example .env
# Edit .env with your API key
```

### Step 6: Run Application

```bash
python app_production.py
```

### Step 7: Open in Browser

Visit: `http://localhost:5000`

---

## Linux Installation

### Step 1: Install Python & Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip git
```

**Fedora/RHEL:**
```bash
sudo dnf install python3.11 python3.11-venv python3-pip git
```

**Arch:**
```bash
sudo pacman -S python pip git
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/Weather-API-Dashboard.git
cd Weather-API-Dashboard
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Create Environment File

```bash
cp .env.example .env
nano .env  # Edit with your API key
```

### Step 6: Run Application

```bash
python app_production.py
```

### Step 7: Open in Browser

Visit: `http://localhost:5000`

---

## Docker Installation (Optional)

If you have Docker installed:

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app_production.py"]
```

### Build and Run

```bash
docker build -t weather-dashboard .
docker run -p 5000:5000 weather-dashboard
```

---

## Troubleshooting

### Python Not Found
**Error:** `python: command not found`

**Solution (Windows):**
- Reinstall Python and check "Add Python to PATH"
- Use `python -m venv` instead of `venv`

**Solution (macOS/Linux):**
- Use `python3` instead of `python`
- Update PATH in ~/.bashrc or ~/.zshrc

### pip Install Fails
**Error:** `pip: command not found`

**Solution:**
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Virtual Environment Not Activating
**Error:** `No module named virtualenv`

**Solution:**
```bash
python -m venv .venv --clear
# Then activate again
```

### Port 5000 Already in Use
**Error:** `Address already in use`

**Solution (Windows):**
```powershell
# Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution (macOS/Linux):**
```bash
lsof -i :5000
kill -9 <PID>
```

Or change port in `app_production.py`:
```python
if __name__ == '__main__':
    app.run(debug=False, port=5001, use_reloader=False)
```

### Database Error
**Error:** `database is locked`

**Solution:**
```bash
# Delete database and restart
rm weather_dashboard.db
python app_production.py
```

### API Key Invalid
**Error:** `API Error: 401`

**Solution:**
1. Verify API key from OpenWeatherMap account
2. Key may take few minutes to activate after creation
3. Ensure key has access to 5-day forecast endpoint
4. Check `.env` file has correct key (no extra spaces)

### Import Error
**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Activate venv first, then install
pip install -r requirements.txt
```

---

## Next Steps

1. **Create Account:**
   - Register with username, email, password
   - Log in to dashboard

2. **Add Weather Data:**
   - Option A: Add manually
   - Option B: Fetch from API

3. **View Dashboard:**
   - Generate visualization
   - Export to CSV

4. **Configure Alerts:**
   - Set temperature threshold
   - Set humidity threshold

---

## Need Help?

- Check [README.md](README.md)
- View [GitHub Issues](https://github.com/yourusername/Weather-API-Dashboard/issues)
- Contact: your.email@example.com

Happy weather monitoring! 🌤️
