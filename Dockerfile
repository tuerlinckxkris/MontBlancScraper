FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY monitor_montblanc.py .

# Run the monitor script
CMD ["python", "-u", "monitor_montblanc.py"]
