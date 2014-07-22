
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Dianjoy
from django.http import HttpResponse
from ads.views.apns import cb_apns_notify

import logging, json
from urllib import unquote

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

logger = logging.getLogger('django')

def check_token(time_stamp, token, type='ios'):
    if type == 'ios':
        sk = 'B3rwUJwyuIFFGrYz'
    else:
        sk = 'Go6MaX27ZS8RHfJV'

    import hashlib
    if hashlib.md5(time_stamp+sk).hexdigest() == token:
        return True
        
    raise MyException('token illegal')

def cb_dianjoy_ios(request):

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

        check_token(time_stamp, token)

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

            cb_apns_notify(user.token, ad_name, currency)
    finally:
        return HttpResponse('200')


def cb_dianjoy_android(request):
    
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

        check_token(time_stamp, token, 'android')

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

