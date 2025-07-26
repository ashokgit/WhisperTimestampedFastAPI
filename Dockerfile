# Multi-stage build for whisper-timestamped microservice
FROM python:3.10-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install whisper-timestamped
RUN pip install --no-cache-dir git+https://github.com/linto-ai/whisper-timestamped.git

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 whisper && chown -R whisper:whisper /app
USER whisper

# Expose port
EXPOSE 8000

CMD ["python", "app.py"]