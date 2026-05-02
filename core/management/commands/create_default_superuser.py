from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates or fixes the default superuser'

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(username='admin')
        user.set_password('farmadmin2026')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        if created:
            self.stdout.write('Superuser created')
        else:
            self.stdout.write('Superuser fixed')