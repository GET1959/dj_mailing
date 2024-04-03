from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(default=0, verbose_name='текст сообщения')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
