# Use an official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Pillow (libjpeg, zlib)
RUN apt-get update && apt-get install -y libjpeg-dev zlib1g-dev

# Copy project files into the container
COPY . /app

# Copy the fonts directory into the Docker container
COPY fonts /app/fonts

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 8000

# Install gunicorn (if not already in requirements.txt)
RUN pip install gunicorn

# Run the Flask app with gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]