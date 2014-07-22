
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Miidi
from django.http import HttpResponse
from ads.views.apns import cb_apns_notify

import logging, json
from urllib import unquote
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


logger = logging.getLogger('django')

def check_sign(param, sign):
    sk = 'z50b95b12zb3rc87uiaaz2rvpm8zw1'

    import hashlib
    if hashlib.md5(param+sk).hexdigest() == sign:
        return True

    logger.info('cb_miidi_ios: sign illegal')
    raise MyException('sign illegal')

def cb_miidi_ios(request):
    ret = {}
    ret['message'] = 'success'

    try:
        adid = request.GET.get('id')
        trand_no = request.GET.get('trand_no')
        cash = int (request.GET.get('cash') )
        imei = request.GET.get('imei')
        bundleId = request.GET.get('bundleId')
        param0 = request.GET.get('param0')
        appName = unquote( request.GET.get('appName') )
        sign = request.GET.get('sign')
        
        param = adid + trand_no + str(cash) + param0
        check_sign(param, sign)  

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

            cb_apns_notify(user.token, appName, cash) 
    finally:
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

