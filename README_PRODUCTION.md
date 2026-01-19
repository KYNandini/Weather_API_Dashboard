# Weather Dashboard - Production Version

A full-featured weather monitoring application with user authentication, real-time data fetching, and advanced analytics.

## Features

### ✅ Core Features
- **User Authentication** - Secure login/registration with password hashing
- **Manual Data Entry** - Add weather data manually for testing or local logging
- **API Integration** - Fetch real live weather from OpenWeatherMap API
- **Data Visualization** - Generate beautiful plots for temperature, humidity, and wind speed trends
- **Data Persistence** - SQLite database stores all data securely
- **CSV Export** - Export data for analysis in Excel or other tools

### ✅ Advanced Features
- **Data Filtering** - Filter by city, date range, or other criteria
- **Weather Alerts** - Configure temperature and humidity thresholds
- **Multi-user Support** - Each user has isolated data
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Production Ready** - Database, authentication, error handling

## Installation

### Prerequisites
- Python 3.8+ installed
- pip package manager

### Quick Setup

1. **Navigate to project directory:**
```powershell
cd C:\Users\[YourUsername]\Desktop\Weather_API_Dashboard
```

2. **Create and activate virtual environment:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

4. **Run the application:**
```powershell
python app_production.py
```

5. **Open in browser:**
```
http://localhost:5000
```

## Usage

### First Time Setup
1. Click "Sign up here" on the login page
2. Create account with username, email, and password
3. Log in with your credentials

### Adding Weather Data

**Option A - Manual Entry:**
1. Go to "Data" tab
2. Fill in date/time, temperature, humidity, wind speed, description, and city
3. Click "Add Entry"

**Option B - API Data (Recommended for real data):**
1. Go to "Data" tab
2. Get API key from https://openweathermap.org/api (free tier available)
3. Enter API key, city name, and unit preference
4. Click "Fetch Data"

### Viewing Dashboard
1. Go to "Dashboard" tab
2. Click "Generate Dashboard"
3. View plots and download CSV

### Configuring Alerts
1. Go to "Alerts" tab
2. Set temperature and humidity thresholds
3. Click "Save Alerts" (future: will send email alerts when thresholds exceeded)

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `password_hash` - Hashed password
- `alert_threshold_temp` - Temperature alert setting
- `alert_threshold_humidity` - Humidity alert setting

### Weather Entries Table
- `id` - Primary key
- `user_id` - Foreign key to user
- `datetime` - Date and time of reading
- `temperature` - Temperature value
- `humidity` - Humidity percentage
- `wind_speed` - Wind speed value
- `description` - Weather description
- `city` - City name
- `source` - Data source (manual/api)
- `created_at` - Entry creation timestamp

## API Endpoints

### Authentication
- `POST /register` - Create new account
- `POST /login` - Log in to account
- `GET /logout` - Log out

### Data Management
- `POST /add_entry` - Add manual weather entry
- `GET /get_entries` - Fetch user's weather entries (supports filters)
- `DELETE /delete_entry/<id>` - Delete specific entry
- `POST /clear_data` - Delete all entries

### Weather Data
- `POST /fetch_api_data` - Fetch from OpenWeatherMap API
- `GET /generate_dashboard` - Generate visualization and CSV

### Alerts
- `POST /set_alerts` - Configure alert thresholds
- `GET /get_alerts` - Get current alert settings

## File Structure

```
Weather_API_Dashboard/
├── app_production.py          # Main application (production version)
├── weather_dashboard.py       # Original CLI version
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .env                       # Environment variables (API keys)
├── .env.example              # Example environment file
├── templates/
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── dashboard.html        # Main dashboard (production)
│   └── index.html            # Original dashboard
├── weather_dashboard.db      # SQLite database (auto-created)
└── weather_forecast_*.csv    # Generated CSV exports
```

## Environment Variables

Create a `.env` file in the project root:

```
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_CITY=Bengaluru
SECRET_KEY=your-secret-key-change-in-production
```

## Production Deployment

### For Real-World Deployment:

1. **Use PostgreSQL instead of SQLite:**
```python
# In app_production.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/weather_db'
```

2. **Use production WSGI server (Gunicorn):**
```powershell
pip install gunicorn
gunicorn -w 4 app_production:app
```

3. **Enable HTTPS/SSL:**
- Use Let's Encrypt for free SSL certificates
- Configure with Nginx reverse proxy

4. **Add rate limiting:**
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: current_user.id)
```

5. **Setup scheduled jobs (APScheduler):**
- Auto-fetch weather every 6 hours
- Send email alerts for threshold breaches
- Cleanup old data

6. **Email alerts (coming soon):**
```python
def send_alert_email(user, alert_message):
    # Configure SMTP and send email
    pass
```

## Troubleshooting

### "Cannot connect to page"
- Ensure app is running: `python app_production.py`
- Check if port 5000 is available
- Try `http://127.0.0.1:5000` instead

### "API Error 401"
- Verify OpenWeatherMap API key is valid
- Check if API key is active (may take a few minutes after creation)
- Ensure key has access to 5-day forecast endpoint

### "Database locked"
- Close all other instances of the app
- Delete `weather_dashboard.db` and restart (will lose data)

### "Login failed"
- Ensure you registered an account first
- Check username/password are correct
- Browser cookies may be blocking - try incognito mode

## Future Enhancements

- [ ] Email notifications for weather alerts
- [ ] Scheduled API fetching every 6 hours
- [ ] Weather trend predictions (ML-based)
- [ ] Mobile app version
- [ ] Integration with weather APIs (AccuWeather, NOAA)
- [ ] Data export to cloud (Google Drive, AWS S3)
- [ ] Dark mode UI theme
- [ ] Multi-language support

## License

Free to use and modify for personal or commercial use.

## Support

For issues or feature requests, refer to documentation or modify source code as needed.

---

**Version:** 2.0 (Production)  
**Last Updated:** January 2026
