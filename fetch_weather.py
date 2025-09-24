import os, json, requests
from datetime import datetime, timezone

API_KEY = os.getenv("WEATHER_API_KEY")
CITY   = os.getenv("CITY", "London")
UNITS  = os.getenv("UNITS", "metric")
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}"

def fetch_weather():
    if not API_KEY:
        raise RuntimeError("WEATHER_API_KEY environment variable not set")
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    data = r.json()
    # add a last_updated timestamp to help testing/monitoring
    data["_last_updated_utc"] = datetime.now(timezone.utc).isoformat()
    with open("data/weather.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Weather fetched and saved.")
    return data

if __name__ == "__main__":
    fetch_weather()