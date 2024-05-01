from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from clients.forms import ClientForm
from clients.models import Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    extra_context = {"title": "Создание клиента"}
    success_url = reverse_lazy("clients:list")


class ClientListView(ListView):
    model = Client
    extra_context = {"title": "Клиенты"}

    def get_queryset(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(DetailView):
    model = Client
    extra_context = {"title": "Информация о клиенте"}


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {"title": "Редактирование профиля"}
    success_url = reverse_lazy("clients:list")


class ClientDeleteView(DeleteView):
    model = Client
    extra_context = {"title": "Удаление клиента"}
    success_url = reverse_lazy("client:list")
