
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import Channel

def AddChannel(code, name ,description, image, order, is_enable=True):
    channels =  Channel.objects.create(code=code, name=name, description=description, image=image, order=order, is_enable=is_enable)

def ClearChannels():
    Channel.objects.all().delete()

def InitChannels(request):
    ret = {}

    prefix = 'http://' + request.get_host() + '/res/'
    try:
        ClearChannels()
        AddChannel('dianjoy', '点乐', '全国领先的手机智能平台, 专注于发掘移动营销领域的潜力与价值, 倾力于打造移动广告平台', prefix+'logo_dianjoy.png', 10)
        AddChannel('youmi', '有米', '中国最好的移动广告平台,提供专业优质的广告服务,让您的广告遍布每个角落', prefix+'logo_youmi.png', 20)
        AddChannel('miidi', '米迪', '国内领先的移动广告平台,致力于打造一个多方共赢的手机移动广告平台', prefix+'logo_miidi.jpg', 30)
        AddChannel('adwo', '安沃', '移动广告专家,致力于打造全新的移动互联网广告平台模式', prefix+'logo_adwo.png', 40)
        AddChannel('domob', '多盟', '中国第一智能手机广告平台', prefix+'logo_domob.png', 50)
        AddChannel('waps', '万普', '中国领先的移动营销服务提供商,致力于为全球广告客户提供基于移动互联网的效果广告及整合营销服务', prefix+'logo_waps.png', 60)
        AddChannel('yijifen', '易积分', '易积分移动广告平台', prefix+'logo_yijifen.png', 70)
        AddChannel('guomob', '果盟', '国内最注重效果的移动广告平台', prefix+'logo_guomob.jpg', 80)
        AddChannel('dianru', '点入', '专注于移动互联网平台开发及网络技术服务,精准化、智能化的综合广告管理平台', prefix+'logo_dianru.png', 90)
        AddChannel('mobsmar', '指盟', '灵活定制的移动广告解决方案无论提升品牌还是绩效都能轻松应对', prefix+'logo_mobsmar.png', 100)
        AddChannel('mobsmar', '力美', '中国领先的移动营销解决方案提供商', prefix+'logo_limei.png', 110)
        AddChannel('mobsmar', '触控', '触控广告平台新版上线，开启新纪元，流量更优质，投放更精准！', prefix+'logo_chukong.png', 120)
        AddChannel('mopan', '磨盘', '中国最具探索力数字营销平台！', prefix+'logo_mopan.png', 130) 
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)

def GetChannels(request):
    ret = {}
    ret['channels'] = []

    try:
        channels =  Channel.objects.filter(is_enable=True).order_by('order')
        for c in channels:
            ret['channels'].append(c.toJSON())

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM) 
