from django.conf import settings
from django.db import models

from clients.models import Client
from mess.models import Message

NULLABLE = {"blank": True, "null": True}


class Mailing(models.Model):
    FREQ_CHOICES = [
        ("10 секунд", "10 секунд"),
        ("минута", "минута"),
        ("день", "день"),
        ("неделя", "неделя"),
        ("месяц", "месяц"),
    ]

    title = models.CharField(max_length=150, verbose_name="рассылка")
    recipients = models.ManyToManyField(Client, verbose_name="Получатели")
    message = models.ForeignKey(Message, default=0, on_delete=models.CASCADE, verbose_name="сообщение")
    start_time = models.DateTimeField(verbose_name="старт рассылки")
    stop_time = models.DateTimeField(verbose_name="окончание рассылки")
    next_sending = models.DateTimeField(verbose_name="следующая отправка")
    frequency = models.CharField(max_length=50, choices=FREQ_CHOICES, verbose_name="периодичность рассылки")
    status = models.CharField(max_length=150, default="created", verbose_name="статус рассылки")
    is_active = models.BooleanField(**NULLABLE, default=True, verbose_name="активна")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        permissions = [
            ("set_activity", "Активация рассылки")
        ]

    def has_object_permissions(self, owner):
        return self.owner == owner


class Attempt(models.Model):
    name = models.CharField(max_length=150, verbose_name="попытка")  # Edit fields
    attempt_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, **NULLABLE, verbose_name="название рассылки")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="время попытки")
    attempt_result = models.CharField(max_length=150, default="успешно", verbose_name="результат попытки")
    server_response = models.TextField(**NULLABLE, verbose_name="ответ сервера")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "попытка"
        verbose_name_plural = "попытки"
