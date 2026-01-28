#!/bin/bash
# Professional startup script for Render deployment
# Orchestrates database migrations, data loading, and app startup

set -e  # Exit on any error

echo "=================================================================="
echo "🚀 DJANGO HMIS RENDER STARTUP SCRIPT"
echo "=================================================================="
echo "Time: $(date)"
echo "Environment: $RENDER_GIT_BRANCH (Render Service ID: $RENDER_SERVICE_ID)"
echo "=================================================================="

# Run startup migrations with full output
echo ""
echo "▶ Step 1: Running migrations and data initialization..."
python manage.py startup_migrations

if [ $? -ne 0 ]; then
    echo "✗ FATAL: Startup migrations failed!"
    exit 1
fi

echo ""
echo "✓ Migrations and initialization complete"
echo ""
echo "▶ Step 2: Starting gunicorn WSGI server..."
echo "Port: $PORT"
echo "Workers: $(nproc)"
echo ""
echo "=================================================================="

# Start gunicorn with proper signal handling
exec gunicorn \
    hello_world.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers $(nproc) \
    --worker-class sync \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
