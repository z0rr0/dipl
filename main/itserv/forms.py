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

class ProductForm(forms.ModelForm):
    u"""
    Форма для добавления/правки данных о товаре
    """
    class Meta:
        model = Product
        fields = ('provider', 'name', 'price', 'rest', 'service', 'comment')  

class ProductSmallForm(forms.ModelForm):
    u"""
    Форма для добавления/правки данных о товаре
    """
    class Meta:
        model = Product
        fields = ('service', 'name', 'price', 'rest', 'comment')
        widgets = {
            # 'name': forms.TextInput(attrs={'style': 'width: 100%'}),
            'comment': forms.TextInput()}

class ProductManyForm(forms.ModelForm):
    u"""
    Форма для добавления/правки данных о нескольких товарах
    """
    class Meta:
        model = Product
        fields = ('provider', 'name', 'price', 'rest', 'service', 'comment')
        widgets = {'provider': forms.Select(attrs={'style': 'width: 100%'}),
            'name': forms.TextInput(attrs={'style': 'width: 100%'}),
            'price': forms.TextInput(attrs={'style': 'width: 100%'}),
            'rest': forms.TextInput(attrs={'style': 'width: 100%'}),
            'comment': forms.TextInput()}

class ProviderSelectForm(forms.Form):
    u"""
    список для выбора поставщиков
    """
    provider = Provider.objects.all()
    CHOICES = [(0, '-----')]
    # CHOICES += [(p.id, p.name) for p in Provider.objects.all()]
    provider = forms.ChoiceField(label=u'поставщик', widget=forms.Select(), choices=CHOICES)
    onlyservice = forms.BooleanField(label=u'только услуги', widget=forms.CheckboxInput())  

class ClientForm(forms.ModelForm):
    u"""
    Форма для добавления/правки данных клиенте
    """
    class Meta:
        model = Client
        fields = ('name', 'phone', 'email', 'discont', 'address', 'comment')

class ReqClientSelectForm(forms.Form):
    u"""
    список для выбора поставщиков
    """
    # список
    CHOICES = [(0, '-----')]
    # CHOICES += [(p.id, p.name) for p in Client.objects.filter(id__in=free_reqlists)]
    client = forms.ChoiceField(label=u'Клиент', widget=forms.Select(), choices=CHOICES)
