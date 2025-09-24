# A Flask web app that shows current weather for a city.

A scheduled CI job (GitHub Actions) runs every 2 hours to fetch fresh weather data from a Weather API and commit/update the repository (or push to storage/deploy), while CI tests ensure data integrity. App reads a local JSON file data/weather.json and renders it with Jinja.

## Tools

- **Flask + Jinja** — quick, lightweight web app and templating for display
- **requests** — fetch data from the Weather API
- **pytest** — automated tests for CI to validate the fetched data
- **Git & GitHub** — version control and repo hosting
- **GitHub Actions** — CI/CD and schedule (cron) for the 2-hour updates
- **Docker** — reproducible runtime and easy deployment
- **GitHub Secrets** — safely store API keys (never commit keys)