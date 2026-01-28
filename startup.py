#!/usr/bin/env python
"""
Professional production startup script for Render deployment.
Handles migrations, data loading, and gunicorn startup.
Pure Python - no bash dependency issues.
"""
import os
import sys
import time
import django
import logging
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def banner(message):
    """Print formatted banner"""
    width = 70
    logger.info("=" * width)
    logger.info(message)
    logger.info("=" * width)

def check_database():
    """Verify database connectivity with retries"""
    from django.db import connection
    from django.db.utils import OperationalError
    
    logger.info("🔍 Checking database connectivity...")
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(1, max_retries + 1):
        try:
            connection.ensure_connection()
            logger.info(f"✓ Database connection successful (attempt {attempt})")
            return True
        except OperationalError as e:
            if attempt < max_retries:
                logger.warning(f"⚠ Connection failed (attempt {attempt}/{max_retries}): {str(e)}")
                logger.info(f"⏳ Waiting {retry_delay}s before retry...")
                time.sleep(retry_delay)
            else:
                logger.error(f"✗ Database connection failed after {max_retries} retries - FATAL")
                return False
    return False

def run_migrations():
    """Execute Django migrations"""
    from django.core.management import call_command
    
    logger.info("▶ Running database migrations...")
    try:
        call_command('migrate', '--noinput', verbosity=2)
        logger.info("✓ Migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Migration failed: {str(e)}")
        logger.exception("Detailed error:")
        return False

def load_initial_data():
    """Create initial users"""
    from django.contrib.auth.models import User
    
    logger.info("▶ Loading initial data...")
    try:
        # Admin user
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
            logger.info("✓ Created admin user (admin/admin1234)")
        else:
            logger.info("⚠ Admin user already exists")

        # Staff users
        staff_data = [
            ('doctor1', 'doctor1@neudebri.com', 'James', 'Kipchoge'),
            ('doctor2', 'doctor2@neudebri.com', 'Mary', 'Wanjiru'),
            ('doctor3', 'doctor3@neudebri.com', 'Peter', 'Mutunga'),
            ('nurse4', 'nurse4@neudebri.com', 'Alice', 'Ochieng'),
            ('nurse5', 'nurse5@neudebri.com', 'Carol', 'Mwangi'),
            ('lab_tech6', 'lab_tech6@neudebri.com', 'David', 'Kiplagat'),
            ('pharmacist7', 'pharmacist7@neudebri.com', 'Ruth', 'Kipchoge'),
            ('cashier8', 'cashier8@neudebri.com', 'Rose', 'Chepkurui'),
        ]

        created_count = 0
        for username, email, first_name, last_name in staff_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_staff': True,
                }
            )
            if created:
                user.set_password(username)
                user.save()
                created_count += 1

        logger.info(f"✓ Initial data loaded ({created_count} new users created)")
        return True
    except Exception as e:
        logger.error(f"✗ Data loading failed: {str(e)}")
        logger.exception("Detailed error:")
        return False

def start_gunicorn():
    """Start gunicorn server"""
    import subprocess
    
    port = os.environ.get('PORT', '10000')
    workers = os.cpu_count() or 2
    
    logger.info("▶ Starting gunicorn WSGI server...")
    logger.info(f"Port: {port}")
    logger.info(f"Workers: {workers}")
    logger.info("=" * 70)
    
    # Build gunicorn command
    cmd = [
        sys.executable, '-m', 'gunicorn',
        'hello_world.wsgi:application',
        f'--bind=0.0.0.0:{port}',
        f'--workers={workers}',
        '--worker-class=sync',
        '--max-requests=1000',
        '--max-requests-jitter=100',
        '--timeout=30',
        '--access-logfile=-',
        '--error-logfile=-',
        '--log-level=info',
    ]
    
    # exec into gunicorn (replaces this process)
    os.execvp(cmd[0], cmd)

def main():
    """Main startup sequence"""
    banner("DJANGO HMIS STARTUP SEQUENCE")
    
    is_production = os.environ.get('DATABASE_URL') is not None
    logger.info(f"Environment: {'PRODUCTION' if is_production else 'DEVELOPMENT'}")
    logger.info(f"Debug: {os.environ.get('DEBUG', 'FALSE')}")
    
    if not is_production:
        logger.info("⊘ Skipping migrations - development environment detected")
        start_gunicorn()
        return
    
    # Step 1: Check database
    if not check_database():
        logger.error("✗ FATAL: Cannot connect to database")
        sys.exit(1)
    
    # Step 2: Run migrations
    if not run_migrations():
        logger.error("✗ FATAL: Migrations failed")
        sys.exit(1)
    
    # Step 3: Load initial data (non-critical)
    load_initial_data()
    
    banner("✓ STARTUP COMPLETE - Starting server")
    
    # Step 4: Start gunicorn
    start_gunicorn()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        logger.exception("Detailed traceback:")
        sys.exit(1)
