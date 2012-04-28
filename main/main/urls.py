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

    # поставщики - полный список
    url(r'^providers/$', 'itserv.views.obj_all', {
        'vtemplate': 'provider_home.html',
        'model': Provider
        }),
    # удаление поставщика
    (r'^provider/delete/(?P<id>\d+)/?$', 'itserv.views.obj_delete', {
        'redirecturl': '/providers/',
        'model': Provider, 
        'perm': 'itserv.delete_provider'}),
    # редактирование данных о поставщике
    (r'^provider/edit/(?P<id>\d+)/?$', 'itserv.views.provider_edit', {
        'vtemplate': 'provider_edit.html'}),
    # добавление данных о поставщике
    (r'^provider/add/?$', 'itserv.views.provider_add', {
        'vtemplate': 'provider_edit.html'}),

    # товары
    url(r'^products/$', 'itserv.views.product_all', {
        'vtemplate': 'product_home.html',
        }),
    # поиск товаров
    url(r'^product/search/$', 'itserv.views.product_search', {
        'vtemplate': 'product_search.html',
        }),
    # удаление товара
    (r'^product/delete/(?P<id>\d+)/?$', 'itserv.views.obj_delete', {
        'redirecturl': '/products/',
        'model': Product, 
        'perm': 'itserv.delete_product'}),
    (r'^product/ajdel/(?P<id>\d+)/?$', 'itserv.views.obj_delete_ajax', {
        'model': Product,
        'perm': 'itserv.delete_product'}),
    # редактирование данных о товаре
    (r'^product/edit/(?P<id>\d+)/?$', 'itserv.views.product_edit', {
        'vtemplate': 'product_edit.html'}),
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