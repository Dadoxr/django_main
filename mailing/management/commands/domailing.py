# runapscheduler.py
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore


from mailing.services import check_time_and_send_mail

logger = logging.getLogger(__name__)


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
      check_time_and_send_mail,
      trigger=CronTrigger(minute="*/5"),
      id="check_time_and_send_mail", 
      max_instances=1,
      replace_existing=True,
    )


    logger.info("Added job 'check_time_and_send_mail'.")

    try:
      logger.info("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")
