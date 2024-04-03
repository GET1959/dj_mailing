from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from jobs.models import Mailing, Attempt


class MailingCreateView(CreateView):
    model = Mailing
    extra_context = {
        'title': 'Создание рассылки'
    }
    fields = ('title', 'recipients', 'message', 'start_time', 'stop_time', 'next_sending', 'frequency',)
    success_url = reverse_lazy('jobs:list')


class MailingListView(ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылки'
    }


class MailingDetailView(DetailView):
    model = Mailing
    extra_context = {
        'title': 'Информация о рассылке'
    }


class MailingUpdateView(UpdateView):
    model = Mailing
    extra_context = {
        'title': 'Редактирование рассылки'
    }
    fields = ('title', 'recipients', 'message', 'start_time', 'stop_time', 'next_sending', 'frequency',)
    success_url = reverse_lazy('jobs:list')


class MailingDeleteView(DeleteView):
    model = Mailing
    extra_context = {
        'title': 'Удаление рассылки'
    }
    success_url = reverse_lazy('jobs:list')


class AttemptListView(ListView):
    model = Attempt
    extra_context = {
        'title': 'Попытки рассылок'
    }
