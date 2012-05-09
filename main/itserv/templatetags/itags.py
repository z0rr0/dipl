#-*- coding: utf-8 -*-
from django.db.models import Sum
from django import template
import locale

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
register = template.Library()

@register.filter(name='rusnum')
def rusnum(value):
    return locale.format('%0.2f', value, True)

@register.filter(name='errorcss')
def errorcss(value):
    u""" 
    Стиль для поля с ошибкой 
    """
    return " error" if value else ""

@register.filter(name='curproduct')
def curproduct(value, arg):
    u""" 
    Получение элемента списка
    """
    return value[int(arg)]

@register.filter(name='allprodnum')
def allprodnum(value):
    u""" 
    Получение количества товаров
    """
    total = value.aggregate(s=Sum('number'))
    return total['s']
