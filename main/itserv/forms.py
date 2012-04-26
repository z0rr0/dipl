#-*- coding: utf-8 -*-
from itserv.models import *
from django import forms

class ProviderForm(forms.ModelForm):
    u"""
    Форма для добавления/правки данных поставщиках
    """

    class Meta:
        model = Provider
        fields = ('name', 'phone', 'email', 'address', 'site', 'comment')