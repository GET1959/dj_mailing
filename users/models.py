from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name="телефон")
    avatar = models.ImageField(upload_to="users/", **NULLABLE, verbose_name="аватар")
    is_active = models.BooleanField(default=True, verbose_name="активен")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ("set_activity", "Активация пользователя")
        ]
