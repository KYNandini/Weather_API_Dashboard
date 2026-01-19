# Contributing to Weather API Dashboard

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs
1. Check [GitHub Issues](https://github.com/yourusername/Weather-API-Dashboard/issues) to see if bug already reported
2. If new bug, create issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python version, etc.)

### Suggesting Features
1. Create GitHub Issue with label `enhancement`
2. Describe the feature and why it would be useful
3. Provide example use cases

### Pull Requests
1. **Fork** the repository
2. **Create** a feature branch:
```bash
git checkout -b feature/amazing-feature
```

3. **Make** your changes with clear commits:
```bash
git commit -m "Add: description of changes"
```

4. **Push** to your fork:
```bash
git push origin feature/amazing-feature
```

5. **Open** Pull Request with:
   - Clear title and description
   - Reference to related issues
   - Screenshots/demo if applicable

## Development Setup

1. **Clone your fork:**
```bash
git clone https://github.com/yourusername/Weather-API-Dashboard.git
cd Weather-API-Dashboard
```

2. **Create virtual environment:**
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` for testing:**
```bash
cp .env.example .env
# Add your test API key
```

5. **Run app:**
```bash
python app_production.py
```

## Code Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

Example:
```python
def fetch_weather_data(api_key, city, units='metric'):
    """
    Fetch weather data from OpenWeatherMap API.
    
    Args:
        api_key (str): OpenWeatherMap API key
        city (str): City name
        units (str): 'metric' or 'imperial'
    
    Returns:
        dict: Weather data from API
    """
    # Implementation here
    pass
```

### Commits
- Use clear, descriptive commit messages
- Format: `[Type]: Description`
- Types: Add, Fix, Update, Refactor, Docs, Test

Examples:
```
Add: User authentication system
Fix: Database connection timeout issue
Update: Improved dashboard performance
Refactor: Simplified API integration
Docs: Added API endpoint documentation
Test: Added unit tests for weather filtering
```

### HTML/CSS/JavaScript
- Indent with 4 spaces
- Use semantic HTML
- Keep styles organized
- Comment complex logic

## Testing

Before submitting PR, test:
1. Registration and login
2. Adding manual entries
3. Fetching API data
4. Filtering data
5. Generating dashboard
6. Deleting entries
7. Alert configuration
8. Mobile responsiveness

## Documentation

Update docs for:
- New features (README.md)
- Configuration changes (.env.example)
- Installation steps (INSTALLATION.md)
- API changes (inline comments)

## File Naming Conventions

- **Python files:** `snake_case.py`
- **HTML templates:** `page_name.html`
- **CSS classes:** `kebab-case`
- **JavaScript functions:** `camelCase`

## Areas for Contribution

### High Priority
- [ ] Email alert notifications
- [ ] Scheduled API fetching
- [ ] Performance optimizations
- [ ] Bug fixes

### Medium Priority
- [ ] Dark mode UI
- [ ] Additional weather APIs
- [ ] Data export formats
- [ ] Advanced filtering

### Low Priority
- [ ] UI polish
- [ ] Documentation improvements
- [ ] Code refactoring
- [ ] Test coverage

## Code Review Process

1. **Automated Checks:**
   - Code passes without errors
   - Dependencies are correct
   - `.gitignore` rules followed

2. **Manual Review:**
   - Code quality and style
   - Functionality and tests
   - Documentation completeness

3. **Approval:**
   - At least one approval required
   - All conversations resolved
   - Ready to merge

## Questions?

- Check [Discussions](https://github.com/yourusername/Weather-API-Dashboard/discussions)
- Open an issue with `question` label
- Contact: your.email@example.com

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- No harassment or discrimination
- Assume good intentions

Thank you for contributing! 🙌
