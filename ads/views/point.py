
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import PointRecord


def GetPoint(request):
    ret = {}

    try:    
        ret['score'] = request.META['USER'].total_points
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)


def GetPointRecord(request):
    ret = {}
    ret['records'] = []

    try:    
        records = PointRecord.objects.filter(user=request.META['USER'])
        
        for r in records:
            ret['records'].append(r.toJSON())
        
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)

