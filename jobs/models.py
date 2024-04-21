from django.db import models

from clients.models import Client
from mess.models import Message

NULLABLE = {"blank": True, "null": True}


class Mailing(models.Model):
    title = models.CharField(max_length=150, verbose_name="рассылка")
    recipients = models.ManyToManyField(Client, verbose_name="Получатели")  # Edit fields
    message = models.ForeignKey(
        Message, default=0, on_delete=models.CASCADE, verbose_name="сообщение"
    )  # Edit fields
    start_time = models.DateTimeField(verbose_name="старт рассылки")
    stop_time = models.DateTimeField(verbose_name="окончание рассылки")
    next_sending = models.DateTimeField(verbose_name="следующая отправка")
    frequency = models.CharField(max_length=50, verbose_name="периодичность рассылки")
    status = models.CharField(max_length=150, default="created", verbose_name="статус рассылки")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"


class Attempt(models.Model):
    name = models.CharField(max_length=150, verbose_name="попытка")  # Edit fields
    attempt_mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, **NULLABLE, verbose_name="название рассылки"
    )
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="время попытки")
    attempt_result = models.CharField(
        max_length=150, default="успешно", verbose_name="результат попытки"
    )
    server_response = models.TextField(**NULLABLE, verbose_name="ответ сервера")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "попытка"
        verbose_name_plural = "попытки"
