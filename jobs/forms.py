from django import forms

from jobs.models import Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class MailingForm(StyleFormMixin, forms.ModelForm):

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
