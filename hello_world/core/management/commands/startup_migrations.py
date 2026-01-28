"""
Professional startup migrations command with comprehensive error handling.
Runs migrations and initializes data on app startup for production deployments.
"""
import os
import sys
import time
import logging
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection, connections
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run migrations and initialize data on app startup (production only)'

    def log(self, message, level='info'):
        """Log message with timestamp"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        full_msg = f"[{timestamp}] {message}"
        getattr(logger, level)(full_msg)
        self.stdout.write(full_msg)

    def check_database_connection(self, max_retries=5, retry_delay=2):
        """
        Check if database is accessible with retry logic.
        Production databases may take a moment to be ready.
        """
        self.log("🔍 Checking database connectivity...")
        
        for attempt in range(1, max_retries + 1):
            try:
                # Test the connection
                connection.ensure_connection()
                self.log(f"✓ Database connection successful (attempt {attempt})")
                return True
            except OperationalError as e:
                self.log(f"⚠ Database connection failed (attempt {attempt}/{max_retries}): {str(e)}", 'warning')
                if attempt < max_retries:
                    self.log(f"⏳ Waiting {retry_delay}s before retry...")
                    time.sleep(retry_delay)
                else:
                    self.log("✗ Database connection failed after all retries - CRITICAL", 'error')
                    return False
        return False

    def run_migrations(self):
        """Run Django migrations"""
        self.log("▶ Running database migrations...")
        try:
            call_command('migrate', '--noinput', verbosity=2)
            self.log("✓ Migrations completed successfully")
            return True
        except Exception as e:
            self.log(f"✗ Migration failed: {str(e)}", 'error')
            logger.exception("Detailed migration error:")
            return False

    def load_initial_data(self):
        """Create initial users and data"""
        self.log("▶ Loading initial data...")
        try:
            from django.contrib.auth.models import User
            
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
                self.log("✓ Created admin user (admin/admin1234)")
            else:
                self.log("⚠ Admin user already exists, skipping creation")

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

            self.log(f"✓ Initial data loaded ({created_count} new staff users created)")
            return True
        except Exception as e:
            self.log(f"✗ Data loading failed: {str(e)}", 'error')
            logger.exception("Detailed data loading error:")
            # Don't fail completely - app can still run without this data
            return False

    def handle(self, *args, **options):
        """Main startup handler"""
        is_production = os.environ.get('DATABASE_URL') is not None
        
        self.log("=" * 70)
        self.log("DJANGO HMIS STARTUP MIGRATIONS")
        self.log(f"Environment: {'PRODUCTION' if is_production else 'DEVELOPMENT'}")
        self.log(f"Debug Mode: {os.environ.get('DEBUG', 'FALSE')}")
        self.log("=" * 70)
        
        if not is_production:
            self.log("⊘ Skipping - development environment detected")
            return

        # Step 1: Check database connectivity
        if not self.check_database_connection():
            self.log("✗ FATAL: Cannot connect to database - aborting startup", 'error')
            sys.exit(1)

        # Step 2: Run migrations
        if not self.run_migrations():
            self.log("✗ FATAL: Migrations failed - aborting startup", 'error')
            sys.exit(1)

        # Step 3: Load initial data
        self.load_initial_data()

        self.log("=" * 70)
        self.log("✓ STARTUP COMPLETE - App ready to serve requests")
        self.log("=" * 70)
