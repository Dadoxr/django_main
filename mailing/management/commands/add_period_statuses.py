from typing import Any
from django.core.management import BaseCommand

from mailing.models import NameSetting
from django.conf import settings


class Command(BaseCommand):
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        for category_name, category_value in settings.NAMESETTING.items():
            for setting_name, setting_values in category_value.items():
                NameSetting.objects.get_or_create(
                    category=category_name, 
                    name=setting_values.get('name')
                )
        
