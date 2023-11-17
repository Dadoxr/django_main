
from django.core.management import BaseCommand

from mailing.services import check_time_and_send_mail


class Command(BaseCommand):

    def handle(self, *args, **options):
        check_time_and_send_mail()
        