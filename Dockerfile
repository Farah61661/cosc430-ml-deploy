# Use a slim Python 3.11 base image to keep the image small and secure
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first so Docker can cache this layer
# (if requirements don't change, this layer won't be rebuilt)
COPY requirements.txt .

# Install dependencies without caching to avoid bloating the image layer
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app
COPY app.py .

# Copy the trained model - needed by app.py at startup (joblib.load)
COPY model.pkl .

# Tell the container which port to listen on
ENV PORT=8080
EXPOSE 8080

# Start the app with Gunicorn (production WSGI server)
# 2 workers handle concurrent requests safely
# Flask's built-in dev server (app.run) is NOT safe for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
