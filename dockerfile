# Use a slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (e.g., for cron/timezone and SSL)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libssl-dev \
    libpq-dev \
    cython3 \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]