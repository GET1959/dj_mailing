import logging
import smtplib
from datetime import datetime, timedelta

import pytz
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from jobs.models import Mailing, Attempt

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fh = logging.FileHandler("mailing.log", mode="w", encoding="utf-8")
fh.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

logger.addHandler(fh)


def get_next_date(period: str):
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    if period == '10 секунд':
        next_date = current_datetime + timedelta(seconds=10)
        return next_date
    elif period == 'минута':
        next_date = current_datetime + timedelta(minutes=1)
        return next_date
    if period == 'день':
        next_date = current_datetime + timedelta(days=1)
        return next_date
    elif period == 'неделя':
        next_date = current_datetime + timedelta(weeks=1)
        return next_date
    elif period == 'месяц':
        next_date = current_datetime + timedelta(days=30)
        return next_date


def my_job():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.all().filter(next_sending__lte=current_datetime).filter(status__in=['created', 'active'])
    for mailing in mailings:
        try:
            send_mail(
                subject=mailing.message.title,
                message=mailing.message.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.recipients.all()],
                fail_silently=False,
            )
            Attempt.objects.create(
                name='email_sending',
                attempt_mailing=mailing,
                attempt_time=current_datetime,
                attempt_result='успешно',
                server_response='OK'
            )
            logger.info(f"email {mailing.title} sent OK")
        except smtplib.SMTPException as e:
            Attempt.objects.create(
                name='email_sending',
                attempt_mailing=mailing,
                attempt_time=current_datetime,
                attempt_result='не отправлено',
                server_response=e
            )
            logger.error(e)
        if mailing.frequency == '10 секунд' and (mailing.stop_time - current_datetime).seconds < 10:
            mailing.status = "completed"
            mailing.save()
        elif mailing.frequency == 'минута' and (mailing.stop_time - current_datetime).seconds < 60:
            mailing.status = "completed"
            mailing.save()
        elif mailing.frequency == 'день' and (mailing.stop_time - current_datetime).days < 1:
            mailing.status = "completed"
            mailing.save()
        elif mailing.frequency == 'неделя' and (mailing.stop_time - current_datetime).days < 7:
            mailing.status = "completed"
            mailing.save()
        elif mailing.frequency == 'месяц' and (mailing.stop_time - current_datetime).days < 30:
            mailing.status = "completed"
            mailing.save()
        else:
            mailing.status = "active"
            mailing.next_sending = get_next_date(mailing.frequency)
            mailing.save()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=300):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.

    https://coderslegacy.com/python/apscheduler-cron-trigger/
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger='interval',  # CronTrigger(),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
