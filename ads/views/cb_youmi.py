
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Youmi
from django.http import HttpResponse
 
import logging, json
from urllib import unquote

logger = logging.getLogger('django')
       

def cb_youmi_ios(request):
    logger.info('cb_youmi_ios request params: ' + ' '.join(request.GET.keys()))
    try:
        order = request.GET.get('order')
        app = request.GET.get('app')
        ad = request.GET.get('ad')
        adid = request.GET.get('adid')
        user = request.GET.get('user')
        device = request.GET.get('device')
        chn = request.GET.get('chn')
        price = float(request.GET.get('price'))
        point = int(request.GET.get('points'))
        time = request.GET.get('time')
        sig = request.GET.get('sig')
        sign = request.GET.get('sign')

        logger.info('cb_youmi_ios  device:' + device + '  point:' + str(point))
        records = Youmi.objects.filter(order=order, device=device)
        if len(records) == 0:
            Youmi.objects.create(type='ios',order=order, app=app, ad=ad, adid=str(adid), user=user, device=device,
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
    
    logger.info('cb_youmi_android request params: ' + ' '.join(request.GET.keys()))
    try:
        order = request.GET.get('order')
        app = request.GET.get('app')
        ad = request.GET.get('ad')
        user = request.GET.get('user')
        device = request.GET.get('device')
        chn = request.GET.get('chn')
        point = int(request.GET.get('points'))
        time = request.GET.get('time')
        #sign = request.GET.get('sign')

        logger.info('cb_youmi_android  device:' + device + '  point:' + str(point))
        records = Youmi.objects.filter(order=order, device=device)
        if len(records) == 0:
            Youmi.objects.create(type='android',order=order, app=app, ad=unquote(ad), user=user, device=unquote(device),
            chn=chn, point=point, time=time)

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
        logger.info('cb_youmi_android  failed' )
        return HttpResponse('error')   

def show_youmi(request):
    ret = {}
    ret['records'] = []

    records = Youmi.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())
    
    return SuccessResponse(ret)

