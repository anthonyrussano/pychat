# Use Python 3.12 slim image as the base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir flask flask-socketio

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
