
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Adwo, Youmi
from django.http import HttpResponse
        
def cb_adwo(request):
    ret = {}
    
    try:    
        appid = request.GET.get('appid')
        adname = request.GET.get('adname')
        adid = request.GET.get('adid')
        device = request.GET.get('device')
        idfa = request.GET.get('idfa')
        point = int(request.GET.get('point'))
        ts = request.GET.get('ts')
        sign = request.GET.get('sign')
        
        records = Adwo.objects.filter(device=device, idfa=idfa, ts=ts)
        if len(records) == 0:
            Adwo.objects.create(appid=appid, adname=adname, adid=adid, device=device, idfa=idfa, point=point, ts=ts)
            
            #update user point record
            user = User.objects.get(mac=device)
            PointRecord.objects.create(user=user, channel='adwo', task=adname, point=point, status='ok')
            user.total_points += point
            user.save()
            return HttpResponse('success')
        else:
            return HttpResponse('duplicate')
    except:
        return HttpResponse('error')

def cb_youmi_ios(request):

    try:
        order = request.GET.get('order')
        app = request.GET.get('app')
        ad = request.GET.get('ad')
        adid = request.GET.get('adid')
        user = request.GET.get('user', '')
        device = request.GET.get('device')
        chn = request.GET.get('chn')
        price = float(request.GET.get('price'))
        point = int(request.GET.get('point'))
        time = request.GET.get('time')        
        sign = request.GET.get('sign')

        records = Youmi.objects.filter(order=order, device=device)
        if len(records) == 0:
            Youmi.objects.create(type='ios',order=order, app=app, ad=ad, adid=adid, user=user, device=device,
            chn=chn, price=price, point=point, time=time)

            #update user point record
            if len(device) == 12:
                user = User.objects.get(mac=device)
            else:
                user = User.objects.get(dev_id=device)                
            PointRecord.objects.create(user=user, channel='youmi', task=ad, point=point, status='ok')
            user.total_points += point
            user.save()
            return HttpResponse('success')
        else:
            return HttpResponse('duplicate', status=403)
    except:
        return HttpResponse('error')

def cb_youmi_android(request):

    try:
        order = request.GET.get('order')
        app = request.GET.get('app')
        ad = request.GET.get('ad')
        adid = request.GET.get('adid', '')
        user = request.GET.get('user', '')
        device = request.GET.get('device')
        chn = request.GET.get('chn')
        price = float(request.GET.get('price', 0))
        point = int(request.GET.get('point'))
        time = request.GET.get('time')
        sign = request.GET.get('sign')

        records = Youmi.objects.filter(order=order, device=device)
        if len(records) == 0:
            Youmi.objects.create(type='android',order=order, app=app, ad=ad, adid=adid, user=user, device=device,
            chn=chn, price=price, point=point, time=time)

            #update user point record
            if len(device) == 12:
                user = User.objects.get(mac=device)
            else:
                user = User.objects.get(dev_id=device)                
            PointRecord.objects.create(user=user, channel='youmi', task=ad, point=point, status='ok')
            user.total_points += point
            user.save()
            return HttpResponse('success') 
        else:
            return HttpResponse('duplicate', status=403)
    except:
        return HttpResponse('error')
