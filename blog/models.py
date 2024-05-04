from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(upload_to="blog/", null=True, blank=True, verbose_name="Изображение")
    views_count = models.IntegerField(default=0, verbose_name="просмотры")
    create_date = models.DateField(auto_now_add=True, verbose_name="Дата публикации")
    is_active = models.BooleanField(default=True, verbose_name="активна")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        permissions = [
            ("set_activity", "Управление статьей")
        ]
