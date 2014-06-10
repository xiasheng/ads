
# -*- coding: utf-8 -*-  

from ads.views.common import *

def HasNewVersion(request):
    ret = {}
    ret['url'] = 'http://www.abc.com/ads/v1.0.0'
    return SuccessResponse(ret)

