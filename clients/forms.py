from django import forms

from clients.models import Client
from jobs.forms import StyleFormMixin


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'email', 'comment',)
