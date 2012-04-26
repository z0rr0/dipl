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
# from itserv.forms import *

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# --------- MAIN FUNTIONS -------------
# home page
@login_required
def index(request, vtemplate):
    u""" 
    Главная страница 
    """
    deviz = u"быстро, удобно, надежно"
    # logger.info(program)
    return TemplateResponse(request, vtemplate, {'deviz': deviz})