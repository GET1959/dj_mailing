from django.contrib import admin

from jobs.models import Mailing


# Register your models here.
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'start_time', 'stop_time', 'next_sending', 'frequency',)
