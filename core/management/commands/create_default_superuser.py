from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates a default superuser if none exists'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@farm.com',
                password='changeme123'
            )
            self.stdout.write('Superuser created successfully')
        else:
            self.stdout.write('Superuser already exists')