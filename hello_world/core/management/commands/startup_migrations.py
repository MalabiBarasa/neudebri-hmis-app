"""
Custom management command to run migrations on app startup
This ensures database tables are created before the app runs
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Run migrations on startup (called automatically via WSGI)'

    def handle(self, *args, **options):
        """Run migrations and load initial data"""
        
        # Only run on production (when DATABASE_URL is set)
        if not os.environ.get('DATABASE_URL'):
            self.stdout.write('Skipping - development environment')
            return
        
        self.stdout.write('Running migrations...')
        try:
            call_command('migrate', '--noinput', verbosity=2)
            self.stdout.write(self.style.SUCCESS('✓ Migrations completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Migration error: {str(e)}'))
            raise
        
        # Load initial data
        self.stdout.write('Loading initial data...')
        try:
            from django.contrib.auth.models import User
            from hello_world.core.models import UserProfile
            
            # Create admin user
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
                self.stdout.write(f'✓ Created admin user')
            else:
                self.stdout.write('⚠ Admin user already exists')

            # Create staff users
            staff_data = [
                ('doctor1', 'doctor1@neudebri.com', 'James', 'Kipchoge', 'doctor'),
                ('doctor2', 'doctor2@neudebri.com', 'Mary', 'Wanjiru', 'doctor'),
                ('doctor3', 'doctor3@neudebri.com', 'Peter', 'Mutunga', 'doctor'),
                ('nurse4', 'nurse4@neudebri.com', 'Alice', 'Ochieng', 'nurse'),
                ('nurse5', 'nurse5@neudebri.com', 'Carol', 'Mwangi', 'nurse'),
                ('lab_tech6', 'lab_tech6@neudebri.com', 'David', 'Kiplagat', 'lab_tech'),
                ('pharmacist7', 'pharmacist7@neudebri.com', 'Ruth', 'Kipchoge', 'pharmacist'),
                ('cashier8', 'cashier8@neudebri.com', 'Rose', 'Chepkurui', 'cashier'),
            ]

            for username, email, first_name, last_name, role in staff_data:
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

            self.stdout.write(self.style.SUCCESS('✓ Initial data loaded'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Data loading warning: {str(e)}'))
