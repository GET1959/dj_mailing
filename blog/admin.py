from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body', 'image', 'create_date', 'views_count',)
    search_fields = ('title', 'body',)
    list_filter = ('create_date', 'views_count',)
