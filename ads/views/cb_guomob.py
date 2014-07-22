
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Guomob
from django.http import HttpResponse
from ads.views.apns import cb_apns_notify

import logging, json
from urllib import unquote

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

logger = logging.getLogger('django')

def cb_guomob_ios(request):
    ret = {}
    ret['message'] = 'ok'

    logger.info('cb_guomob_ios request params: ' + ' '.join(request.GET.keys()))
    try:
        order = request.GET.get('order')
        app = request.GET.get('app')
        ad = unquote( request.GET.get('ad') )
        adsid = request.GET.get('adsid')
        device = request.GET.get('device')
        mac = request.GET.get('mac')
        idfa = request.GET.get('idfa')
        openudid = request.GET.get('openudid')
        price = float( request.GET.get('price') )
        points = int( request.GET.get('points') )
        time = request.GET.get('time')
        sign = request.GET.get('sign')

        logger.info('cb_guomob_ios  device:' + device + '  points:' + str(points))
        records = Guomob.objects.filter(order=order, device=device)
        if len(records) == 0:
            Guomob.objects.create(order=order, app=app, ad=ad, adsid=adsid,
            device=device, mac=mac, idfa=idfa, openudid=openudid, price=price, points=points, time=time )

            #update user point record
            user = User.objects.get(dev_id=device)
            PointRecord.objects.create(user=user, channel=u'果盟', task=ad, point=points, status='ok')
            user.total_points += points
            user.save()

            cb_apns_notify(user.token, ad, points)
    finally:
        return SuccessResponse(ret)



def cb_guomob_android(request):
    ret = {}
    ret['message'] = 'error'
    return HttpResponse(ret)

def show_guomob(request):
    ret = {}
    ret['records'] = []

    records = Guomob.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())

    return SuccessResponse(ret)

