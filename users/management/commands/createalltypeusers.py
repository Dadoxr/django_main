from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.conf import settings
import os

from users.models import User

def add_permissions_to_group(group, permissions):
    if permissions:
        permission_objects = Permission.objects.filter(codename__in=permissions)
        group.permissions.add(*permission_objects)

class Command(BaseCommand):
    def create_or_update_user(self, email, is_staff, is_superuser, group_list):
        user, just_created = User.objects.get_or_create(
            email=email,
            defaults={
                'is_staff': is_staff,
                'is_superuser': is_superuser,
            }
        )

        if just_created:
            for group_name in group_list:
                user.groups.add(Group.objects.get(name=group_name))
            user.set_password(os.getenv('SUPERUSER_STAFF_USER_PASSWORD')) # 1111
            user.save()

    def handle(self, *args, **options):

        for name, codename_list in settings.ALL_TYPES_USERS_PERMISSIONS.items():
            group, just_created = Group.objects.get_or_create(name=name)
            if just_created:
                add_permissions_to_group(group, codename_list)

        self.create_or_update_user(os.getenv('STAFF_SUPERUSER_EMAIL'), True, True, ['blog','staff']
        )
        self.create_or_update_user(
            os.getenv('BLOG_MANAGER_EMAIL'), True, False, ['blog']
        )
        self.create_or_update_user(
            os.getenv('STAFF_EMAIL'), True, False, ['staff']
        )
        self.create_or_update_user(
            os.getenv('USER_EMAIL'), False, False, ['user']
        )
