# GitHub Setup Guide

Complete guide to uploading Weather API Dashboard to GitHub.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name:** `Weather-API-Dashboard`
3. **Description:** "Production-ready weather monitoring dashboard with real-time API integration"
4. **Public** (recommended) or Private
5. **DO NOT** initialize with README (we have one)
6. Click "Create repository"

## Step 2: Prepare Local Repository

In your project folder (PowerShell):

```powershell
# Initialize git if not already done
git init

# Add all files (except those in .gitignore)
git add .

# Create initial commit
git commit -m "Initial commit: Production-ready weather dashboard"

# Rename branch to main (GitHub standard)
git branch -M main
```

## Step 3: Connect to Remote Repository

Replace `yourusername` with your GitHub username:

```powershell
git remote add origin https://github.com/yourusername/Weather-API-Dashboard.git
git branch -M main
git push -u origin main
```

## Step 4: Verify Upload

1. Go to https://github.com/yourusername/Weather-API-Dashboard
2. Check all files are visible
3. Verify `.gitignore` is working (no `.db`, `.env`, `__pycache__`)

## Step 5: Add GitHub Topics

1. Go to repository Settings
2. Under "About" section, add topics:
   - `weather`
   - `dashboard`
   - `flask`
   - `python`
   - `api`
   - `open-weather-map`
   - `data-visualization`
   - `sqlite`

## Step 6: Enable Features (Optional)

In Settings:

- [x] Issues
- [x] Discussions
- [x] Projects
- [x] Wiki (optional)

## Step 7: Create Release

1. Go to "Releases"
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Weather Dashboard v1.0.0 - Production Ready`
5. Description:
```markdown
# Version 1.0 - Production Ready

## Features
- Multi-user authentication with secure password hashing
- Real-time weather data from OpenWeatherMap API
- Manual data entry for testing and logging
- Beautiful data visualization with Matplotlib
- SQLite database with full data persistence
- Advanced filtering and search capabilities
- Weather alert configuration
- Responsive mobile-friendly design

## What's New
- User authentication system
- Database integration (SQLAlchemy)
- Advanced filtering and alerts
- Production-ready configuration

## Installation
See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

## Quick Start
```bash
git clone https://github.com/yourusername/Weather-API-Dashboard.git
cd Weather-API-Dashboard
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app_production.py
```

Visit `http://localhost:5000` and start monitoring weather!

## License
MIT License - See LICENSE file
```

6. Click "Publish release"

## Step 8: Add Badge to README

Add to top of README.md:

```markdown
[![GitHub stars](https://img.shields.io/github/stars/yourusername/Weather-API-Dashboard.svg?style=social)](https://github.com/yourusername/Weather-API-Dashboard)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/Weather-API-Dashboard.svg?style=social)](https://github.com/yourusername/Weather-API-Dashboard/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/yourusername/Weather-API-Dashboard.svg?style=social)](https://github.com/yourusername/Weather-API-Dashboard)
```

Then commit:
```powershell
git add README.md
git commit -m "Add: GitHub badges to README"
git push
```

## Step 9: Setup Branch Protection (Optional)

1. Go to Settings → Branches
2. Click "Add rule"
3. Branch name pattern: `main`
4. Enable:
   - [x] Require pull request reviews
   - [x] Require status checks to pass
   - [x] Require branches to be up to date

## Step 10: Share Your Project

Announce on:
- Reddit: r/Python, r/webdev
- Stack Overflow: Tag questions
- Dev.to: Write article
- Twitter/X: Share link
- LinkedIn: Post update
- GitHub Trending: Listed automatically

## File Checklist Before Upload

Verify these files exist and are correct:

```
✓ README.md              - Comprehensive documentation
✓ INSTALLATION.md        - Setup guide for all platforms
✓ CONTRIBUTING.md        - Contribution guidelines
✓ LICENSE                - MIT License
✓ .gitignore             - Excludes sensitive files
✓ requirements.txt       - All dependencies listed
✓ .env.example           - Example configuration
✓ app_production.py      - Main application
✓ weather_dashboard.py   - Original CLI version
✓ templates/             - All HTML files
```

## What Should NOT Be Uploaded

These will be automatically ignored by `.gitignore`:

- ✗ `weather_dashboard.db` - Database file
- ✗ `.env` - Sensitive API keys
- ✗ `__pycache__/` - Python cache
- ✗ `.venv/` - Virtual environment
- ✗ `*.pyc` - Compiled files
- ✗ `weather_forecast_*.csv` - Generated files

## Update Workflow

For future updates:

```powershell
# Make changes to files

# Stage changes
git add .

# Commit with clear message
git commit -m "Add: New feature description"

# Push to GitHub
git push origin main

# Create release when ready
git tag -a v1.1.0 -m "Version 1.1.0 - New features"
git push origin v1.1.0
```

## Common Commands

```powershell
# Check status
git status

# View recent commits
git log --oneline -5

# Add specific file
git add path/to/file

# Undo changes to file
git restore filename

# Push all changes
git push

# Pull latest from remote
git pull

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Merge branch
git merge feature/new-feature
```

## Troubleshooting

### "fatal: not a git repository"
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/Weather-API-Dashboard.git
git push -u origin main
```

### "Permission denied (publickey)"
- Generate SSH key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- Or use HTTPS instead of SSH

### ".gitignore not working"
```powershell
git rm -r --cached .
git add .
git commit -m "Fix: Apply .gitignore rules"
git push
```

## Success! 🎉

Your project is now on GitHub! Next steps:
1. Share with community
2. Ask for feedback
3. Consider adding CI/CD
4. Start collecting stars ⭐

---

**Repository:** https://github.com/yourusername/Weather-API-Dashboard  
**License:** MIT  
**Status:** Production Ready ✓
