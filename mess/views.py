from django.contrib.auth.mixins import LoginRequiredMixin
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


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {"title": "Сообщения"}

    def get_queryset(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView):
    model = Message
    extra_context = {"title": "Сообщение рассылки"}


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    extra_context = {"title": "Редактирование сообщения"}
    success_url = reverse_lazy("mess:list")

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageDeleteView(DeleteView):
    model = Message
    extra_context = {"title": "Удаление сообщения"}
    success_url = reverse_lazy("mess:list")
