"""
Management command to ensure all users have UserProfiles with correct roles
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hello_world.core.models import UserProfile


class Command(BaseCommand):
    help = 'Ensure all users have UserProfiles with correct roles'

    def handle(self, *args, **options):
        # Role mapping based on username patterns
        role_mapping = {
            'admin': 'super_admin',
            'doctor1': 'doctor',
            'doctor2': 'doctor',
            'doctor3': 'doctor',
            'nurse4': 'nurse',
            'nurse5': 'nurse',
            'lab_tech6': 'lab_tech',
            'pharmacist7': 'pharmacist',
            'cashier8': 'cashier',
        }

        users = User.objects.all()
        updated_count = 0
        created_count = 0

        for user in users:
            if user.username in role_mapping:
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': role_mapping[user.username],
                        'employee_id': f"{user.username.upper()}_ID",
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created profile for {user.username} with role {profile.role}')
                    )
                elif profile.role != role_mapping[user.username]:
                    old_role = profile.role
                    profile.role = role_mapping[user.username]
                    profile.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated {user.username}: {old_role} -> {profile.role}')
                    )
                else:
                    self.stdout.write(
                        f'Profile for {user.username} already correct (role: {profile.role})'
                    )

        # Handle any users not in the mapping (set to guest role)
        for user in users:
            if user.username not in role_mapping and user.username != 'AnonymousUser':
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': 'guest',
                        'employee_id': f"{user.username.upper()}_ID",
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created guest profile for {user.username}')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'Completed: {created_count} profiles created, {updated_count} profiles updated'
            )
        )