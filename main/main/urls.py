#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login, logout
from itserv.models import *

urlpatterns = patterns('',
    # accounts
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$' , logout),
    # Examples:
    # url(r'^$', 'main.views.home', name='home'),
    # url(r'^main/', include('main.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # главная страница
    url(r'^$', 'itserv.views.index', {'vtemplate': 'index.html'}),

    # **************************************************
    # ПОСТАВЩИКИ
    # **************************************************
    url(r'^providers/$', 'itserv.views.obj_all', {
        'vtemplate': 'provider_home.html',
        'model': Provider
        }),
    # удаление поставщика
    url(r'^provider/delete/(?P<id>\d+)/?$', 'itserv.views.obj_delete', {
        'redirecturl': '/providers/',
        'model': Provider, 
        'perm': 'itserv.delete_provider'}),
    # редактирование данных о поставщике
    url(r'^provider/edit/(?P<id>\d+)/?$', 'itserv.views.provider_edit', {
        'vtemplate': 'provider_edit.html'}),
    # добавление данных о поставщике
    url(r'^provider/add/?$', 'itserv.views.provider_add', {
        'vtemplate': 'provider_edit.html'}),

    # **************************************************
    # ТОВАРЫ
    # **************************************************
    url(r'^products/$', 'itserv.views.product_all', {
        'vtemplate': 'product_home.html'}),
    # поиск товаров
    url(r'^product/search/$', 'itserv.views.product_search', {
        'vtemplate': 'product_search.html'}),
    # удаление товара
    url(r'^product/delete/(?P<id>\d+)/?$', 'itserv.views.obj_delete', {
        'redirecturl': '/products/',
        'model': Product, 
        'perm': 'itserv.delete_product'}),
    url(r'^product/ajdel/(?P<id>\d+)/?$', 'itserv.views.obj_delete_ajax', {
        'model': Product,
        'perm': 'itserv.delete_product'}),
    # редактирование данных о товаре
    url(r'^product/edit/(?P<id>\d+)/?$', 'itserv.views.product_edit', {
        'vtemplate': 'product_edit.html'}),
    # добавление данных о товаре
    url(r'^product/add/?$', 'itserv.views.product_add', {
        'vtemplate': 'product_edit.html'}),
    # добавление нескольких строк данных о товаре/услуге
    url(r'^product/many/(?P<extra_num>\d+)/?$', 'itserv.views.product_manyadd', {
        'vtemplate': 'product_manyadd.html'}),
    # редактирование только основных данных о товаре
    url(r'^product/smalledit/(?P<id>\d+)/?$', 'itserv.views.product_smalledit', {
        'vtemplate': 'product_smalledit.html'}),
    # просмотр основных данных о товаре
    url(r'^product/smallview/(?P<id>\d+)/?$', 'itserv.views.product_smallview', {
        'vtemplate': 'product_smallview.html'}),

    # **************************************************
    # КЛИЕНТЫ
    # **************************************************
    url(r'^clients/$', 'itserv.views.client_all', {
        'vtemplate': 'client_home.html',
        'model': Client}),
    # удаление клиента
    url(r'^client/delete/(?P<id>\d+)/?$', 'itserv.views.obj_delete', {
        'redirecturl': '/clients/',
        'model': Client, 
        'perm': 'itserv.delete_client'}),
    # редактирование данных о клиента
    url(r'^client/edit/(?P<id>\d+)/?$', 'itserv.views.client_edit', {
        'vtemplate': 'client_edit.html'}),
    # добавление данных о клиенте
    url(r'^client/add/?$', 'itserv.views.client_add', {
        'vtemplate': 'client_edit.html'}),

    # **************************************************
    # ЗАЯВКИ
    # **************************************************
    url(r'^reqlists/$', 'itserv.views.reqlist_all', {
        'vtemplate': 'reqlist_home.html'}),
    # заявки и товары для них
    url(r'^reqlist/product/$', 'itserv.views.reqlist_client_ajax', {
        'vtemplate': 'reqlist_product.html'}),
    # поиск заявок по клиенту
    url(r'^reqlist/search/$', 'itserv.views.reqlist_search', {
        'vtemplate': 'reqlist_search.html'}),
    url(r'^reqlist/ajdel/(?P<id>\d+)/?$', 'itserv.views.obj_delete_ajax', {
        'model': Reqlist,
        'perm': 'itserv.delete_reqlist'}),
    url(r'^reqlist/add/(?P<client>\d+)/?$', 'itserv.views.reqlist_add', {
        'vtemplate': 'reqlist_add.html'}),
    url(r'^reqlist/client/(?P<client>\d+)/?$', 'itserv.views.reqlist_client', {
        'vtemplate': 'reqlist_client.html'}),
    url(r'^reqlist/plus/(?P<client>\d+)/(?P<product>\d+)/?$', 'itserv.views.reqlist_plus'),

    # **************************************************
    # КОНТРАКТЫ
    # **************************************************
    url(r'^contracts/$', 'itserv.views.contract_all', {
        'vtemplate': 'contract_home.html',
        'model': Contract}),
    # добавление данных о контракте
    url(r'^contract/add/?$', 'itserv.views.contract_add', {
        'vtemplate': 'contract_edit.html'}),
    # редактирование данных о контракте
    url(r'^contract/edit/(?P<id>\d+)/?$', 'itserv.views.contract_edit', {
        'vtemplate': 'contract_edit.html'}),
    # удаление контракта
    url(r'^contract/delete/(?P<id>\d+)/?$', 'itserv.views.contract_delete', {
        'redirecturl': '/contracts/', 't': 0}),
    url(r'^contract/delete/(?P<id>\d+)/?(?P<t>\d?)/?$', 'itserv.views.contract_delete', {
        'redirecturl': '/contracts/'}),
    # правка набора товаров для заказа
    url(r'^contract/addreq/(?P<id>\d+)/?$', 'itserv.views.contract_addreq', {
        'vtemplate': 'contract_addreq.html'}),

    # **************************************************
    # ОТЧЕТЫ
    # **************************************************
    url(r'^reports/contracts/?$', 'itserv.views.report_contracts', {
        'vtemplate': 'report_contracts.html'}),
    url(r'^reports/viewdiv/?$', 'itserv.views.report_view_div', {
        'vtemplate': 'report_contracts_viewdiv.html',
        'format': 'html'
        }),
    url(r'^reports/viewcvs/?$', 'itserv.views.report_view_div', {
        'vtemplate': 'report_contracts_viewdiv.html',
        'format': 'cvs'
        }),
    url(r'^reports/viewexcel/?$', 'itserv.views.report_view_div', {
        'vtemplate': 'report_contracts_viewdiv.html',
        'format': 'excel'
        }),
)

# media content                   
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^robots.txt$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'path': "robots.txt"}),
        url(r'^favicon.ico$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'path': "favicon.ico"}),
   	)