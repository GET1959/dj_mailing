from django import forms

from jobs.forms import StyleFormMixin
from mess.models import Message


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = (
            "title",
            "content",
        )
