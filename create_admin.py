import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leave_project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
password = 'admin'
email = 'admin@example.com'

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(username, email, password)
    print("Superuser created successfully.")
else:
    print(f"Superuser {username} already exists. Updating password...")
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print("Password updated successfully.")
