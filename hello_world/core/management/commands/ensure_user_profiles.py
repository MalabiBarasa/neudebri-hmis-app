"""
Management command to ensure all users have UserProfiles
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hello_world.core.models import UserProfile


class Command(BaseCommand):
    help = 'Ensure all users have UserProfiles'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(userprofile__isnull=True)

        if not users_without_profiles.exists():
            self.stdout.write(self.style.SUCCESS('All users already have UserProfiles'))
            return

        created_count = 0
        for user in users_without_profiles:
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'guest',
                    'employee_id': f'EMP{user.id:04d}',
                }
            )
            created_count += 1
            self.stdout.write(f'Created UserProfile for: {user.username}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} UserProfiles')
        )