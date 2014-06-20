
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Youmi
from django.http import HttpResponse
    
def syncYoumi():
    records = Youmi.objects.all()
    
    PointRecord.objects.filter(channel='youmi').delete()

    for r in records:
        try:
            user = User.objects.get(dev_id=r.device)
            PointRecord.objects.create(user=user, channel='youmi', task=r.ad, point=r.point, status='ok')
            user.total_points += r.point
            user.save()
        except:
            pass
    
            
def SyncCallback(request):
    channel = request.GET.get('channel', 'all')
    
    syncYoumi()
    
    return HttpResponse('sync success')

