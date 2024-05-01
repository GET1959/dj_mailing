from django.conf import settings
from django.db import models


NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name="имя")
    email = models.EmailField(max_length=150, verbose_name="почта")
    comment = models.TextField(**NULLABLE, verbose_name="комментарий")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    # def has_object_permissions(self, owner):
    #     return self.owner == owner
