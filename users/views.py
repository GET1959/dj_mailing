from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    LoginView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, TemplateView, View, ListView

from users.forms import (
    UserRegisterForm,
    UserProfileForm,
    UserLoginForm,
    UserForgotPasswordForm,
    UserSetNewPasswordForm,
)
from users.models import User
from users.services import generate_password


# CURRENT_SITE = Site.objects.get_current().domain  # Установил в админке DOMAIN NAME 127.0.0.1:8000
CURRENT_SITE = "127.0.0.1:8000"


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    # def get_queryset(self, **kwargs):
    #     if self.request.user.is_superuser or self.request.user.is_staff:
    #         return Mailing.objects.all()
    #     view_perm = Permission.objects.get(codename='view_mailing')
    #     change_perm = Permission.objects.get(codename='change_mailing')
    #     delete_perm = Permission.objects.get(codename='delete_mailing')
    #     self.request.user.user_permissions.set([view_perm, change_perm, delete_perm])
    #     return Mailing.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy("users:confirm_email", kwargs={"uidb64": uid, "token": token})
        send_mail(
            subject="Подтвердите свой электронный адрес",
            message=f"""Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой
            адрес электронной почты: http://{CURRENT_SITE}{activation_url}""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return redirect("users:email_confirmation_sent")


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """

    form_class = UserLoginForm
    template_name = "users/login.html"
    next_page = "/"
    success_message = "Добро пожаловать на сайт!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация на сайте"
        return context


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = generate_password(12)
    send_mail(
        subject="Вы сменили пароль",
        message=f"Ваш новый пароль: {new_password}\n Скопируйте его и войдите здесь http://{CURRENT_SITE}/users",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse("users:pw_generated_sent"))


class PasswordGeneratedSent(TemplateView):
    template_name = "users/pw_generated_sent.html"


class UserConfirmEmailView(View):

    @staticmethod
    def get(request, uidb64, token):

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("users:email_confirmed")
        else:
            return redirect("users:email_confirmation_failed")


class EmailConfirmationSentView(TemplateView):
    template_name = "users/email_confirmation_sent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено"
        return context


class EmailConfirmedView(TemplateView):
    template_name = "users/email_confirmed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес активирован"
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = "users/email_confirmation_failed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес не активирован"
        return context


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Контроллер по сбросу пароля по почте
    """

    form_class = UserForgotPasswordForm
    template_name = "users/user_password_reset.html"
    success_url = reverse_lazy("users:pw_request_sent")
    success_message = "Письмо с инструкцией по восстановлению пароля отправлена на ваш email"
    subject_template_name = "users/email/password_subject_reset_mail.txt"
    email_template_name = "users/email/password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class PasswordRequestSent(TemplateView):
    template_name = "users/pw_request_sent.html"


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Контроллер установки нового пароля
    """

    form_class = UserSetNewPasswordForm
    template_name = "users/user_password_set_new.html"
    success_url = reverse_lazy("users:pw_changed")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context


class PasswordChanged(SuccessMessageMixin, LoginView):
    """
    Уведомление об успешной смене пароля
    """

    form_class = UserLoginForm
    template_name = "users/pw_changed.html"
    next_page = "/"
    success_message = "Добро пожаловать на сайт!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пароль успешно изменен"
        return context


class AuthorizationRequest(SuccessMessageMixin, LoginView):
    """
    запрос авторизации
    """

    form_class = UserLoginForm
    template_name = "users/auth_request.html"
    next_page = "/"
    success_message = "Добро пожаловать на сайт!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Для посещения этой страницы необходимо авторизоваться"
        return context


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    extra_context = {"title": "Пользователи"}
    permission_required = ["users.view_user", "users.set_activity"]

    def has_permission(self):
        is_manager = self.request.user.groups.filter(name='manager').exists()
        return is_manager


def activity_trigger(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
    else:
        user_item.is_active = True
    user_item.save()
    return redirect('users:user_list')
