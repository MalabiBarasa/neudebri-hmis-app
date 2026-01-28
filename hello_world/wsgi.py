"""
WSGI config for hello_world project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello_world.settings")

# Setup Django
application = get_wsgi_application()

# Run migrations on app startup (production only)
def run_startup_migrations():
    """Run migrations on first WSGI app load"""
    if not os.environ.get('DATABASE_URL'):
        return  # Skip in development
    
    # Check if migrations have already run
    if hasattr(run_startup_migrations, '_already_ran'):
        return
    
    run_startup_migrations._already_ran = True
    
    logger = logging.getLogger(__name__)
    logger.info("[WSGI] Running startup migrations on app initialization...")
    
    try:
        from django.core.management import call_command
        from django.contrib.auth.models import User
        
        # Run migrations
        call_command('migrate', '--noinput', verbosity=0)
        logger.info("[WSGI] ✓ Migrations completed")
        
        # Create admin user if needed
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
        # Always set admin password on startup to ensure it's correct on Render
        admin_user.set_password('admin1234')
        admin_user.save()
        if created:
            logger.info("[WSGI] ✓ Created admin user")
        else:
            logger.info("[WSGI] ✓ Reset admin password")
        
        # Create UserProfile for admin user if it doesn't exist
        from hello_world.core.models import UserProfile
        admin_profile, profile_created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'role': 'admin',
                'employee_id': 'ADMIN001',
            }
        )
        if profile_created:
            logger.info("[WSGI] ✓ Created admin user profile")
        
        # Set passwords for all staff accounts on startup
        # This ensures Render production always has correct passwords
        staff_passwords = {
            'doctor1': 'doctor1',
            'doctor2': 'doctor2',
            'doctor3': 'doctor3',
            'nurse4': 'nurse4',
            'nurse5': 'nurse5',
            'lab_tech6': 'lab_tech6',
            'pharmacist7': 'pharmacist7',
            'cashier8': 'cashier8',
        }
        
        for username, password in staff_passwords.items():
            try:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                logger.info(f"[WSGI] ✓ Set password for {username}")
            except User.DoesNotExist:
                logger.info(f"[WSGI] User {username} does not exist yet")
        
    except Exception as e:
        logger.error(f"[WSGI] Migration error: {e}", exc_info=True)
        # Don't crash - app can still start

# Run migrations when module loads
try:
    run_startup_migrations()
except Exception as e:
    import traceback
    traceback.print_exc()

