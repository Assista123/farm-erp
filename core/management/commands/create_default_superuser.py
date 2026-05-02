import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates or fixes the default superuser'

    def handle(self, *args, **kwargs):
        password = os.environ.get('ADMIN_PASSWORD', 'farmadmin2026')
        user, created = User.objects.get_or_create(username='admin')
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.email = 'admin@farm.com'
        user.save()
        self.stdout.write(f'Admin user {"created" if created else "updated"} with password from environment')