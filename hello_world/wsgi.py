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
        
        # Create and set passwords for all staff accounts on startup
        # This ensures Render production always has all users with correct passwords
        staff_data = {
            'doctor1': {'password': 'doctor1', 'role': 'doctor', 'email': 'doctor1@neudebri.com'},
            'doctor2': {'password': 'doctor2', 'role': 'doctor', 'email': 'doctor2@neudebri.com'},
            'doctor3': {'password': 'doctor3', 'role': 'doctor', 'email': 'doctor3@neudebri.com'},
            'nurse4': {'password': 'nurse4', 'role': 'nurse', 'email': 'nurse4@neudebri.com'},
            'nurse5': {'password': 'nurse5', 'role': 'nurse', 'email': 'nurse5@neudebri.com'},
            'lab_tech6': {'password': 'lab_tech6', 'role': 'laboratory_technician', 'email': 'lab_tech6@neudebri.com'},
            'pharmacist7': {'password': 'pharmacist7', 'role': 'pharmacist', 'email': 'pharmacist7@neudebri.com'},
            'cashier8': {'password': 'cashier8', 'role': 'cashier', 'email': 'cashier8@neudebri.com'},
        }
        
        for username, info in staff_data.items():
            # Create or get the user
            staff_user, staff_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': info['email'],
                    'first_name': username,
                    'last_name': 'Staff',
                    'is_staff': True,
                }
            )
            # Always set the password on startup
            staff_user.set_password(info['password'])
            staff_user.save()
            
            if staff_created:
                logger.info(f"[WSGI] ✓ Created staff user {username}")
            else:
                logger.info(f"[WSGI] ✓ Reset password for {username}")
            
            # Create UserProfile for staff user if needed
            staff_profile, profile_created = UserProfile.objects.get_or_create(
                user=staff_user,
                defaults={
                    'role': info['role'],
                    'employee_id': f"{username.upper()}001",
                }
            )
            if profile_created:
                logger.info(f"[WSGI] ✓ Created profile for {username}")
        
    except Exception as e:
        logger.error(f"[WSGI] Migration error: {e}", exc_info=True)
        # Don't crash - app can still start

# Run migrations when module loads
try:
    run_startup_migrations()
except Exception as e:
    import traceback
    traceback.print_exc()

