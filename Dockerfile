# syntax=docker/dockerfile:1

FROM python:3.11-slim

LABEL maintainer="Antigravity"
LABEL description="Docker image for Garmin Sleep Stats Streamlit App"

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (if needed, e.g., for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a volume for data persistence (JSON files, cache)
VOLUME ["/app/data"]

# Streamlit uses 8501 by default
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
