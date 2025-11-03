# base image
FROM python:3.11-slim

WORKDIR /app

# Install OS deps for mysql connector (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["python", "app.py"]
