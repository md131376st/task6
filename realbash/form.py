from django import forms
from .models import CsvDoc


class Myform(forms.ModelForm):
    class Meta:
        model = CsvDoc
        fields ='__all__'

