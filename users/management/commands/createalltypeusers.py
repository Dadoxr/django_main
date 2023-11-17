import os
from typing import Any
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        superuser = User.objects.get_or_create(
            email=os.getenv('STAFF_SUPERUSER_EMAIL'), #admin@admin.admin
            is_staff=True,
            is_superuser=True,
        )
        staff = User.objects.get_or_create(
            email=os.getenv('STAFF_EMAIL'), #staff@staff.staff
            is_staff=True,
            is_superuser=False,
        )
        blog_manager = User.objects.get_or_create(
            email=os.getenv('BLOG_MANAGER_EMAIL'), #blog@blog.blog
            is_staff=True,
            is_superuser=False,
        )
        user = User.objects.get_or_create(
            email=os.getenv('USER_EMAIL'), #user@user.user
            is_staff=False,
            is_superuser=False,
        )

        superuser[0].set_password(os.getenv('SUPERUSER_STAFF_USER_PASSWORD')) #1111
        staff[0].set_password(os.getenv('SUPERUSER_STAFF_USER_PASSWORD')) #1111
        blog_manager[0].set_password(os.getenv('SUPERUSER_STAFF_USER_PASSWORD')) #1111
        user[0].set_password(os.getenv('SUPERUSER_STAFF_USER_PASSWORD')) #1111
        
        superuser[0].save()
        staff[0].save()
        blog_manager[0].save()
        user[0].save()

