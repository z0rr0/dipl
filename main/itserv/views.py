#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.template.response import TemplateResponse
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.core.context_processors import csrf
from django.db.models import Q, F, Sum, Count
from django.db import transaction
from django.contrib import auth

from itserv.models import *
from itserv.forms import *

# import the logging library
import logging, math
# Get an instance of a logger
logger = logging.getLogger(__name__)

PAGE_COUNT = 10

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

# for private use
def allobj(request, model):
    objlist = model.objects.all()
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            searchtext = request.POST['searchtext']
            objlist = objlist.filter(name__icontains=searchtext)
    else:
        searchtext = ""
    return objlist, searchtext

@login_required
def obj_all(request, vtemplate, model):
    u""" 
    Список объектов, с возможным фильтром по имени
    """
    c = {}
    c.update(csrf(request))
    objlist, searchtext = allobj(request, model)
    return TemplateResponse(request, vtemplate, {'objlist': objlist, 'searchtext': searchtext})

@login_required_ajax404
def obj_all_ajax(request, vtemplate, model):
    u""" 
    Список объектов, с возможным фильтром по имени, полученный в ajax запросе
    """
    c = {}
    c.update(csrf(request))
    objlist, searchtext = allobj(request, model)
    return TemplateResponse(request, vtemplate, {'objlist': objlist, 'searchtext': searchtext})

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

@permission_required('itserv.change_provider')
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

@permission_required('itserv.add_provider')
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
    form.fields['provider'].choices += [(p.id, p.name) for p in Provider.objects.all()]
    return TemplateResponse(request, vtemplate, {'form': form})

# private function
def pagination_info(objs, onpage, page):
    u"""
    Возвращает переменные для постраничного просмотра
    """
    countobj = objs.count()
    # количество страниц, это число >=1
    pagec = math.ceil(countobj/float(onpage))
    pagec = 1 if pagec < 1 else pagec
    # итератор для страниц
    allpage = range(1, int(pagec + 1))
    # текущая страница не должна выходить за границы
    if page < 1:
        page = 1
    elif page > pagec:
        page = pagec
    getobj = objs[(page-1)*onpage:page*onpage]
    return getobj, allpage, page

@login_required_ajax404
def product_search(request, vtemplate):
    u"""
    поиск товаров и/или услуг по базовым критериям
    """
    products = Product.objects.all()
    page = 1
    prov = 0
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
        if 'page' in request.GET:
            page = int(request.GET['page'])
        # постраничный просмотр
        products, iter_page, page = pagination_info(products, PAGE_COUNT, page)
    except (KeyError, ValueError) as err:
        logger.info(err)
    return TemplateResponse(request, vtemplate, {'products': products, 'provider': prov,
        'page': page, 'allpage': iter_page})

@permission_required('itserv.change_product')
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

@permission_required('itserv.add_product')
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

@permission_required('itserv.add_product')
def product_manyadd(request, extra_num, vtemplate):
    u"""
    Добавление сразу нескольких товарос/услуг
    """
    c = {}
    c.update(csrf(request))
    extra_num = 1 if int(extra_num) < 1 else int(extra_num)
    ProductFormSet = modelformset_factory(Product, extra=extra_num, form=ProductManyForm)
    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            with transaction.commit_on_success():
                for form in formset:
                    # skip empty forms
                    if form.cleaned_data:
                        product = form.save()
            return redirect('/products/')
    else:
        qproduct = Product.objects.none()
        formset = ProductFormSet(queryset=qproduct)
    return TemplateResponse(request, vtemplate, {'formset': formset})

