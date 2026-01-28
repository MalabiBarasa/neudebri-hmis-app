#!/usr/bin/env python3
"""
Ultra-reliable startup script for Render.
Absolutely ensures migrations run before gunicorn starts.
"""
import os
import sys
import time

# Set environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')

print("[STARTUP] Python startup script executing...")
print(f"[STARTUP] Python version: {sys.version}")
print(f"[STARTUP] Working directory: {os.getcwd()}")
print(f"[STARTUP] DATABASE_URL set: {'DATABASE_URL' in os.environ}")

# Step 1: Initialize Django
print("[STARTUP] Initializing Django...")
import django
django.setup()
print("[STARTUP] ✓ Django initialized")

# Step 2: Run migrations
print("[STARTUP] Running migrations...")
from django.core.management import call_command
try:
    call_command('migrate', '--noinput', verbosity=2)
    print("[STARTUP] ✓ Migrations completed")
except Exception as e:
    print(f"[STARTUP] ✗ Migration failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Create initial data
print("[STARTUP] Creating initial data...")
from django.contrib.auth.models import User

admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@neudebri.com',
        'first_name': 'System',
        'last_name': 'Administrator',
        'is_staff': True,
        'is_superuser': True,
    }
)
if created:
    admin_user.set_password('admin1234')
    admin_user.save()
    print("[STARTUP] ✓ Created admin user")
else:
    print("[STARTUP] ⚠ Admin user already exists")

# Step 4: Start gunicorn
print("[STARTUP] ✓ All setup complete - starting gunicorn")
print("[STARTUP] " + "="*70)

port = os.environ.get('PORT', '10000')
os.execvp(sys.executable, [
    sys.executable, '-m', 'gunicorn',
    'hello_world.wsgi:application',
    f'--bind=0.0.0.0:{port}',
    f'--workers={os.cpu_count() or 2}',
    '--worker-class=sync',
    '--timeout=30',
    '--access-logfile=-',
    '--error-logfile=-',
])
