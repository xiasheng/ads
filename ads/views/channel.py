
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import Channel

def AddChannel(code, name ,description, order):
    channels =  Channel.objects.create(code=code, name=name, description=description, order=order)

def ClearChannels():
    Channel.objects.all().delete()

def InitChannels(request):
    ret = {}

    try:
        ClearChannels()
        AddChannel('youmi', 'youmi', '中国最好的移动广告平台 提供专业优质的广告服务 让您的广告遍布每个角落', 1)
        AddChannel('adwo', 'adwo', '安沃传媒 移动广告专家', 2)   
        return SuccessResponse(ret)
    except IOError:
        return ErrorResponse(E_SYSTEM)


def GetChannels(request):
    ret = {}
    ret['channles'] = []

    try:    
        channels =  Channel.objects.all()
        for c in channels:
            ret['channles'].append(c.toJSON())

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)