@login_required_ajax404
def product_smalledit(request, id, vtemplate):
    # Быстрое редактирование товара
    if request.user.has_perm('itserv.change_product'):
        product = get_object_or_404(Product, pk=int(id))
        if request.method == 'POST':
            status = 0
            try:
                form = ProductSmallForm(request.POST, instance=product, auto_id='id_' + str(product.id) + '_%s')
                if form.is_valid():
                    form.save()
                    # данные сохранены
                    status = 1
            except:
                pass
            if status:
                return HttpResponse(str(status))
        else:
            form = ProductSmallForm(instance=product, auto_id='id_' + str(product.id) + '_%s')
        if 'page' in request.GET:
            page = request.GET['page']
        else:
            page = 1
    else:
        return HttpResponseNotFound('Error search object')
    return TemplateResponse(request, vtemplate, {'form': form, 'page': page, 'product': product})

@login_required_ajax404
def product_smallview(request, id, vtemplate):
    u"""
    просмотр данных о товаре/услуге по ID
    """
    product = get_object_or_404(Product, pk=int(id))
    if 'page' in request.GET:
        page = request.GET['page']
    else:
        page = 1
    return TemplateResponse(request, vtemplate, {'product': product, 'page': page,})

@login_required
def client_all(request, vtemplate, model):
    u""" 
    Список объектов, с возможным фильтром по имени
    """
    c = {}
    c.update(csrf(request))
    objlist, searchtext = allobj(request, model)
    try:
        if 'client' in request.GET:
            client = Client.objects.get(pk=int(request.GET['client']))
            searchtext = client.name
            objlist = objlist.filter(name=searchtext)
    except:
        pass
    return TemplateResponse(request, vtemplate, {'objlist': objlist, 'searchtext': searchtext})

@permission_required('itserv.change_client')
def client_edit(request, id, vtemplate):
    u""" 
    Редактирование данных о клиенте 
    """
    c = {}
    c.update(csrf(request))
    client = get_object_or_404(Client, id=int(id))
    form, client, saved = get_obj_form(request, client, ClientForm)
    if saved:
        return redirect('/clients/')
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Редактирование'})

@permission_required('itserv.add_client')
def client_add(request, vtemplate):
    u""" 
    Добавление данных о клиенте 
    """
    c = {}
    c.update(csrf(request))
    form, client, saved = get_obj_form(request, None, ClientForm)
    if saved:
        return redirect('/clients/')
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Добавление'})

@login_required
def reqlist_all(request, vtemplate):
    u"""
    Клиенты, оставившие заявки
    """
    first = 0
    try:
        if 'client' in request.GET:
            client = int(request.GET['client'])
        else:
            client = first
    except (KeyError, ValueError) as err:
        client = first
    form = ReqClientSelectForm(initial={'client': client})
    # set choises
    free_reqlists = Reqlist.objects.filter(contract__isnull=True).values_list('client')
    form.fields['client'].choices +=[(p.id, p.name) for p in Client.objects.filter(id__in=free_reqlists)]
    return TemplateResponse(request, vtemplate, {'form': form})

@login_required_ajax404
def reqlist_search(request, vtemplate):
    u"""
    поиск заявок клиента(ов)
    """
    c = {}
    c.update(csrf(request))
    # request не содеждит name, фильтра не будет
    objlist = Reqlist.objects.filter(contract__isnull=True)
    client_id = 0
    try:
        if request.method == 'POST':
            if 'client' in request.POST:
                client_id = int(request.POST['client'])
    except (KeyError, ValueError) as err:
        pass
    # число столбцов в таблице
    cols = 5 
    if client_id:
        objlist = objlist.filter(client=client_id)
        cols = cols - 1
    allsum = 0
    for obj in objlist:
        obj.itog = obj.product.price * obj.number
        allsum += obj.itog
    return TemplateResponse(request, vtemplate, {'objlist': objlist, 
        'client': client_id, 'allsum': allsum, 'cols': cols})

@permission_required('itserv.add_reqlist')
def reqlist_add(request, client, vtemplate):
    u"""
    добавление заявки
    """
    client = get_object_or_404(Client, pk=int(client))
    client_info = [u'тел. ' + client.phone]
    if client.discont:
        client_info.append(u'скидка ' + str(client.discont) + '%')
    return TemplateResponse(request, vtemplate, {'client': client, 'info': client_info})

