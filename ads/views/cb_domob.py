
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Domob
from django.http import HttpResponse

import logging, json
from urllib import unquote
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

logger = logging.getLogger('django')

def check_sign(param, sign):
    sk = '6243ef86'

    import hashlib
    if hashlib.md5(param+sk).hexdigest() == sign:
        return True

    logger.info('cb_domob_ios: sign illegal')
    raise MyException('sign illegal')


def cb_domob_ios(request):
    ret = {}
    ret['message'] = 'success'

    try:
        orderid = request.GET.get('orderid')
        pubid = request.GET.get('pubid')
        ad = unquote( request.GET.get('ad') )
        adid = request.GET.get('adid')
        user = request.GET.get('user')
        device = request.GET.get('device')
        channel = request.GET.get('channel')
        price_raw = request.GET.get('price')
        price = float( price_raw )
        point = int( request.GET.get('point') )
        ts = request.GET.get('ts')
        sign = request.GET.get('sign')

        param = "ad=%sadid=%schannel=%sdevice=%sorderid=%spoint=%dprice=%spubid=%sts=%suser=%s" \
                %(ad, adid, channel, device, orderid, point,price_raw, pubid, ts, user)
        check_sign(param, sign) 

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
    finally:
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

