
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Mopan
from django.http import HttpResponse

import logging, json
from urllib import unquote

logger = logging.getLogger('django')
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def check_sign(param, sign):
    sk = 'osu1jzrefj1ppofwm3ovjoehy98pot'

    import hashlib
    if hashlib.md5(param+sk).hexdigest() == sign:
        return True

    logger.info('cb_mopan_ios: sign illegal')
    raise MyException('sign illegal')

def cb_mopan_ios(request):

    try:
        imei = request.GET.get('imei')
        param0 = request.GET.get('param0', '')
        cash = int( request.GET.get('cash') )
        trand_no = request.GET.get('trand_no')
        adid = request.GET.get('id')
        appShowName = unquote( request.GET.get('appShowName') )
        sign = request.GET.get('sign')

        param = adid + trand_no + str(cash) + param0
        check_sign(param, sign) 

        logger.info('cb_mopan_ios  imei:' + imei + '  cash:' + str(cash))
        records = Mopan.objects.filter(trand_no=trand_no, imei=imei)
        if len(records) == 0:
            Mopan.objects.create(imei=imei, param0=param0, cash=cash, trand_no=trand_no,
            adid=adid, appShowName=appShowName)

            #update user point record
            user = User.objects.get(dev_id=imei)
            PointRecord.objects.create(user=user, channel=u'磨盘', task=appShowName, point=cash, status='ok')
            user.total_points += cash
            user.save()
    finally:
        return HttpResponse('success')


def cb_mopan_android(request):

    return HttpResponse('error', status=403)


def show_mopan(request):
    ret = {}
    ret['records'] = []

    records = Mopan.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())

    return SuccessResponse(ret)        

