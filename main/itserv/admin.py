#-*- coding: utf-8 -*-
from django.contrib import admin
from itserv.models import Client, Provider, Product, Contract, Reqlist

class ClientAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'student', 'key', 'comment', 'date_start')
    search_fields = ('name', 'comment', )

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'site')
    search_fields = ('name', 'comment',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price', 'rest')
    search_fields = ('name',)
    list_filter = ('provider',)

class ContractAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'total_all', 'total_disc')
    search_fields = ('number',)
    list_filter = ('user',)

class ReqlistAdmin(admin.ModelAdmin):
    list_display = ('client', 'contract', 'product', 'number', 'price')
    search_fields = ('product__name', 'client__name')
    list_filter = ('client', 'contract',)

admin.site.register(Client, ClientAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Reqlist, ReqlistAdmin)


