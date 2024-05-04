from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    DeleteView,
)

from blog.models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ("title", "body", "image", "views_count")
    success_url = reverse_lazy("blog:list")


class ArticleListView(ListView):
    model = Article
    extra_context = {"title": "Статьи блога"}


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


def activity_trigger(request, pk):
    mailing_item = get_object_or_404(Article, pk=pk)
    if mailing_item.is_active:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True
    mailing_item.save()
    return redirect('blog:list')


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy("blog:list")
