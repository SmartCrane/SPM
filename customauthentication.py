# -*- coding: UTF-8 -*-
'''
Created on 2015年6月6日

@author: lisongwei
'''
import traceback
from urllib import url2pathname
import urlparse

from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from SPM import settings
from SPM.models import CustomUser


@csrf_protect
@never_cache
def customlogin(request,template_name='registration/login.html',redirect_field_name=REDIRECT_FIELD_NAME):
#     try:
#         user = authenticate(username='xz', password='admin')
#     except:
#         traceback.print_exc()
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    if request.method == "POST":
        user = CustomUser.objects.get(username='xz');
        user.backend='django.contrib.auth.backends.ModelBackend'
        if user is not None:
            if user.is_active:
                login(request, user)
                redirect_to = request.POST.get(redirect_field_name,
                                       request.GET.get(redirect_field_name, ''))
                return HttpResponseRedirect(redirect_to)
    else:
        nextparms = request.GET.get('next')
        urlstr= urlparse.urlparse(nextparms)
        urlparms = urlparse.parse_qs(urlstr.query,True)
        usercode = ""
        if urlparms:
            usercode = urlparms['usercode'][0]
        #如果存在用户code
        if usercode:
            try:
                user = CustomUser.objects.get(username=usercode)
                user.backend='django.contrib.auth.backends.ModelBackend'
            #如果用户不存在则返回form    
            except CustomUser.DoesNotExist:
                form = AuthenticationForm(request)
                current_site = get_current_site(request)
                context = {
                    'form': form,
                    redirect_field_name: redirect_to,
                    'site': current_site,
                    'site_name': current_site.name,
                }
                return HttpResponseRedirect('http://'+current_site+'/portal/')
            #如果用户存在则登录
            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect_to = request.POST.get(redirect_field_name,
                                           request.GET.get(redirect_field_name, ''))
                    return HttpResponseRedirect(redirect_to)
        #如果不存在usercode返回form
        else:
            form = AuthenticationForm(request)
            current_site = get_current_site(request)
            context = {
                'form': form,
                redirect_field_name: redirect_to,
                'site': current_site,
                'site_name': current_site.name,
            }
            return HttpResponseRedirect('http://'+current_site+'/portal/')
