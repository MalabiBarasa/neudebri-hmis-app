FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn whitenoise

# Copy project
COPY . .

# Create static directory
RUN mkdir -p staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Run migrations and start server
CMD ["gunicorn", "hello_world.wsgi:application", "--bind", "0.0.0.0:8000"]
