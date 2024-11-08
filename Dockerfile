# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# # Copy requirements file to the container
# COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install flask flask_sqlalchemy

# Copy application code to the container
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
