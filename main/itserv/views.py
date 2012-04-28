#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.template.response import TemplateResponse
from django.core.context_processors import csrf
from django.db.models import Q, F, Sum
from django.db import transaction
from django.contrib import auth

from itserv.models import *
from itserv.forms import *

# import the logging library
import logging, math
# Get an instance of a logger
logger = logging.getLogger(__name__)

PAGE_COUNT = 10.0

# --------- ADD FUNTIONS -------------
# decorator for ajax login
def login_required_ajax404(fn):
    def wrapper(*args, **kwargs):
        if args[0].user.is_authenticated():
            return fn(*args, **kwargs)
        else:
            return HttpResponseNotFound('Auth error')
    return wrapper

# --------- MAIN FUNTIONS -------------
@login_required
def index(request, vtemplate):
    u""" 
    Главная страница 
    """
    deviz = u"быстро, удобно, надежно"
    # logger.info(program)
    return TemplateResponse(request, vtemplate, {'deviz': deviz})

@login_required
def obj_all(request, vtemplate, model):
    u""" 
    Список объектов
    """
    objlist = model.objects.all()    
    return TemplateResponse(request, vtemplate, {'objlist': objlist})

@login_required
def obj_delete(request, id, redirecturl, model, perm):
    u""" 
    Удалении данных об объекте 
    """
    if request.user.has_perm(perm):
        obj = get_object_or_404(model, pk=int(id))
        with transaction.commit_on_success():
            obj.delete()
            to_url = redirecturl
    else:
        to_url = '/accounts/login/?next=%s' % request.path
    return HttpResponseRedirect(to_url)

@login_required_ajax404
@transaction.autocommit
def obj_delete_ajax(request, id, model, perm):
    u""" 
    Удалении данных об объекте в Ajax запросе
    """
    status = 'ERROR'
    if request.user.has_perm(perm):
        obj = get_object_or_404(model, pk=int(id))
        obj.delete()
        status = 'OK'
    else:
        return HttpResponseNotFound('Error delete')
    return HttpResponse(status)

def get_obj_form(request, setobrj, SetForm):
    u"""
    Добавление или обновление данных об объектах, инициализации или сохранение данных формы
    """
    saved = False
    if request.method == 'POST':
        form = SetForm(request.POST or None, request.FILES, instance=setobrj)
        if form.is_valid():
            with transaction.commit_on_success():
                setobrj = form.save()
                saved = True
    else:
        form = SetForm(instance=setobrj)
    return form, setobrj, saved

permission_required('itserv.change_provider')
def provider_edit(request, id, vtemplate):
    u""" 
    Редактирование данных о поставщике 
    """
    c = {}
    c.update(csrf(request))
    provider = get_object_or_404(Provider, id=int(id))
    form, provider, saved = get_obj_form(request, provider, ProviderForm)
    if saved:
        return redirect('/providers/')
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Редактирование'})

permission_required('itserv.add_provider')
def provider_add(request, vtemplate):
    u""" 
    Редактирование данных о поставщике 
    """
    c = {}
    c.update(csrf(request))
    form, provider, saved = get_obj_form(request, None, ProviderForm)
    if saved:
        return redirect('/providers/')
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Добавление'})

@login_required
def product_all(request, vtemplate):
    u""" 
    Список товаров
    """
    # first = Provider.objects.all()[0]
    # first = first.id
    first = 0
    onlyservice = False
    try:
        if 'provider' in request.GET:
            provider = int(request.GET['provider'])
        else:
            provider = first
        if 'service' in request.GET:
            onlyservice = bool(int(request.GET['service']))
    except (KeyError, ValueError) as err:
        provider = 0
    form = ProviderSelectForm(initial={'provider': provider, 'onlyservice': onlyservice})    
    return TemplateResponse(request, vtemplate, {'form': form})

@login_required_ajax404
def product_search(request, vtemplate):
    u"""
    поиск товаров и/или услуг по базовым критериям
    """
    products = Product.objects.all()
    page = 1
    try:
        if request.method == 'POST':
            prov = int(request.POST['provider'])
            if prov:
                products = products.filter(provider=prov)
            service = int(request.POST['onlyservice'])
            if service:
                products = products.filter(service=True)
            search = request.POST['search']
            if search:
                products = products.filter(Q(name__icontains=search) | Q(comment__icontains=search))
        # количество страниц
        pagec = int(math.ceil(products.count()/PAGE_COUNT))
        pagec = 1 if pagec < 1 else pagec
        allpage = range(1, pagec + 1)
        if 'page' in request.GET:
            page = int(request.GET['page'])
            page = 1 if page < 2 else page
            page = pagec if page > pagec else page
        products = products[(page-1)*PAGE_COUNT:page*PAGE_COUNT]
    except (KeyError, ValueError) as err:
        logger.info(err)
    return TemplateResponse(request, vtemplate, {'products': products, 
        'page': page, 'allpage': allpage, 'pagec': pagec})

permission_required('itserv.change_product')
def product_edit(request, id, vtemplate):
    u""" 
    Редактирование данных о поставщике 
    """
    c = {}
    c.update(csrf(request))
    product = get_object_or_404(Product, id=int(id))
    form, product, saved = get_obj_form(request, product, ProductForm)
    if saved:
        return redirect('/products/?provider=' + str(product.provider.id))
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Редактирование'})

permission_required('itserv.add_product')
def product_add(request, vtemplate):
    u""" 
    Редактирование данных о поставщике 
    """
    c = {}
    c.update(csrf(request))
    form, product, saved = get_obj_form(request, None, ProductForm)
    if saved:
        return redirect('/products/?provider=' + str(product.provider.id))
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Добавление'})