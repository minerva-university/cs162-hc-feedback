# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install logging

# Expose the port your app runs on
EXPOSE 8080

# Command to run your application
CMD ["python", "run.py"]
