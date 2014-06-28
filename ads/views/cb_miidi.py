
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Miidi
from django.http import HttpResponse

import logging, json
from urllib import unquote

logger = logging.getLogger('django')

def cb_miidi_ios(request):
    ret = {}
    ret['message'] = u'ok'

    #logger.info('cb_miidi_ios request params: ' + ' '.join(request.GET.keys()))
    try:
        adid = request.GET.get('id')
        trand_no = request.GET.get('trand_no')
        cash = int (request.GET.get('cash') )
        imei = request.GET.get('imei')
        bundleId = request.GET.get('bundleId')
        param0 = request.GET.get('param0')
        appName = unquote( request.GET.get('appName') )
        sign = request.GET.get('sign')
        
        logger.info('cb_miidi_ios  imei:' + imei + '  cash:' + str(cash))
        records = Miidi.objects.filter(imei=imei, trand_no=trand_no)
        if len(records) == 0:
            Miidi.objects.create(adid=adid, trand_no=trand_no, cash=cash, imei=imei,
            bundleId=bundleId, param0=param0, appName=appName )

            #update user point record
            user = User.objects.get(dev_id=imei)
            PointRecord.objects.create(user=user, channel=u'米迪', task=appName, point=cash, status='ok')
            user.total_points += cash
            user.save()
            return SuccessResponse(ret)
        else:
            ret['message'] = u'duplicate'
            return SuccessResponse(ret)
    except:
        ret['message'] = u'error'
        return SuccessResponse(ret)



def cb_miidi_android(request):
    ret = {}
    ret['message'] = 'error'
    return HttpResponse(ret)

def show_miidi(request):
    ret = {}
    ret['records'] = []

    records = Miidi.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())

    return SuccessResponse(ret)