@login_required_ajax404
def reqlist_client_ajax(request, vtemplate):
    u""" 
    Список товаров, еще отсутстующих в заявке клиента, на которые еще не заключены сделки
    """
    try:
        client = int(request.POST['client'])
        name = request.POST.get('name', '')
    except (KeyError, ValueError) as err:
        return HttpResponseNotFound('Error, not found client info')
    reqlist_products = Reqlist.objects.filter(contract__isnull=True, client=client).values_list('product')
    products = Product.objects.exclude(id__in=reqlist_products).filter(Q(service=True)|Q(rest__gt=0))
    if name:
        products = products.filter(name__icontains=name)
    return TemplateResponse(request, vtemplate, {'objlist': products, 'client': client})

@login_required_ajax404
def reqlist_client(request, client, vtemplate):
    u""" 
    Список заявок клиента
    """
    c = {}
    c.update(csrf(request))
    client = get_object_or_404(Client, pk=int(client))
    try:
        if request.method == 'POST':
            countreq = request.POST['len']
            if request.user.has_perm('itserv.change_reqlist'):
                with transaction.commit_on_success():
                    for i in range(1, int(countreq) + 1):
                        id = int(request.POST['id' + str(i)])
                        number = int(request.POST['number' + str(i)])
                        reqlist = Reqlist.objects.filter(pk=id).update(number=number)
    except:
        pass
    reqlists = Reqlist.objects.filter(contract__isnull=True, client=client)
    allsum = 0
    for obj in reqlists:
        obj.itog = obj.product.price * obj.number
        allsum += obj.itog
    allsum_disc = allsum * (1 - client.discont/100.0)
    return TemplateResponse(request, vtemplate, {'reqlists': reqlists, 'allsum': allsum,
        'discont': client.discont, 'allsum_disc': allsum_disc, 'client': client})

@login_required_ajax404
@transaction.autocommit
def reqlist_plus(request, client, product):
    u""" 
    Добавление данных об объекте в Ajax запросе
    """
    status = 'ERROR'
    if request.user.has_perm('itserv.add_reqlist'):
        obj = Reqlist(
            client=get_object_or_404(Client, pk=int(client)),
            product=get_object_or_404(Product, pk=int(product)))
        obj.save()
        status = 'OK'
    else:
        return HttpResponseNotFound('Error delete')
    return HttpResponse(status)

@login_required
def contract_all(request, vtemplate, model):
    u""" 
    Список контрактов, с возможным фильтром номеру или клиенту
    """
    c = {}
    c.update(csrf(request))
    objlist = model.objects.all()
    if request.method == 'POST':
        searchtext = request.POST.get('searchtext', '')
        objlist = objlist.filter(Q(number__icontains=searchtext) | Q(client__name__icontains=searchtext))
    else:
        searchtext = ""
        try:
            if 'client' in request.GET:
                client = Client.objects.get(pk=int(request.GET['client']))
                searchtext = client.name
                objlist = objlist.filter(client__name=searchtext)
        except:
            pass
    return TemplateResponse(request, vtemplate, {'objlist': objlist, 'searchtext': searchtext})

@permission_required('itserv.add_contract')
def contract_add(request, vtemplate):
    u""" 
    Добавление данных о контракте
    """
    c = {}
    c.update(csrf(request))
    form, contract, saved = get_obj_form(request, None, ContractForm)
    if saved:
        return redirect('/contract/addreq/' + str(contract.id))
    # клиенты
    free_reqlists = Reqlist.objects.filter(contract__isnull=True).values_list('client')
    form.fields['client'].choices =[(p.id, p.name) for p in Client.objects.filter(id__in=free_reqlists)]
    # сотрудники
    free_users = User.objects.filter(is_active=True).only('id', 'last_name', 'first_name')
    form.fields['user'].choices =[(p.id, "%s %s" % (p.first_name, p.last_name)) for p in free_users]
    try:
        if request.method != 'POST':
            form.initial['user'] = request.user.id
            if 'client' in request.GET:
                form.initial['client'] = int(request.GET['client'])
    except:
        pass
    # отправка данных
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Добавление'})    

