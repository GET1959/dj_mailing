from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name='имя')
    email = models.EmailField(max_length=150, verbose_name='почта')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
