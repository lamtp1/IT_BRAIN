# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files to the container
COPY . /app

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5200

# Set environment variables
ENV FLASK_APP=chatgpt_backup.py
ENV FLASK_RUN_HOST=0.0.0.0

# Start the Flask application
CMD ["python", "chatgpt_backup.py"]