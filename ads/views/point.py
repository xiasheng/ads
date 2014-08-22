
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import PointRecord, ZhuanPanRecord


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
        records = PointRecord.objects.filter(user=request.META['USER']).order_by('-id')
        
        for r in records:
            ret['records'].append(r.toJSON())

        records = ZhuanPanRecord.objects.filter(user=request.META['USER']).order_by('-id')

        for r in records:
            rr = {}
            rr['status'] = 'ok'
            rr['type'] = '+'
            rr['increase'] = r.point
            rr['task'] = u'钱庄'
            rr['createtime'] = r.time_created
            rr['channel'] = u'游戏'
            ret['records'].append(rr)
        
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)

