# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements from project root (one level up)
COPY ../requirements-api.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-api.txt

# Copy the rest of the application (from project root)
COPY ../api ./api
COPY ../models ./models
COPY ../data ./data

# Expose port
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]