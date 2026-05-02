from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates or updates the default superuser'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@farm.com',
                password='farmadmin2026'
            )
            self.stdout.write('Superuser created successfully')
        else:
            user = User.objects.get(username='admin')
            user.set_password('farmadmin2026')
            user.save()
            self.stdout.write('Superuser password updated')