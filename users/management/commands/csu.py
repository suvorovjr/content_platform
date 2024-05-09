from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            phone_number='9998887766',
            first_name='Adminfirst',
            last_name='Adminlast',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password('admin')
        user.save()
