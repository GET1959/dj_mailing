from django.urls import path
from django.views.decorators.cache import never_cache, cache_page

from blog.apps import BlogConfig
from blog.views import (
    ArticleCreateView,
    ArticleListView,
    ArticleDetailView,
    ArticleDeleteView, activity_trigger,
)

app_name = BlogConfig.name

urlpatterns = [
    path("create/", never_cache(ArticleCreateView.as_view()), name="create"),
    path("", cache_page(60)(ArticleListView.as_view()), name="list"),
    path("view/<int:pk>/", ArticleDetailView.as_view(), name="view"),
    path("delete/<int:pk>/", ArticleDeleteView.as_view(), name="delete"),
    path('activity/<int:pk>/', activity_trigger, name='activity_trigger'),
]
