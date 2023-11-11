import os
from typing import Any
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        superuser = User.objects.create(
            email=os.getenv('STAFF_SUPERUSER_EMAIL'), #admin@admin.admin
            is_staff=True,
            is_superuser=True,
        )
        staff = User.objects.create(
            email=os.getenv('STAFF_EMAIL'), #staff@staff.staff
            is_staff=True,
            is_superuser=False,
        )
        user = User.objects.create(
            email=os.getenv('USER_EMAIL'), #user@user.user
            is_staff=False,
            is_superuser=False,
        )

        superuser.set_password(os.getenv('SUPERUSER_STAFF_USER_PASSWORD')) #1111
        staff.set_password(os.getenv('SUPERUSER_STAFF_USER_PASSWORD')) #1111
        user.set_password(os.getenv('SUPERUSER_STAFF_USER_PASSWORD')) #1111
        
        superuser.save()
        staff.save()
        user.save()
