
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Youmi
from django.http import HttpResponse
 
import logging, json
from urllib import unquote

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

logger = logging.getLogger('django')
 
def check_sign(param, sign):
    sk = '1ba4555d3feebded'
    
    import hashlib
    if hashlib.md5(param+sk).hexdigest() == sign:
        return True
        
    logger.info('cb_youmi_ios: sign illegal')
    raise MyException('sign illegal')      

def cb_youmi_ios(request):
    try:
        order = request.GET.get('order')
        app = request.GET.get('app')
        ad = unquote( request.GET.get('ad') )
        adid = request.GET.get('adid')
        user = request.GET.get('user')
        device = request.GET.get('device')
        chn = request.GET.get('chn')
        price_raw = request.GET.get('price')
        price = float(price_raw)
        point = int(request.GET.get('points'))
        ts = request.GET.get('time')
        sig = request.GET.get('sig')
        sign = request.GET.get('sign')

        param = "ad=%sadid=%sapp=%schn=%sdevice=%sorder=%spoints=%dprice=%ssig=%stime=%suser=%s" \
                %(ad, adid, app, chn, device, order, point, price_raw, sig, ts, user)
        check_sign(param, sign)    


        logger.info('cb_youmi_ios  device:' + device + '  point:' + str(point))
        records = Youmi.objects.filter(order=order, device=device)
        if len(records) == 0:
            Youmi.objects.create(type='ios',order=order, app=app, ad=ad, adid=str(adid), user=user, device=device,
            chn=chn, price=price, point=point, ts=ts)

            #update user point record
            user = User.objects.get(dev_id=device)
            PointRecord.objects.create(user=user, channel=u'有米', task=ad, point=point, status='ok')
            user.total_points += point
            user.save()
    finally:
        return HttpResponse('success')


def cb_youmi_android(request):
    
    try:
        order = request.GET.get('order')
        app = request.GET.get('app')
        ad = request.GET.get('ad')
        user = request.GET.get('user')
        device = request.GET.get('device')
        chn = request.GET.get('chn')
        point = int(request.GET.get('points'))
        ts = request.GET.get('time')
        #sign = request.GET.get('sign')

        logger.info('cb_youmi_android  device:' + device + '  point:' + str(point))
        records = Youmi.objects.filter(order=order, device=device)
        if len(records) == 0:
            Youmi.objects.create(type='android',order=order, app=app, ad=unquote(ad), user=user, device=unquote(device),
            chn=chn, point=point, ts=ts)

            #update user point record
            if len(device) == 12:
                user = User.objects.get(mac=device)
            else:
                user = User.objects.get(dev_id=device)
            PointRecord.objects.create(user=user, channel=u'有米', task=ad, point=point, status='ok')
            user.total_points += point
            user.save()
            return HttpResponse('success')
        else:
            return HttpResponse('duplicate', status=403)
    except:
        logger.info('cb_youmi_android  failed' )
        return HttpResponse('error')   

def show_youmi(request):
    ret = {}
    ret['records'] = []

    records = Youmi.objects.all().order_by('-id')[:10]
    for r in records:
        ret['records'].append(r.toJSON())
    
    return SuccessResponse(ret)

