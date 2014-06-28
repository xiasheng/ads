
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Dianjoy
from django.http import HttpResponse

import logging, json
from urllib import unquote

logger = logging.getLogger('django')


def cb_dianjoy_ios(request):

    #logger.info('cb_dianjoy_ios request params: ' + ' '.join(request.GET.keys()))
    try:
        snuid = request.GET.get('snuid')
        device_id = request.GET.get('device_id')
        app_id = request.GET.get('app_id')
        currency = int( request.GET.get('currency') )
        app_ratio = float( request.GET.get('app_ratio') )
        time_stamp = request.GET.get('time_stamp')
        ad_name = unquote( request.GET.get('ad_name') )
        pack_name = request.GET.get('pack_name')
        token = request.GET.get('token')

        logger.info('cb_dianjoy_ios  device_id:' + device_id + '  currency:' + str(currency))
        records = Dianjoy.objects.filter(device_id=device_id, ad_name=ad_name)
        if len(records) == 0:
            Dianjoy.objects.create(snuid=snuid, device_id=device_id, app_id=app_id, currency=currency,
            app_ratio=app_ratio, time_stamp=time_stamp, ad_name=ad_name, pack_name=pack_name)

            #update user point record
            user = User.objects.get(dev_id=device_id)
            PointRecord.objects.create(user=user, channel=u'点乐', task=ad_name, point=currency, status='ok')
            user.total_points += currency
            user.save()
    finally:
        return HttpResponse('200')


def cb_dianjoy_android(request):
    
    #logger.info('cb_dianjoy_android request params: ' + ' '.join(request.GET.keys()))
    try:
        snuid = request.GET.get('snuid')
        device_id = request.GET.get('device_id')
        app_id = request.GET.get('app_id')
        currency = int( request.GET.get('currency') )
        app_ratio = float( request.GET.get('app_ratio') )
        time_stamp = request.GET.get('time_stamp')
        ad_name = unquote( request.GET.get('ad_name') )
        pack_name = request.GET.get('pack_name')
        task_id = request.GET.get('task_id')
        trade_type = request.GET.get('trade_type')
        token = request.GET.get('token')

        logger.info('cb_dianjoy_android  device_id:' + device_id + '  currency:' + str(currency))
        records = Dianjoy.objects.filter(device_id=device_id, ad_name=ad_name)
        if len(records) == 0:
            Dianjoy.objects.create(type='android', snuid=snuid, device_id=device_id, app_id=app_id, currency=currency,
            app_ratio=app_ratio, time_stamp=time_stamp, ad_name=ad_name, pack_name=pack_name)

            #update user point record
            user = User.objects.get(dev_id=device_id)
            PointRecord.objects.create(user=user, channel=u'点乐', task=ad_name, point=currency, status='ok')
            user.total_points += currency
            user.save()
    finally:
        return HttpResponse('200') 


def show_dianjoy(request):
    ret = {}
    ret['records'] = []

    records = Dianjoy.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())

    return SuccessResponse(ret)
