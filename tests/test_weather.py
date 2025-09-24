import json
from pathlib import Path

def test_weather_file_exists():
    p = Path("data/weather.json")
    assert p.exists(), "data/weather.json not found. Run fetch_weather.py"

def test_basic_keys():
    with open("data/weather.json") as f:
        data = json.load(f)
    assert "main" in data, "'main' key missing"
    assert "weather" in data, "'weather' key missing"
    assert "_last_updated_utc" in data, "missing timestamp"
