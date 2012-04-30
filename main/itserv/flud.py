#-*- coding: utf-8 -*-
from django.db.models import Q, F, Sum
from django.db import transaction
from datetime import datetime
import string, random

from main.settings import DEBUG
from itserv.models import *

def nodebug(fn):
    def wrapper(*args, **kwargs):
        if not DEBUG:
            print 'It is work with DEBUG only'
            return False
        else:
            fn(*args, **kwargs)
    return wrapper

# generation random value
def gen_salt(size=15):
    chars = string.ascii_letters + string.digits * 5
    return ''.join(random.choice(chars) for x in range(size))

def get_price(a, b):
    r = random.random()
    return round(a + (b-a) * r, 2)

@nodebug
def flud_provider(obj_count=50):
    try:
        for_one_date = datetime.now()
        for i in range(obj_count):
            provider = Provider(
                name=gen_salt(),
                address=u'почтовый адрес',
                phone='8-(831)-47-455-66',
                email='test@apiasi.ru',
                comment=u"создано автоматически",
                modified=for_one_date,
                created=for_one_date,
            )
            provider.save()
            # get id
            provider.name = u'Поставщик' + str(provider.id)
            provider.save()
            print(provider)
    except Provider.DoesNotExist as err:
        print err
        return False
    print 'End function'
    return True

@nodebug
def flud_product(obj_count=50, service=False):
    providers = Provider.objects.all()
    provider_count = providers.count()
    try:
        for_one_date = datetime.now()
        for i in range(obj_count):
            def_name = u'Услуга' if service else u'Товар'
            def_rest = 0 if service else random.randint(10, 100)
            get_provider = random.randint(0, provider_count - 1)
            get_provider = providers[get_provider] if get_provider else None
            product = Product(
                provider=get_provider,
                name=gen_salt(),
                service=service,
                price=get_price(1000, 10000),
                rest=def_rest,
                comment=u"создано автоматически",
                modified=for_one_date,
                created=for_one_date,
            )
            product.save()
            # get id
            product.name = def_name  + str(product.id)
            product.save()
            print(product)
    except Provider.DoesNotExist as err:
        print err
        return False
    return True

@nodebug
def flud_client(obj_count=10):
    try:
        for_one_date = datetime.now()
        for i in range(obj_count):
            client = Client(
                name=gen_salt(),
                phone='8-(831)-47-455-66',
                email='test@apiasi.ru',
                address=u'почтовый адрес',
                discont=0.0,
                comment=u"создано автоматически",
                modified=for_one_date,
                created=for_one_date,
            )
            client.save()
            # get id
            client.name = u'Клиент_' + str(client.id)
            client.save()
            print(client)
    except Client.DoesNotExist as err:
        print err
        return False
    print 'End function'
    return True