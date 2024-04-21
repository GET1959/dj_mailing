from django.contrib import admin

from mess.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title", "content")
