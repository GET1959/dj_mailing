from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mess.forms import MessageForm
from mess.models import Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    extra_context = {"title": "Новое сообщение"}
    success_url = reverse_lazy("mess:list")


class MessageListView(ListView):
    model = Message
    extra_context = {"title": "Сообщения"}


class MessageDetailView(DetailView):
    model = Message
    extra_context = {"title": "Сообщение рассылки"}


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    extra_context = {"title": "Редактирование сообщения"}
    success_url = reverse_lazy("mess:list")


class MessageDeleteView(DeleteView):
    model = Message
    extra_context = {"title": "Удаление сообщения"}
    success_url = reverse_lazy("mess:list")
