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
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

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