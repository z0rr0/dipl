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
    price = forms.FloatField(min_value=0)
    rest = forms.IntegerField(min_value=0)

    class Meta:
        model = Product
        fields = ('service', 'name', 'price', 'rest', 'comment')
        widgets = {
            # 'name': forms.TextInput(attrs={'style': 'width: 100%'}),
            'comment': forms.TextInput(),
        }

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
    discont = forms.FloatField(label=u'Скидка', min_value=0, max_value=100, initial=0, help_text=u'постоянная скидка клиента (0-100%)')

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

class ContractForm(forms.ModelForm):
    u"""
    Форма для добавления/правки данных о контакте
    """
    discont = forms.FloatField(label=u'Скидка', min_value=0, max_value=100, initial=0, help_text=u'скидка на сделку (0-100)')

    class Meta:
        model = Contract
        fields = ('user', 'client', 'number', 'discont', 'date', 'comment')


class ContractList(forms.Form):
    u"""
    Выбор товаров в заказ
    """
    id = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    for_use = forms.BooleanField(label=u'выбрать', widget=forms.CheckboxInput(), required=False)
    number = forms.IntegerField(label=u'количество', min_value=0)
    price = forms.FloatField(label=u'цена', min_value=0, widget=forms.HiddenInput)
