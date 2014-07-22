
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, ZhuanPanRecord
import random, time

zp = [8, 0, 2, 10, 5, 1, 100, 5, 10, 1, 2, 8, 0, 1, 2, 1]

def ZhuanPan(request):
    ret = {}

    try:
        user = request.META['USER']
        
        t_now = int(time.time())
        t_begin = t_now - 24 * 3600
        t_end = t_now
        
        c = ZhuanPanRecord.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).count()
        if c >= 10:
            ret['angle'] = 0
            ret['score'] = 0
            ret['cooltime'] = 60 * 60
            ret['status'] = 1;  
            return SuccessResponse(ret)

        random.seed()
        r = random.randint(0, len(zp)-1)

        if zp[r] == 100:
            r = random.randint(0, len(zp)-1)

        ret['angle'] = r
        ret['score'] = zp[r]
        ret['cooltime'] = 60
        ret['status'] = 0;
        
        ZhuanPanRecord.objects.create(user=user, point=zp[r], angle=r)
        
        user.total_points += zp[r]

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)

