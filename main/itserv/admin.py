#-*- coding: utf-8 -*-
from django.contrib import admin
from itserv.models import Client, Provider, Product, Contract, CRequest

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

class CRequestAdmin(admin.ModelAdmin):
    list_display = ('contract', 'product', 'number')
    search_fields = ('number',)
    list_filter = ('contract',)

admin.site.register(Client, ClientAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(CRequest, CRequestAdmin)


