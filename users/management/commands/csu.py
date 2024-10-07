import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from users.models import User

load_dotenv()

SU_EMAIL = os.getenv("SU_EMAIL")
SU_PASSWORD = os.getenv("SU_PASSWORD")


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=SU_EMAIL,
            first_name="admin_first_name",
            last_name="admin_last_name",
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(SU_PASSWORD)
        user.save()
