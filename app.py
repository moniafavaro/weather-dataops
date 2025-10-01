from flask import Flask, render_template, abort, Response
from datetime import datetime
import pandas as pd
import json, os, io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

app = Flask(__name__)

DATA_PATH = os.path.join("data", "weather.json")
LOG_FILE = os.path.join("data", "weather_log.csv")


def load_weather():
    # Load the latest weather snapshot from JSON
    if not os.path.exists(DATA_PATH):
        return None
    
    try:
        with open(DATA_PATH) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None  # File exists but invalid JSON


@app.route("/")
def home():
    # Render latest weather data from JSON snapshot
    weather = load_weather()
    if not weather:
        abort(503, "Weather data not available. Run the fetch job.")

    raw_time = weather.get("_last_updated_utc")
    formatted_time = None
    if raw_time:
        try:
            dt = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
            formatted_time = dt.strftime("%d-%m-%y %H:%M")
        except ValueError:
            formatted_time = raw_time  # fallback if parsing fails

    parsed = {
        "city": weather.get("name", "Unknown"),
        "temperature": weather.get("main", {}).get("temp"),
        "humidity": weather.get("main", {}).get("humidity"),
        "condition": weather.get("weather", [{}])[0].get("description", "").title(),
        "last_updated": formatted_time
    }
    return render_template("index.html", weather=parsed)


@app.route("/plot.png")
def plot_temperature():
    if not os.path.exists(LOG_FILE):
        abort(404, "No weather log yet")

    df = pd.read_csv(LOG_FILE, parse_dates=["timestamp"])

    if df.empty or "temperature" not in df.columns:
        abort(404, "No valid temperature data found")

    plt.figure(figsize=(8, 4))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=10))
    plt.plot(df["timestamp"], df["temperature"], marker="o", color="slateblue", linewidth=2)
    plt.grid(True, linestyle=":", linewidth=0.7, color="lightgray")
    plt.title("Temperature Trend", fontsize=20)
    plt.xlabel("Date (dd-mm-yy)")
    plt.ylabel("Temperature (°C)")
    # plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return Response(img.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)