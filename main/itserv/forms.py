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

class ProviderSelectForm(forms.Form):
    u"""
    список для выбора поставщиков
    """
    provider = Provider.objects.all()
    CHOICES = [(0, '-----')]
    CHOICES += [(p.id, p.name) for p in Provider.objects.all()]

    # CHOICES=[(0, '--- все программы ---'),
    #     (u"Для студенов", [(p.id, p.name) for p in program.filter(use_student=True).only('id', 'name')]),
    #     (u"Только для ВУЗа", [(p.id, p.name) for p in program.filter(use_student=False).only('id', 'name')]),
    # ]
    # forms.Select(attrs={'onchange': 'alert("ok")'})
    provider = forms.ChoiceField(label=u'Поставщик', widget=forms.Select(), choices=CHOICES)
    # onlyfree = forms.BooleanField(label=u'только доступные ключи', widget=forms.CheckboxInput())   