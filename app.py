from flask import Flask, render_template, abort
import json
import os

app = Flask(__name__)

DATA_PATH = os.path.join("data", "weather.json")

def load_weather():
    try:
        with open(DATA_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@app.route("/")
def home():
    weather = load_weather()
    if not weather:
        abort(503, "Weather data not available. Run the fetch job.")
    parsed = {
        "city": weather.get("name", "Unknown"),
        "temperature": weather.get("main", {}).get("temp"),
        "humidity": weather.get("main", {}).get("humidity"),
        "condition": weather.get("weather", [{}])[0].get("description", "").title(),
        "last_updated": weather.get("_last_updated_utc")
    }
    return render_template("index.html", weather=parsed)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
