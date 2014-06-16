
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import Channel

def AddChannel(code, name ,description, image, order):
    channels =  Channel.objects.create(code=code, name=name, description=description, image=image, order=order)

def ClearChannels():
    Channel.objects.all().delete()

def InitChannels(request):
    ret = {}

    prefix = 'http://' + request.get_host() + '/res/'
    try:
        ClearChannels()
        AddChannel('youmi', '有米', '中国最好的移动广告平台,提供专业优质的广告服务,让您的广告遍布每个角落', prefix+'logo_youmi.jpg', 1)
        AddChannel('adwo', '安沃', '移动广告专家,致力于打造全新的移动互联网广告平台模式', prefix+'logo_adwo.jpg', 2)
        AddChannel('dianru', '点入', '专注于移动互联网平台开发及网络技术服务,精准化、智能化的综合广告管理平台', prefix+'logo_dianru.png', 3)
        AddChannel('miidi', '米迪', '国内领先的移动广告平台,致力于打造一个多方共赢的手机移动广告平台', prefix+'logo_miidi.jpg', 4)
        AddChannel('domob', '多盟', '中国第一智能手机广告平台', prefix+'logo_domob.jpg', 5)
        AddChannel('yijifen', '易积分', '多快好省', prefix+'logo_yijifen.jpg', 6)
        AddChannel('adview', 'AdView', '中国最大的移动广告交易平台', prefix+'logo_adview.png', 7)
        AddChannel('cocounion', '触控', '开启新纪元,流量更优质,投放更精准', prefix+'logo_cocounion.png', 8)

        return SuccessResponse(ret)
    except :
        return ErrorResponse(E_SYSTEM)

def GetChannels(request):
    ret = {}
    ret['channels'] = []

    try:    
        channels =  Channel.objects.all()
        for c in channels:
            ret['channels'].append(c.toJSON())

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)

