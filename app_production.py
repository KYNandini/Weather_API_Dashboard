from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
import os
import requests
import logging
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import func

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create instance folder
import os as os_module
instance_path = os_module.path.join(os_module.path.dirname(__file__), 'instance')
os_module.makedirs(instance_path, exist_ok=True)

app = Flask(__name__)
# Use absolute path for database
db_path = os_module.path.join(instance_path, 'weather_dashboard.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path.replace(chr(92), "/")}'
app.config['SECRET_KEY'] = os_module.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['ENV'] = 'production'

db = SQLAlchemy(app)

# Global user for shared data (no authentication)
DEFAULT_USER_ID = 1

# ==================== DATABASE MODELS ====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), default='Guest', nullable=False)
    email = db.Column(db.String(120), default='guest@example.com', nullable=False)
    weather_entries = db.relationship('WeatherEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    alert_threshold_temp = db.Column(db.Float, default=None)
    alert_threshold_humidity = db.Column(db.Float, default=None)
    created_at = db.Column(db.DateTime, server_default=func.now())

class WeatherEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    city = db.Column(db.String(100))
    source = db.Column(db.String(50), default='manual')  # 'manual' or 'api'
    created_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'DateTime': self.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'Temperature': self.temperature,
            'Humidity': self.humidity,
            'WindSpeed': self.wind_speed,
            'Description': self.description,
            'City': self.city,
            'Source': self.source
        }

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Open dashboard directly without login"""
    logger.info('Loading dashboard')
    return render_template('dashboard.html')

@app.route('/add_entry', methods=['POST'])
def add_entry():
    try:
        data = request.json
        entry = WeatherEntry(
            user_id=DEFAULT_USER_ID,
            datetime=datetime.fromisoformat(data.get('datetime')),
            temperature=float(data.get('temperature', 0)),
            humidity=float(data.get('humidity', 0)),
            wind_speed=float(data.get('windspeed', 0)),
            description=data.get('description', ''),
            city=data.get('city', 'Manual Entry'),
            source='manual'
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Entry added'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_entries', methods=['GET'])
def get_entries():
    try:
        city_filter = request.args.get('city', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        query = WeatherEntry.query.filter_by(user_id=DEFAULT_USER_ID)
        
        if city_filter:
            query = query.filter_by(city=city_filter)
        if date_from:
            query = query.filter(WeatherEntry.datetime >= datetime.fromisoformat(date_from))
        if date_to:
            query = query.filter(WeatherEntry.datetime <= datetime.fromisoformat(date_to))
        
        entries = query.order_by(WeatherEntry.datetime.desc()).all()
        return jsonify([entry.to_dict() for entry in entries])
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/delete_entry/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    try:
        entry = WeatherEntry.query.get(entry_id)
        if not entry or entry.user_id != DEFAULT_USER_ID:
            return jsonify({'status': 'error', 'message': 'Entry not found'})
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Entry deleted'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/fetch_api_data', methods=['POST'])
def fetch_api_data():
    try:
        data = request.json
        api_key = data.get('api_key')
        city = data.get('city', 'Bengaluru')
        units = data.get('units', 'metric')
        
        if not api_key:
            return jsonify({'status': 'error', 'message': 'API key not provided'})
        
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
        response = requests.get(url)
        
        if response.status_code != 200:
            error_data = response.json()
            return jsonify({'status': 'error', 'message': f"API Error: {error_data.get('message', 'Unknown error')}"})
        
        api_data = response.json()
        forecast_list = api_data.get('list', [])
        
        for item in forecast_list:
            entry = WeatherEntry(
                user_id=DEFAULT_USER_ID,
                datetime=datetime.fromtimestamp(item['dt']),
                temperature=item['main']['temp'],
                humidity=item['main']['humidity'],
                wind_speed=item['wind']['speed'],
                description=item['weather'][0]['description'],
                city=city,
                source='api'
            )
            db.session.add(entry)
        
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'Loaded {len(forecast_list)} entries from API for {city}',
            'entries_count': len(forecast_list)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/generate_dashboard', methods=['GET'])
def generate_dashboard():
    try:
        entries = WeatherEntry.query.filter_by(user_id=DEFAULT_USER_ID).all()
        
        if not entries:
            return jsonify({'status': 'error', 'message': 'No data to visualize'})
        
        data = [entry.to_dict() for entry in entries]
        df = pd.DataFrame(data)
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df = df.sort_values('DateTime')
        
        plt.figure(figsize=(14, 10))
        
        plt.subplot(3, 1, 1)
        plt.plot(df['DateTime'], df['Temperature'], marker='o', color='red', linewidth=2)
        plt.title('Temperature Forecast Trend', fontsize=14, fontweight='bold')
        plt.ylabel('Temperature (°C)')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3, 1, 2)
        plt.plot(df['DateTime'], df['Humidity'], marker='o', color='blue', linewidth=2)
        plt.title('Humidity Forecast Trend', fontsize=14, fontweight='bold')
        plt.ylabel('Humidity (%)')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3, 1, 3)
        plt.plot(df['DateTime'], df['WindSpeed'], marker='o', color='green', linewidth=2)
        plt.title('Wind Speed Forecast Trend', fontsize=14, fontweight='bold')
        plt.ylabel('Wind Speed (m/s)')
        plt.xlabel('Date & Time')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        csv_filename = f'weather_forecast_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(csv_filename, index=False)
        
        return jsonify({
            'status': 'success',
            'image': plot_url,
            'csv_saved': csv_filename
        })
    except Exception as e:
        logger.error(f'Error generating dashboard: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/clear_data', methods=['POST'])
def clear_data():
    try:
        WeatherEntry.query.filter_by(user_id=DEFAULT_USER_ID).delete()
        db.session.commit()
        logger.info('All data cleared')
        return jsonify({'status': 'success', 'message': 'All data cleared'})
    except Exception as e:
        logger.error(f'Error clearing data: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_cities', methods=['GET'])
def get_cities():
    try:
        cities = db.session.query(WeatherEntry.city).filter_by(user_id=DEFAULT_USER_ID).distinct().all()
        return jsonify([city[0] for city in cities if city[0]])
    except Exception as e:
        logger.error(f'Error getting cities: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/set_alerts', methods=['POST'])
def set_alerts():
    try:
        data = request.json
        user = User.query.get(DEFAULT_USER_ID)
        if user:
            user.alert_threshold_temp = data.get('temp_threshold')
            user.alert_threshold_humidity = data.get('humidity_threshold')
            db.session.commit()
            logger.info('Alerts configured')
        return jsonify({'status': 'success', 'message': 'Alerts configured'})
    except Exception as e:
        logger.error(f'Error setting alerts: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_alerts', methods=['GET'])
def get_alerts():
    try:
        user = User.query.get(DEFAULT_USER_ID)
        if user:
            return jsonify({
                'temp_threshold': user.alert_threshold_temp,
                'humidity_threshold': user.alert_threshold_humidity
            })
        return jsonify({'temp_threshold': None, 'humidity_threshold': None})
    except Exception as e:
        logger.error(f'Error getting alerts: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)})

# ==================== BACKGROUND SCHEDULER ====================

def scheduled_api_fetch():
    """Fetch weather data for all users periodically"""
    pass  # Implement as needed

scheduler = BackgroundScheduler()
# scheduler.add_job(scheduled_api_fetch, 'interval', hours=6)
# scheduler.start()

# ==================== DATABASE INITIALIZATION ====================

def init_db():
    """Initialize database safely"""
    import os
    try:
        # Create instance folder if it doesn't exist
        instance_path = os.path.join(os.path.dirname(__file__), 'instance')
        os.makedirs(instance_path, exist_ok=True)
        
        with app.app_context():
            db.create_all()
            # Create default user if it doesn't exist
            if not User.query.get(DEFAULT_USER_ID):
                default_user = User(id=DEFAULT_USER_ID, username='Guest', email='guest@example.com')
                db.session.add(default_user)
                db.session.commit()
                logger.info(f'Created default user with ID {DEFAULT_USER_ID}')
    except Exception as e:
        logger.error(f'Database initialization error: {e}')

if __name__ == '__main__':
    init_db()
    logger.info('Starting Weather Dashboard (No Authentication Mode)')
    logger.info('Open http://localhost:5000 in your browser')
    try:
        app.run(debug=False, port=5000, use_reloader=False)
    except Exception as e:
        logger.error(f'Failed to start app: {e}')
