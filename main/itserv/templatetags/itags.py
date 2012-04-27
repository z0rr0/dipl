#-*- coding: utf-8 -*-
from django import template
import locale

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
register = template.Library()

@register.filter(name='errorcss')
def errorcss(value):
    u""" 
    Стиль для поля с ошибкой 
    """
    return " error" if value else ""