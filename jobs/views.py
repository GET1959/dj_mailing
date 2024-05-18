import random

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from blog.models import Article
from clients.models import Client
from jobs.forms import MailingForm
from jobs.models import Mailing, Attempt
from jobs.services import get_cached_client


class HomeView(TemplateView):
    template_name = 'jobs/home.html'
    extra_context = {
        'title': 'Главная',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mail_count'] = Mailing.objects.all().count()
        context_data['active_mail_count'] = Mailing.objects.filter(is_active=True).count()
        context_data['client_count'] = get_cached_client().count()
        if len(list(Article.objects.all())) > 3:
            context_data['article_list'] = random.sample(list(Article.objects.all()), 3)
        else:
            context_data['article_list'] = list(Article.objects.all())
        return context_data


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {"title": "Создание рассылки"}
    success_url = reverse_lazy("jobs:list")

    # Для отображения в поле 'recipients' только собственных клиентов:
    def get_form_kwargs(self):
        
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.recipients.owner = self.request.user  # 16.05.2024
        self.object.save()
        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    extra_context = {"title": "Рассылки"}
    login_url = "/users"
    redirect_field_name = "users"

    def get_queryset(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(DetailView):
    model = Mailing
    extra_context = {"title": "Информация о рассылке"}


class MailingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'jobs.change_mailing'
    extra_context = {"title": "Редактирование рассылки"}
    success_url = reverse_lazy("jobs:list")

    def has_permission(self):
        mailing = self.get_object()
        is_owner = mailing.has_object_permissions(self.request.user)
        return is_owner


class MailingDeleteView(PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = 'jobs.delete_mailing'
    extra_context = {"title": "Удаление рассылки"}
    success_url = reverse_lazy("jobs:list")

    def has_permission(self):
        product = self.get_object()
        is_owner = product.has_object_permissions(self.request.user)
        return is_owner


class AttemptListView(ListView):
    model = Attempt
    extra_context = {"title": "Попытки рассылок"}


def activity_trigger(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.is_active:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True
    mailing_item.save()
    return redirect('jobs:list')
