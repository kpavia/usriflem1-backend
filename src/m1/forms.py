from django import forms
from m1.models import Receiver


class RifleDateForm(forms.ModelForm):

    serial_number = forms.CharField(label='Serial Number', max_length=10)

    class Meta:
        model = Receiver
        fields = ['maker']

