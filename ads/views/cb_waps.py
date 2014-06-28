
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Waps
from django.http import HttpResponse

import logging, json
from urllib import unquote

logger = logging.getLogger('django')

def cb_waps_ios(request):
    ret = {}
    ret['message'] = u'成功接收'

    #logger.info('cb_waps_ios request params: ' + ' '.join(request.GET.keys()))
    try:
        adv_id = request.GET.get('adv_id')
        app_id = request.GET.get('app_id')
        key = request.GET.get('key')
        udid = request.GET.get('udid')
        open_udid = request.GET.get('open_udid')
        bill = float( request.GET.get('bill') )
        points = int (request.GET.get('points') )
        ad_name = unquote( request.GET.get('ad_name'))
        status = request.GET.get('status')
        activate_time = request.GET.get('activate_time')
        order_id = request.GET.get('order_id')
        random_code = request.GET.get('random_code')
        wapskey = request.GET.get('wapskey')

        logger.info('cb_waps_ios  udid:' + udid + '  points:' + str(points))
        records = Waps.objects.filter(udid=udid, open_udid=open_udid, order_id=order_id)
        if len(records) == 0:
            Waps.objects.create(adv_id=adv_id, app_id=app_id, key=key, udid=udid,
            open_udid=open_udid, bill=bill, points=points, ad_name=ad_name, 
            status=status, activate_time=activate_time, order_id=order_id )

            #update user point record
            user = User.objects.get(dev_id=udid)
            PointRecord.objects.create(user=user, channel=u'万普', task=ad_name, point=points, status='ok')
            user.total_points += points
            user.save()
            return SuccessResponse(ret)
        else:
            ret['message'] = u'无效数据'
            return SuccessResponse(ret)
    except:
        ret['message'] = u'无效数据'
        return SuccessResponse(ret)



def cb_waps_android(request):
    ret = {}
    ret['message'] = 'error'
    return HttpResponse(ret)

def show_waps(request):
    ret = {}
    ret['records'] = []

    records = Waps.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())

    return SuccessResponse(ret)

