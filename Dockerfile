# Use a lightweight Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Install system dependencies including curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Add a non-root user and change ownership of the app directory
RUN useradd -m myuser && chown -R myuser:myuser /usr/src/app
USER myuser

# Expose the port the app runs on
EXPOSE 8080

# Add a health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:8080/ || exit 1

# Run the application
CMD gunicorn --bind 0.0.0.0:8080 app:app & python3 bot.py
