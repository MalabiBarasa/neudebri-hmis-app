"""
Signals for the core app
"""
import logging
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    """
    Create initial users and data after migrations are complete.
    Only runs in production (when DATABASE_URL is set).
    """
    import os

    # Only create initial data in production
    if not os.environ.get('DATABASE_URL'):
        logger.info("Skipping initial data creation - not in production")
        return

    try:
        from django.db import connection
        # Test database connection
        connection.ensure_connection()
        logger.info("Database connection verified")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return

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
            logger.info("⚠ Admin user already exists, skipping creation")

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

        if created_count > 0:
            logger.info(f"✓ Initial data loaded ({created_count} new staff users created)")

    except Exception as e:
        logger.error(f"✗ Failed to create initial data: {str(e)}")
        # Don't raise exception - app should still work without initial data