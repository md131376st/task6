from django import forms
from .models import CsvDoc

""" درست کردن یک فرم برای مدل های data base """


class Myform(forms.ModelForm):
    class Meta:
        model = CsvDoc
        fields ='__all__'

