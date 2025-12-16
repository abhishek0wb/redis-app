# Use a Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file (we'll create this next)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the worker script
COPY worker.py .

# Command to run the worker when the container starts
CMD ["python", "worker.py"]