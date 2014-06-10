
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Adwo
        
def cb_adwo(request):
    ret = {}
    
    try:    
        appid = request.GET.get('appid')
        adname = request.GET.get('adname')
        adid = request.GET.get('adid')
        device = request.GET.get('device')
        idfa = request.GET.get('idfa')
        point = int(request.GET.get('point'))
        ts = request.GET.get('ts')
        sign = request.GET.get('sign')
        
        records = Adwo.objects.filter(device=device, idfa=idfa, ts=ts)
        if len(records) == 0:
            Adwo.objects.create(appid=appid, adname=adname, adid=adid, device=device, idfa=idfa, point=point, ts=ts)
            
            #update user point record
            user = User.objects.get(mac=device)
            PointRecord.objects.create(user=user, channel='adwo', task=adname, point=point, status='ok')
            user.total_points += point
            user.save()
        
    finally:
        return SuccessResponse(ret)

