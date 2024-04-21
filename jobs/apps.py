from time import sleep

from django.apps import AppConfig


class JobsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jobs"

    # def ready(self):
    #     from jobs.management.commands.runapjobs import Command
    #     sleep(2)
    #     Command().handle()
