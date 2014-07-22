
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Yijifen
from django.http import HttpResponse
from ads.views.apns import cb_apns_notify

import logging, json
from urllib import unquote

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

logger = logging.getLogger('django')

def cb_yjf_ios(request):
    ret = {}
    ret['message'] = 'ok'
    
    #logger.info('cb_yjf_ios request params: ' + ' '.join(request.GET.keys()))
    try:
        uuid = request.GET.get('uuid')
        userId = request.GET.get('userId')
        score = int( request.GET.get('score') )
        exchangetime = request.GET.get('exchangetime')
        plat = request.GET.get('plat')
        idfa = request.GET.get('idfa')
        appName = unquote( request.GET.get('appName'))
        adId = request.GET.get('adId')
        adName = unquote( request.GET.get('adName') )
        sign = request.GET.get('sign')

        logger.info('cb_yjf_ios  idfa:' + idfa + '  score:' + str(score))
        records = Yijifen.objects.filter(uuid=uuid, idfa=idfa, exchangetime=exchangetime)
        if len(records) == 0:
            Yijifen.objects.create(uuid=uuid, userId=userId, score=score, exchangetime=exchangetime, 
            plat=plat, idfa=idfa, appName=appName, adId=adId, adName=adName )

            #update user point record
            user = User.objects.get(dev_id=idfa)
            PointRecord.objects.create(user=user, channel=u'易积分', task=adName, point=score, status='ok')
            user.total_points += score
            user.save()

            cb_apns_notify(user.token, adName, score)  
    finally:
        return SuccessResponse(ret)



def cb_yjf_android(request):
    ret = {}
    ret['message'] = 'error'
    return HttpResponse(ret)

def show_yjf(request):
    ret = {}
    ret['records'] = []

    records = Yijifen.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())

    return SuccessResponse(ret)
