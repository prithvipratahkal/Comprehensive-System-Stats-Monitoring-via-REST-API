FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY restapi.py .
COPY system_stats.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9090

CMD ["python3", "restapi.py"]
