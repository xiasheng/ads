
from django.conf.urls import patterns, include, url

from views.helloworld import hello
from views.user import Init, Update, GetTopUser, RequireAuth
from views.channel import GetChannels, InitChannels
from views.point import GetPoint, GetPointRecord
from views.version import HasNewVersion
from views.exchange import ExTelPhone, ExQb, ExAlipay, ExRecord, ExConfirm
from views.callback import cb_adwo

urlpatterns = patterns('',

    url(r'^hello/$', hello),
    url(r'^user/init/$', Init),
    url(r'^user/update/$', RequireAuth(Update)),
    url(r'^channels/$', GetChannels),
    url(r'^channels/init/$', InitChannels),
    url(r'^score/$', RequireAuth(GetPoint)),
    url(r'^score/records/$', RequireAuth(GetPointRecord)),

    url(r'^exchange/telphone/$', RequireAuth(ExTelPhone)),
    url(r'^exchange/qb/$', RequireAuth(ExQb)),
    url(r'^exchange/alipay/$', RequireAuth(ExAlipay)),
    url(r'^exchange/records/$', RequireAuth(ExRecord)),
    url(r'^exconfirm/$', ExConfirm),

    url(r'^top/score/$', GetTopUser),
    url(r'^version/hasnew/$', HasNewVersion),
    url(r'^callback/adwo/ios/$', cb_adwo),

)
