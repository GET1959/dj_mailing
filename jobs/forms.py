from django import forms

from clients.models import Client
from jobs.models import Mailing
from mess.models import Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class MailingForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Получаем текущего пользователя из kwargs
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Фильтруем поле clients только для тех клиентов, которые принадлежат текущему пользователю
        if self.request and self.request.user:
            self.fields['recipients'].queryset = Client.objects.filter(owner=self.request.user)
            self.fields['message'].queryset = Message.objects.filter(owner=self.request.user)

    class Meta:
        model = Mailing
        fields = (
            "title",
            "recipients",
            "message",
            "start_time",
            "stop_time",
            "next_sending",
            "frequency",
        )


class MailingManagerForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ("is_active",)
