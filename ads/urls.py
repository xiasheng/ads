
from django.conf.urls import patterns, include, url

from views.helloworld import hello
from views.user import Init, Update, GetTopUser, RequireAuth, ShowAllUser
from views.channel import GetChannels, InitChannels
from views.point import GetPoint, GetPointRecord
from views.version import HasNewVersion
from views.exchange import ExTelPhone, ExQb, ExAlipay, ExRecord, ExConfirm, ExProblem
from views.cb_adwo import cb_adwo_ios, cb_adwo_android, show_adwo
from views.cb_youmi import cb_youmi_ios, cb_youmi_android, show_youmi
from views.cb_yjf import cb_yjf_ios, cb_yjf_android, show_yjf
from views.cb_dianru import cb_dianru_ios, cb_dianru_android, show_dianru
from views.cb_domob import cb_domob_ios, cb_domob_android, show_domob
from views.cb_waps import cb_waps_ios, cb_waps_android, show_waps
from views.cb_miidi import cb_miidi_ios, cb_miidi_android, show_miidi
from views.cb_dianjoy import cb_dianjoy_ios, cb_dianjoy_android, show_dianjoy
from views.cb_chukong import cb_chukong_ios, cb_chukong_android, show_chukong
from views.cb_mopan import cb_mopan_ios, cb_mopan_android, show_mopan
from views.callback import SyncCallback

from views.statistics import Stat

urlpatterns = patterns('',

    url(r'^hello/$', hello),
    url(r'^user/init/$', Init),
    url(r'^user/update/$', RequireAuth(Update)),
    url(r'^user/showall/$', ShowAllUser),

    url(r'^channels/$', GetChannels),
    url(r'^channels/init/$', InitChannels),
    url(r'^score/$', RequireAuth(GetPoint)),
    url(r'^score/records/$', RequireAuth(GetPointRecord)),

    url(r'^exchange/telphone/$', RequireAuth(ExTelPhone)),
    url(r'^exchange/qb/$', RequireAuth(ExQb)),
    url(r'^exchange/alipay/$', RequireAuth(ExAlipay)),
    url(r'^exchange/records/$', RequireAuth(ExRecord)),
    url(r'^exconfirm/$', ExConfirm),
    url(r'^exproblem/$', ExProblem),

    url(r'^top/score/$', GetTopUser),
    url(r'^version/hasnew/$', HasNewVersion),

    url(r'^callback/adwo/ios$', cb_adwo_ios),
    url(r'^callback/adwo/android$', cb_adwo_android),
    url(r'^callback/adwo/show$', show_adwo),

    url(r'^callback/youmi/ios$', cb_youmi_ios),
    url(r'^callback/youmi/android$', cb_youmi_android),
    url(r'^callback/youmi/show$', show_youmi),

    url(r'^callback/yjf/ios$', cb_yjf_ios),
    url(r'^callback/yjf/android$', cb_yjf_android),
    url(r'^callback/yjf/show$', show_yjf),

    url(r'^callback/dianru/ios$', cb_dianru_ios),
    url(r'^callback/dianru/android$', cb_dianru_android),
    url(r'^callback/dianru/show$', show_dianru),

    url(r'^callback/domob/ios$', cb_domob_ios),
    url(r'^callback/domob/android$', cb_domob_android),
    url(r'^callback/domob/show$', show_domob),

    url(r'^callback/waps/ios$', cb_waps_ios),
    url(r'^callback/waps/android$', cb_waps_android),
    url(r'^callback/waps/show$', show_waps),

    url(r'^callback/miidi/ios$', cb_miidi_ios),
    url(r'^callback/miidi/android$', cb_miidi_android),
    url(r'^callback/miidi/show$', show_miidi),

    url(r'^callback/dianjoy/ios$', cb_dianjoy_ios),
    url(r'^callback/dianjoy/android$', cb_dianjoy_android),
    url(r'^callback/dianjoy/show$', show_dianjoy),

    url(r'^callback/chukong/ios$', cb_chukong_ios),
    url(r'^callback/chukong/android$', cb_chukong_android),
    url(r'^callback/chukong/show$', show_chukong),

    url(r'^callback/mopan/ios$', cb_mopan_ios),
    url(r'^callback/mopan/android$', cb_mopan_android),
    url(r'^callback/mopan/show$', show_mopan), 

    url(r'^callback/sync$', SyncCallback),

    url(r'^admin/stat/', Stat)
)
