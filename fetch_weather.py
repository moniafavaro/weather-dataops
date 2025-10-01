import os, json, requests, csv
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
CITY   = os.getenv("CITY", "London")
UNITS  = os.getenv("UNITS", "metric")
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}"

DATA_DIR = "data"
JSON_FILE = os.path.join(DATA_DIR, "weather.json")
LOG_FILE = os.path.join(DATA_DIR, "weather_log.csv")


def log_weather(data):
    # Append temperature data to a CSV log file for visualization
    os.makedirs(DATA_DIR, exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "temperature"])
        writer.writerow([data["_last_updated_utc"], data["main"]["temp"]])


def fetch_weather():
    # Fetch weather data from API, save to JSON, and log to CSV
    if not API_KEY:
        raise RuntimeError("WEATHER_API_KEY environment variable not set")

    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    data = r.json()

    # Add a last_updated timestamp
    data["_last_updated_utc"] = datetime.now(timezone.utc).isoformat()

    # Save JSON snapshot
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)

    # Append to CSV log
    log_weather(data)

    print("Weather fetched and saved.")
    return data


if __name__ == "__main__":
    fetch_weather()