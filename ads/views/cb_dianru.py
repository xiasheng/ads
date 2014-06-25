
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Dianru
from django.http import HttpResponse

import logging, json
from urllib import unquote

logger = logging.getLogger('django')

def cb_dianru_ios(request):
    ret = {}
    ret['message'] = 'ok'

    logger.info('cb_dianru_ios request params: ' + ' '.join(request.GET.keys()))
    try:
        hashid = request.GET.get('hashid')
        appid = request.GET.get('appid')
        adid = request.GET.get('adid')
        adname = unquote( request.GET.get('adname') )
        userid = request.GET.get('userid')
        deviceid = request.GET.get('deviceid')
        source = request.GET.get('source')
        point = int( request.GET.get('point') )
        ts = request.GET.get('ts')
        checksum = request.GET.get('checksum')

        logger.info('cb_dianru_ios  deviceid:' + deviceid + '  point:' + str(point))
        records = Dianru.objects.filter(hashid=hashid, deviceid=deviceid)
        if len(records) == 0:
            Dianru.objects.create(hashid=hashid, appid=appid, adid=adid, adname=adname,
            userid=userid, deviceid=deviceid, source=source, point=point, ts=ts )

            #update user point record
            user = User.objects.get(dev_id=deviceid)
            PointRecord.objects.create(user=user, channel=u'点入', task=adname, point=point, status='ok')
            user.total_points += point
            user.save()
            return SuccessResponse(ret)
        else:
            ret['message'] = 'duplicate'
            return SuccessResponse(ret)
    except:
        ret['message'] = 'error'
        return SuccessResponse(ret)



def cb_dianru_android(request):
    ret = {}
    ret['message'] = 'error'
    return HttpResponse(ret)

def show_dianru(request):
    ret = {}
    ret['records'] = []

    records = Dianru.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())

    return SuccessResponse(ret)

