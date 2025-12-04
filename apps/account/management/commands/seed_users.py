from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
import random

class Command(BaseCommand):
    help = 'Seeds the database with a superuser and multiple normal users.'

    def add_arguments(self, parser):
        # Optional argument for number of normal users (default 5)
        parser.add_argument('--count', type=int, default=5, help='Number of normal users to create')
        # Optional arguments for custom superuser credentials
        parser.add_argument('--admin-user', type=str, default='admin', help='Superuser username')
        parser.add_argument('--admin-pass', type=str, default='password123', help='Superuser password')
        parser.add_argument('--admin-email', type=str, default='admin@projectr.local', help='Superuser email')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        admin_user = kwargs['admin_user']
        admin_pass = kwargs['admin_pass']
        admin_email = kwargs['admin_email']
        default_user_pass = 'password123'

        self.stdout.write(self.style.WARNING('Starting data seed...'))

        # 1. Ensure Groups Exist
        users_group, created_u = Group.objects.get_or_create(name='Users')
        managers_group, created_m = Group.objects.get_or_create(name='Managers')
        if created_u or created_m:
            self.stdout.write(self.style.SUCCESS("Groups 'Users' and 'Managers' created."))
        else:
            self.stdout.write("Groups already exist.")

        # 2. Create Superuser
        if not User.objects.filter(username=admin_user).exists():
            try:
                User.objects.create_superuser(
                    username=admin_user,
                    email=admin_email,
                    password=admin_pass,
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write(self.style.SUCCESS(f"Superuser '{admin_user}' created. Password: {admin_pass}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating superuser: {e}"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{admin_user}' already exists."))

        # 3. Create Normal Users
        for _ in range(count):
            i = random.randint(100, 999)  # Generate a random 3-digit number
            username = f'user{i}'
            email = f'user{i}@example.com'
            print(username, email)
            
            if not User.objects.filter(username=username).exists():
                try:
                    # Create User (Signals in apps/account/signals.py will trigger Profile creation)
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=default_user_pass,
                        first_name='User',
                        last_name=str(i)
                    )

                    # Replicate RegisterView logic: Add to 'Users' group
                    user.groups.add(users_group)
                    
                    self.stdout.write(self.style.SUCCESS(f"User '{username}' created."))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to create {username}: {e}"))
            else:
                self.stdout.write(f"User '{username}' already exists.")

        self.stdout.write(self.style.SUCCESS(f"\nSeeding Complete!"))
        self.stdout.write(f"Superuser: {admin_user} / {admin_pass}")
        self.stdout.write(f"Normal Users: user1...user{count} / {default_user_pass}")