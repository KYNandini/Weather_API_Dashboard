import os
import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# ----------------------------
# CONFIGURATION
# ----------------------------
# Read API key from environment variable `OPENWEATHER_API_KEY` when available.
# Fallback to the placeholder so existing behavior still works if edited manually.
API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")  # replace with your OpenWeatherMap API key
CITY = os.getenv("OPENWEATHER_CITY", "Bengaluru")  # can override by env var
UNITS = os.getenv("OPENWEATHER_UNITS", "metric")  # metric = Celsius, imperial = Fahrenheit

# OpenWeatherMap 5 day / 3 hour forecast API
URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units={UNITS}"

# ----------------------------
# FETCH DATA FROM API
# ----------------------------
if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
    print("Error: OpenWeatherMap API key not set.")
    print("Set the `OPENWEATHER_API_KEY` environment variable or edit `weather_dashboard.py` to add your key.")
    print("Example (PowerShell): $env:OPENWEATHER_API_KEY = 'your_key_here'")
    sys.exit(1)

response = requests.get(URL)

if response.status_code != 200:
    print("Error fetching data from API!")
    print("Status Code:", response.status_code)
    print("Message:", response.text)
    sys.exit(1)

data = response.json()

# ----------------------------
# EXTRACT REQUIRED DATA
# ----------------------------
forecast_list = data["list"]

weather_data = []

for item in forecast_list:
    dt_txt = item["dt_txt"]
    temp = item["main"]["temp"]
    humidity = item["main"]["humidity"]
    wind_speed = item["wind"]["speed"]
    weather_desc = item["weather"][0]["description"]

    weather_data.append([dt_txt, temp, humidity, wind_speed, weather_desc])

# Convert to DataFrame
df = pd.DataFrame(weather_data, columns=["DateTime", "Temperature", "Humidity", "WindSpeed", "Description"])

# Convert DateTime to actual datetime format
df["DateTime"] = pd.to_datetime(df["DateTime"])

print("\nFetched Weather Data (Sample):")
print(df.head())

# ----------------------------
# VISUALIZATION DASHBOARD
# ----------------------------
plt.figure(figsize=(14, 10))

# 1) Temperature Trend
plt.subplot(3, 1, 1)
plt.plot(df["DateTime"], df["Temperature"], marker="o")
plt.title(f"Temperature Forecast Trend - {CITY}")
plt.ylabel("Temperature (°C)")
plt.grid(True)

# 2) Humidity Trend
plt.subplot(3, 1, 2)
plt.plot(df["DateTime"], df["Humidity"], marker="o")
plt.title(f"Humidity Forecast Trend - {CITY}")
plt.ylabel("Humidity (%)")
plt.grid(True)

# 3) Wind Speed Trend
plt.subplot(3, 1, 3)
plt.plot(df["DateTime"], df["WindSpeed"], marker="o")
plt.title(f"Wind Speed Forecast Trend - {CITY}")
plt.ylabel("Wind Speed (m/s)")
plt.xlabel("Date & Time")
plt.grid(True)

plt.tight_layout()
plt.show()

# ----------------------------
# SAVE DASHBOARD OUTPUT
# ----------------------------
df.to_csv("weather_forecast_data.csv", index=False)
print("\nDashboard displayed successfully!")
print("Data saved as: weather_forecast_data.csv")
