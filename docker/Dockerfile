# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libhdf5-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Copy the entire project directory to the container
COPY .. .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask application
CMD ["python", "./app.py"]
