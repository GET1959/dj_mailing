from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from clients.models import Client


class ClientCreateView(CreateView):
    model = Client
    extra_context = {
        'title': 'Создание клиента'
    }
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('clients:list')


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }


class ClientDetailView(DetailView):
    model = Client
    extra_context = {
        'title': 'Информация о клиенте'
    }


class ClientUpdateView(UpdateView):
    model = Client
    extra_context = {
        'title': 'Редактирование профиля'
    }
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('clients:list')

class ClientDeleteView(DeleteView):
    model = Client
    extra_context = {
        'title': 'Удаление клиента'
    }
    success_url = reverse_lazy('client:list')
