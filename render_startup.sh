#!/bin/bash
# Startup script for Render - runs migrations and loads data before starting gunicorn

echo "🚀 Starting Django HMIS application..."
echo "Running startup migrations and data loading..."

python manage.py startup_migrations

echo "✓ Startup complete - starting gunicorn..."
exec gunicorn hello_world.wsgi:application --bind 0.0.0.0:$PORT
