from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
import os
import requests
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import func

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_dashboard.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['ENV'] = 'production'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    weather_entries = db.relationship('WeatherEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    alert_threshold_temp = db.Column(db.Float, default=None)
    alert_threshold_humidity = db.Column(db.Float, default=None)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        
        if User.query.filter_by(username=username).first():
            return jsonify({'status': 'error', 'message': 'Username already exists'})
        if User.query.filter_by(email=email).first():
            return jsonify({'status': 'error', 'message': 'Email already exists'})
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return jsonify({'status': 'success', 'message': 'Registration successful'})
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'status': 'success', 'message': 'Login successful'})
        return jsonify({'status': 'error', 'message': 'Invalid username or password'})
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ==================== DASHBOARD ROUTES ====================

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/add_entry', methods=['POST'])
@login_required
def add_entry():
    try:
        data = request.json
        entry = WeatherEntry(
            user_id=current_user.id,
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
@login_required
def get_entries():
    try:
        city_filter = request.args.get('city', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        query = WeatherEntry.query.filter_by(user_id=current_user.id)
        
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
@login_required
def delete_entry(entry_id):
    try:
        entry = WeatherEntry.query.get(entry_id)
        if not entry or entry.user_id != current_user.id:
            return jsonify({'status': 'error', 'message': 'Entry not found'})
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Entry deleted'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/fetch_api_data', methods=['POST'])
@login_required
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
                user_id=current_user.id,
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
@login_required
def generate_dashboard():
    try:
        entries = WeatherEntry.query.filter_by(user_id=current_user.id).all()
        
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
        
        csv_filename = f'weather_forecast_{current_user.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(csv_filename, index=False)
        
        return jsonify({
            'status': 'success',
            'image': plot_url,
            'csv_saved': csv_filename
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/clear_data', methods=['POST'])
@login_required
def clear_data():
    try:
        WeatherEntry.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'All data cleared'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_cities', methods=['GET'])
@login_required
def get_cities():
    cities = db.session.query(WeatherEntry.city).filter_by(user_id=current_user.id).distinct().all()
    return jsonify([city[0] for city in cities if city[0]])

@app.route('/set_alerts', methods=['POST'])
@login_required
def set_alerts():
    try:
        data = request.json
        current_user.alert_threshold_temp = data.get('temp_threshold')
        current_user.alert_threshold_humidity = data.get('humidity_threshold')
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Alerts configured'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_alerts', methods=['GET'])
@login_required
def get_alerts():
    return jsonify({
        'temp_threshold': current_user.alert_threshold_temp,
        'humidity_threshold': current_user.alert_threshold_humidity
    })

# ==================== BACKGROUND SCHEDULER ====================

def scheduled_api_fetch():
    """Fetch weather data for all users periodically"""
    pass  # Implement as needed

scheduler = BackgroundScheduler()
# scheduler.add_job(scheduled_api_fetch, 'interval', hours=6)
# scheduler.start()

# ==================== DATABASE INITIALIZATION ====================

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False, port=5000, use_reloader=False)
