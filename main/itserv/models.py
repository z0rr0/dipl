#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Для сотрудников используется стандартная модель User

class Client(models.Model):
    u"""
    Клиенты сервиса
    
    """
    name = models.CharField(max_length = 127, verbose_name=u'имя', db_index=True, help_text=u'Ф.И.О. или название организации')
    phone = models.CharField(max_length=15, verbose_name=u'телефон', help_text=u'номер телефона')
    email = models.EmailField(max_length=255, verbose_name=u'email', blank=True, null=True, help_text=u'адрес электронной почты')
    address = models.TextField(verbose_name = u'адрес', blank=True, null=True, help_text=u'почтовый адрес')
    discont = models.FloatField(default=0, verbose_name=u'скидка', help_text=u'постоянная скидка клиента (0-100%)')
    comment = models.TextField(verbose_name=u'примечание', blank=True, null=True)
    # даты изменения и создания, заполняются автоматически
    modified = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False, help_text=u'дата редактирования объекта')
    created = models.DateTimeField(auto_now_add=True, editable=False, help_text=u'дата создания объекта')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = u"клиент"
        verbose_name_plural = u"клиенты"

class Provider(models.Model):
    u"""
    Поставщики
    """
    name = models.CharField(max_length=127, verbose_name=u'название', unique = True, help_text=u'название организации или предпринимателя')
    address = models.TextField(verbose_name = u'адрес', blank=True, null=True, help_text=u'почтовый адрес')
    phone = models.CharField(max_length=15, verbose_name=u'телефон', help_text=u'номер телефона')
    email = models.EmailField(max_length=255, verbose_name=u'email', blank=True, null=True, help_text=u'адрес электронной почты')
    site = models.URLField(max_length=255, verbose_name=u'сайт', blank=True, null=True, help_text=u'адрес сайта поставщика (если есть)')
    comment = models.TextField(verbose_name=u'примечание', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False, help_text=u'дата редактирования объекта')
    created = models.DateTimeField(auto_now_add=True, editable=False, help_text=u'дата создания объекта')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = u"поставщик"
        verbose_name_plural = u"поставщики"

class Product(models.Model):
    u"""
    Товары и услуги
    """
    provider = models.ForeignKey(Provider, verbose_name = u'поставщик', blank=True, null=True, on_delete=models.SET_NULL, help_text=u'поставщик товара')
    name = models.CharField(max_length=127, verbose_name=u'наименование', unique = True, help_text=u'название торва или услуги')
    service = models.BooleanField(verbose_name = u'услуга', default = False, help_text = u'является услугой, а не товаром', db_index=True)
    price = models.FloatField(default=0, verbose_name=u'цена', help_text=u'цена за единицу торара/услуги')
    rest = models.PositiveIntegerField(default=0, verbose_name=u'остаток', help_text=u'количество в наличии', db_index=True)
    comment = models.TextField(verbose_name=u'примечание', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False, help_text=u'дата редактирования объекта')
    created = models.DateTimeField(auto_now_add=True, editable=False, help_text=u'дата создания объекта')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['service', 'name']
        verbose_name = u"товар/услуга"
        verbose_name_plural = u"товары/услуги"

class Contract(models.Model):
    u"""
    Сделка
    """
    user = models.ForeignKey(User, verbose_name = u'сотрудник')
    discont = models.FloatField(default=0, verbose_name=u'скидка', help_text=u'скидка на сделку')
    total_all = models.FloatField(default=0, verbose_name=u'сумма сделки')
    total_disc = models.FloatField(default=0, verbose_name=u'сумма со скидками')
    number = models.CharField(max_length=50, verbose_name=u'номер договора', unique = True)
    date = models.DateField(verbose_name = u'дата', help_text = u'дата заключения сделки', db_index=True)
    comment = models.TextField(verbose_name=u'примечание', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False, help_text=u'дата редактирования объекта')
    created = models.DateTimeField(auto_now_add=True, editable=False, help_text=u'дата создания объекта')

    def __unicode__(self):
        return self.number

    class Meta:
        ordering = ['date']
        verbose_name = u"сделка"
        verbose_name_plural = u"сделки"

class Reqlist(models.Model):
    u"""
    Заявка
    """
    client = models.ForeignKey(Client, verbose_name = u'клиент')
    contract = models.ForeignKey(Contract, verbose_name=u'сделка', blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name=u'товар')
    number = models.PositiveIntegerField(default=1, verbose_name=u'количество')
    price = models.FloatField(verbose_name=u'цена', help_text=u'фиксированная цена', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False, help_text=u'дата редактирования объекта')
    created = models.DateTimeField(auto_now_add=True, editable=False, help_text=u'дата создания объекта')

    def __unicode__(self):
        return "%s - %s (%s)" % (self.client.name, self.product.name, self.number)

    class Meta:
        ordering = ['contract', 'client__name', 'product__service', 'product__name', 'created']
        verbose_name = u"заявка"
        verbose_name_plural = u"заявки"
