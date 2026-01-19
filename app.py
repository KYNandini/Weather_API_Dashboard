from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid threading issues
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['ENV'] = 'production'  # Disable debug/auto-reload

# Store weather data in memory
weather_data = []
API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
CITY = os.getenv('OPENWEATHER_CITY', 'Bengaluru')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_entry', methods=['POST'])
def add_entry():
    """Add a manual weather entry"""
    try:
        data = request.json
        entry = {
            'DateTime': data.get('datetime'),
            'Temperature': float(data.get('temperature', 0)),
            'Humidity': float(data.get('humidity', 0)),
            'WindSpeed': float(data.get('windspeed', 0)),
            'Description': data.get('description', '')
        }
        weather_data.append(entry)
        return jsonify({'status': 'success', 'message': 'Entry added'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_entries', methods=['GET'])
def get_entries():
    """Get all weather entries"""
    return jsonify(weather_data)

@app.route('/delete_entry/<int:index>', methods=['DELETE'])
def delete_entry(index):
    """Delete a weather entry by index"""
    try:
        if 0 <= index < len(weather_data):
            weather_data.pop(index)
            return jsonify({'status': 'success', 'message': 'Entry deleted'})
        return jsonify({'status': 'error', 'message': 'Invalid index'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/generate_dashboard', methods=['GET'])
def generate_dashboard():
    """Generate and return the dashboard visualization"""
    try:
        if not weather_data:
            return jsonify({'status': 'error', 'message': 'No data to visualize'})
        
        df = pd.DataFrame(weather_data)
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df = df.sort_values('DateTime')
        
        plt.figure(figsize=(14, 10))
        
        # Temperature Trend
        plt.subplot(3, 1, 1)
        plt.plot(df['DateTime'], df['Temperature'], marker='o', color='red')
        plt.title('Temperature Forecast Trend')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        
        # Humidity Trend
        plt.subplot(3, 1, 2)
        plt.plot(df['DateTime'], df['Humidity'], marker='o', color='blue')
        plt.title('Humidity Forecast Trend')
        plt.ylabel('Humidity (%)')
        plt.grid(True)
        
        # Wind Speed Trend
        plt.subplot(3, 1, 3)
        plt.plot(df['DateTime'], df['WindSpeed'], marker='o', color='green')
        plt.title('Wind Speed Forecast Trend')
        plt.ylabel('Wind Speed (m/s)')
        plt.xlabel('Date & Time')
        plt.grid(True)
        
        plt.tight_layout()
        
        # Convert plot to base64 image
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        # Save CSV
        df.to_csv('weather_forecast_data.csv', index=False)
        
        return jsonify({
            'status': 'success',
            'image': plot_url,
            'csv_saved': 'weather_forecast_data.csv'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/clear_data', methods=['POST'])
def clear_data():
    """Clear all weather data"""
    global weather_data
    weather_data = []
    return jsonify({'status': 'success', 'message': 'All data cleared'})

@app.route('/fetch_api_data', methods=['POST'])
def fetch_api_data():
    """Fetch weather data from OpenWeatherMap API"""
    try:
        data = request.json
        api_key = data.get('api_key', API_KEY)
        city = data.get('city', CITY)
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
        
        # Clear previous data and load API data
        global weather_data
        weather_data = []
        
        for item in forecast_list:
            entry = {
                'DateTime': item['dt_txt'],
                'Temperature': item['main']['temp'],
                'Humidity': item['main']['humidity'],
                'WindSpeed': item['wind']['speed'],
                'Description': item['weather'][0]['description']
            }
            weather_data.append(entry)
        
        return jsonify({
            'status': 'success',
            'message': f'Loaded {len(weather_data)} entries from API for {city}',
            'entries_count': len(weather_data)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_config', methods=['GET'])
def get_config():
    """Get current API configuration"""
    return jsonify({
        'api_key_set': bool(API_KEY),
        'city': CITY
    })

if __name__ == '__main__':
    app.run(debug=False, port=5000, use_reloader=False)
