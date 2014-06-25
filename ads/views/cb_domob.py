
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Domob
from django.http import HttpResponse

import logging, json
from urllib import unquote

logger = logging.getLogger('django')

def cb_domob_ios(request):
    ret = {}
    ret['message'] = 'ok'

    logger.info('cb_domob_ios request params: ' + ' '.join(request.GET.keys()))
    try:
        orderid = request.GET.get('orderid')
        pubid = request.GET.get('pubid')
        ad = unquote( request.GET.get('ad') )
        adid = request.GET.get('adid')
        user = request.GET.get('user')
        device = request.GET.get('device')
        channel = request.GET.get('channel')
        price = float( request.GET.get('price') )
        point = int( request.GET.get('point') )
        ts = request.GET.get('ts')
        sign = request.GET.get('sign')

        logger.info('cb_domob_ios  device:' + device + '  point:' + str(point))
        records = Domob.objects.filter(orderid=orderid, device=device)
        if len(records) == 0:
            Domob.objects.create(orderid=orderid, pubid=pubid, ad=ad, adid=adid,
            user=user, device=device, channel=channel, price=price, point=point, ts=ts )

            #update user point record
            user = User.objects.get(dev_id=device)
            PointRecord.objects.create(user=user, channel=u'多盟', task=ad, point=point, status='ok')
            user.total_points += point
            user.save()
            return SuccessResponse(ret)
        else:
            ret['message'] = 'duplicate'
            return SuccessResponse(ret)
    except:
        ret['message'] = 'error'
        return SuccessResponse(ret)



def cb_domob_android(request):
    ret = {}
    ret['message'] = 'error'
    return HttpResponse(ret)

def show_domob(request):
    ret = {}
    ret['records'] = []

    records = Domob.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())

    return SuccessResponse(ret)

