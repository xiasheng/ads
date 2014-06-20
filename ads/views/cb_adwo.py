
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Adwo
from django.http import HttpResponse
 
import logging, json
from urllib import unquote

logger = logging.getLogger('django')
       
def cb_adwo_ios(request):
    ret = {}
    logger.info('cb_adwo_ios request params: ' + ' '.join(request.GET.keys()))    
    try:    
        appid = request.GET.get('appid')
        adname = unquote( request.GET.get('adname') )
        adid = request.GET.get('adid')
        device = request.GET.get('device')
        idfa = request.GET.get('idfa')
        point = int(request.GET.get('point'))
        ts = int(request.GET.get('ts'))
        sign = request.GET.get('sign')
        
        logger.info('cb_adwo_ios  device:' + device + '  point:' + str(point))
        records = Adwo.objects.filter(device=device, idfa=idfa, ts=ts)
        if len(records) == 0:
            Adwo.objects.create(appid=appid, adname=adname, adid=adid, device=device, idfa=idfa, point=point, ts=ts)
            
            #update user point record
            user = User.objects.get(mac=device)
            PointRecord.objects.create(user=user, channel=u'安沃', task=adname, point=point, status='ok')
            user.total_points += point
            user.save()
            return HttpResponse('success')
        else:
            return HttpResponse('duplicate')
    except:
        return HttpResponse('error')



def cb_adwo_android(request):
    ret = {}

    #logger.info('cb_adwo_android request params: ' + ' '.join(request.GET.keys()))
    try:
        appid = request.GET.get('appid')
        adname = unquote( request.GET.get('adname') )
        adid = request.GET.get('adid')
        androidid = request.GET.get('androidid')
        device = request.GET.get('device')
        imei = request.GET.get('imei')
        point = int(request.GET.get('point'))
        ts = int(request.GET.get('ts'))
        sign = request.GET.get('sign')

        logger.info('cb_adwo_android  device:' + device + '  point:' + str(point))
        records = Adwo.objects.filter(imei=imei, ts=ts)
        if len(records) == 0:
            Adwo.objects.create(appid=appid, adname=adname, adid=adid, androidid=androidid, device=device, imei=imei, point=point, ts=ts)

            #update user point record
            user = User.objects.get(dev_id=imei)
            PointRecord.objects.create(user=user, channel=u'安沃', task=adname, point=point, status='ok')
            user.total_points += point
            user.save()
            return HttpResponse('success')
        else:
            return HttpResponse('duplicate')
    except: 
        return HttpResponse('error')

def show_adwo(request):
    ret = {}
    ret['records'] = []

    records = Adwo.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())
    
    return SuccessResponse(ret)

