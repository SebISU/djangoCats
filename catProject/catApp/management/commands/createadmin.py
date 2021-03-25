from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create the initial admin account.'

    def handle(self, *args, **options):
        user = User.objects.create_user(username="admin", password="admin",
                email="admin@admin.com")
        user.is_staff = True
        user.is_superuser = True
        user.save()
