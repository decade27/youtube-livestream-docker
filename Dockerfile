# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Create directories for app and media files
RUN mkdir -p /app/audio /app/video

# Set the working directory to /app
WORKDIR /app

# Copy the application files
COPY app/ /app/

# Ensure that Python won't write pyc files / use buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install any needed packages specified in requirements.txt
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables for dynamic configuration
ENV YOUTUBE_KEY=YOUR_YOUTUBE_STREAM_KEY  
# Example; usually set at runtime

# Run the application
CMD ["python", "stream.py"]