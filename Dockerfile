# Chooses the base image for your container
FROM python:3.10-slim
# Python 3.10 in a lightweight "slim" Linux environment, this avoids installing Python manually and keeps the image small

# Sets the working directory inside the container, equivalent to running cd /app
WORKDIR /app

# Copies only your requirements.txt file into the container
COPY requirements.txt .
# This allows Docker to install dependencies first, and then reuse its cache unless requirements.txt changes

# Installs your Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# --no-cache-dir avoids caching pip packages → keeps the image smaller

# Copies the rest of your project files into the container (Flask app, templates, static files, etc.)
COPY . .
# At this point, everything you need to run the app exists in /app

# Sets an environment variable inside the container
# Tells Flask which file contains your app instance (app.py)
ENV FLASK_APP=app.py

# Documents that your app runs on port 5000 inside the container
EXPOSE 5000
# Doesn’t automatically open the port — you need docker run -p 5000:5000 to expose it to your machine

# Defines the default command to run when the container starts
# Launches your Flask app, binding it to all interfaces (0.0.0.0) so it’s reachable outside the container
# Runs on port 5000, matching the EXPOSE step
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


# FROM … = choose base environment
# WORKDIR … = set workspace
# COPY … = bring files in
# RUN … = install dependencies
# ENV … = configure settings
# EXPOSE … = declare networking
# CMD … = start the app