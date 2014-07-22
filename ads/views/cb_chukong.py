
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Chukong
from django.http import HttpResponse
from ads.views.apns import cb_apns_notify

import logging, json
from urllib import unquote

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

logger = logging.getLogger('django')


def cb_chukong_ios(request):

    logger.info('cb_chukong_ios request params: ' + ' '.join(request.GET.keys()))
    try:
        os = request.GET.get('os')
        os_version = request.GET.get('os_version')
        idfa = request.GET.get('idfa')
        mac = request.GET.get('mac')
        imei = request.GET.get('imei')
        ip = request.GET.get('ip')
        transactionid = request.GET.get('transactionid')
        coins = int( request.GET.get('coins') )
        adid = request.GET.get('adid')
        adtitle = unquote( request.GET.get('adtitle') )
        taskname = unquote( request.GET.get('taskname') )
        taskcontent = unquote( request.GET.get('taskcontent') )
        token = request.GET.get('token')
        sign = request.GET.get('sign')

        logger.info('cb_chukong_ios  idfa:' + idfa + '  coins:' + str(coins))
        records = Chukong.objects.filter(transactionid=transactionid, adid=adid)
        if len(records) == 0:
            Chukong.objects.create(os=os, os_version=os_version, idfa=idfa, mac=mac,
            imei=imei, ip=ip, transactionid=transactionid, coins=coins,
            adid=adid, adtitle=adtitle, taskname=taskname, taskcontent=taskcontent, token=token)

            #update user point record
            user = User.objects.get(dev_id=idfa)
            PointRecord.objects.create(user=user, channel=u'触控', task=adtitle, point=coins, status='ok')
            user.total_points += coins
            user.save()

            cb_apns_notify(user.token, adtitle, coins) 
    finally:
        return HttpResponse('success')


def cb_chukong_android(request):

    #logger.info('cb_Chukong_android request params: ' + ' '.join(request.GET.keys()))
    return HttpResponse('error', status=403)


def show_chukong(request):
    ret = {}
    ret['records'] = []

    records = Chukong.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())

    return SuccessResponse(ret)

