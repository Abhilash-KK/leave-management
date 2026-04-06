from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Initializes roles (Groups) and creates test users'

    def handle(self, *args, **options):
        # 1. Create Groups
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        user_group, _ = Group.objects.get_or_create(name='User')

        # 2. Create Test Users
        users = [
            ('admin_user', 'admin123', admin_group),
            ('teacher_user', 'teacher123', teacher_group),
            ('regular_user', 'user123', user_group),
        ]

        for username, password, group in users:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            else:
                self.stdout.write(f'User {username} already exists')

        self.stdout.write(self.style.SUCCESS('Role initialization complete.'))
