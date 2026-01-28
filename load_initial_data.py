"""
Script to load initial HMIS data (users, departments, etc.)
Run after migrations: python manage.py loaddata initial_data.json
Or use: python manage.py shell < load_data.py
"""

from django.contrib.auth.models import User
from hello_world.core.models import Department, UserProfile

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
    print(f"✅ Created admin user: {admin_user.username}")
else:
    print(f"⚠️  Admin user already exists: {admin_user.username}")

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
        print(f"✅ Created user: {username}")
    else:
        print(f"⚠️  User already exists: {username}")

print("\n✅ All users loaded successfully!")