@permission_required('itserv.change_contract')
def contract_edit(request, id, vtemplate):
    u""" 
    Редактирование данных о контракте 
    """
    c = {}
    c.update(csrf(request))
    contract = get_object_or_404(Contract, id=int(id))
    form, contract, saved = get_obj_form(request, contract, ContractForm)
    if saved:
        return redirect('/contracts/')
    # клиенты
    free_reqlists = Reqlist.objects.filter(contract__isnull=True).values_list('client')
    # текущий клиент должен быть в списке
    form.fields['client'].choices =[(p.id, p.name) for p in Client.objects.filter(Q(id__in=free_reqlists) | Q(pk=contract.client.id))]
    # сотрудники
    free_users = User.objects.filter(is_active=True).only('id', 'last_name', 'first_name')
    form.fields['user'].choices =[(p.id, "%s %s" % (p.first_name, p.last_name)) for p in free_users]
    # отправка данных
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Редактирование'})

@permission_required('itserv.delete_contract')
def contract_delete(request, id, t, redirecturl):
    u""" 
    Удалении данных о контракте

    type (t) = 0 - заявки становятся свободными (по-умолчанию, по параметрам модели)
    type (t) = 1 - заявки тоже удаляются
    """
    obj = get_object_or_404(Contract, pk=int(id))
    with transaction.commit_on_success():
        if t:
            reqlists = Reqlist.objects.filter(contract=obj).delete()
        obj.delete()
    # return TemplateResponse(request, 'contract_home.html')
    return HttpResponseRedirect(redirecturl)

@permission_required('itserv.change_contract')
def contract_addreq(request, id, vtemplate):
    u""" 
    Правка набора товаров для заказа
    """
    c = {}
    c.update(csrf(request))
    contract = get_object_or_404(Contract, pk=int(id))
    discont = contract.client.discont + contract.discont
    reqlists = Reqlist.objects.filter(client=contract.client_id)
    reqlists = reqlists.filter(Q(contract=contract) | Q(contract__isnull=True))
    initform = []
    data1 = {}
    data2 = {}
    for obj in reqlists:
        use = True if obj.contract_id else False
        initform.append({'id': obj.id, 'number': obj.number, 'for_use': use, 'price': obj.product.price})
        data1[obj.id] =  obj.product.name
        data2[obj.id] =  obj.product.price
    # form
    ReqlistFormSet = formset_factory(ContractList, extra=0)
    if request.method == 'POST':
        formset = ReqlistFormSet(request.POST)
        if formset.is_valid():
            with transaction.commit_on_success():
                allsum = 0
                for form in formset:
                    data = form.cleaned_data
                    # logger.info(data)
                    if data['for_use']:
                        reqlst = Reqlist.objects.filter(pk=int(data['id'])).update(
                            number=int(data['number']),
                            price=data2[data['id']],
                            contract=contract)
                        allsum += int(data['number']) * data2[data['id']]
                    else:
                        reqlst = Reqlist.objects.filter(pk=int(data['id'])).update(
                            number=int(data['number']),
                            price=None,
                            contract=None)
                contract.total_all = allsum
                contract.total_disc = allsum * (1 - discont/100.0)
                contract.save()
            return redirect('/contracts/')
    else:
        formset = ReqlistFormSet(initial=initform)
    # скидка
    return TemplateResponse(request, vtemplate, {'contract': contract,  'formset': formset,
        'discont': discont, 'data_product': data1, 'data_price': data2 })

@login_required
def report_contracts(request, vtemplate):
    a = 2
    return TemplateResponse(request, vtemplate, {})