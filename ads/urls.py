
# -*- coding: utf-8 -*- 

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from views.helloworld import hello
from views.user import Init, Update, GetTopUser, RequireAuth, RequireSign, ShowAllUser, SetScore, CreateTestUsers
from views.channel import GetChannels, InitChannels
from views.point import GetPoint, GetPointRecord
from views.version import HasNewVersion
from views.exchange import InitProducts, QueryProducts, ExTelPhone, ExQb, ExAlipay, ExRecord, ExConfirm, ExProblem
from views.cb_adwo import cb_adwo_ios, cb_adwo_android, show_adwo
from views.cb_youmi import cb_youmi_ios, cb_youmi_android, show_youmi
from views.cb_yjf import cb_yjf_ios, cb_yjf_android, show_yjf
from views.cb_dianru import cb_dianru_ios, cb_dianru_android, show_dianru
from views.cb_domob import cb_domob_ios, cb_domob_android, show_domob
from views.cb_guomob import cb_guomob_ios, cb_guomob_android, show_guomob
from views.cb_waps import cb_waps_ios, cb_waps_android, show_waps
from views.cb_miidi import cb_miidi_ios, cb_miidi_android, show_miidi
from views.cb_dianjoy import cb_dianjoy_ios, cb_dianjoy_android, show_dianjoy
from views.cb_chukong import cb_chukong_ios, cb_chukong_android, show_chukong
from views.cb_mopan import cb_mopan_ios, cb_mopan_android, show_mopan
from views.callback import SyncCallback

from views.statistics import Stat
from views.apns import TestApns
from views.game import ZhuanPan, GetGameRecord
from views.qiubai import Spider, QiuShi
from views.duiba import QueryCredit, ConsumeCredit, ResultCredit

from django.contrib import admin

def disableDefaultAdmin():
    from django.contrib.auth.models import User
    #from django.contrib.sites.models import Site
    from django.contrib.auth.models import Group

    admin.site.unregister(User)
    admin.site.unregister(Group)
    #admin.site.unregister(Site)


admin.autodiscover()
disableDefaultAdmin()

from urllib import unquote
urlpatterns = patterns('',
    
    (r'^51admin/', include(admin.site.urls)),

    #url(r'^hello$', hello),
    url(r'^user/init/$', Init),
    url(r'^user/update/$', RequireAuth(Update)),
    url(r'^user/showall/$', ShowAllUser),
    url(r'^user/test/setscore/$', RequireAuth(SetScore)),
    url(r'user/test/create/', CreateTestUsers),

    url(r'^channels/$', RequireSign(GetChannels)),
    url(r'^channels/init/$', InitChannels),
    url(r'^score/$', RequireAuth(GetPoint)),
    url(r'^score/records/$', RequireAuth(GetPointRecord)),

    url(r'^products/init/$', InitProducts),
    url(r'^products/query/$', RequireSign(QueryProducts)),
    url(r'^exchange/telphone/$', RequireAuth(ExTelPhone)),
    url(r'^exchange/qb/$', RequireAuth(ExQb)),
    url(r'^exchange/alipay/$', RequireAuth(ExAlipay)),
    url(r'^exchange/records/$', RequireAuth(ExRecord)),
    url(r'^exconfirm/$', ExConfirm),
    url(r'^exproblem/$', ExProblem),

    url(r'^top/score/$', RequireSign(GetTopUser)),
    url(r'^version/hasnew/$', RequireSign(HasNewVersion)),

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

    url(r'^callback/guomob/ios$', cb_guomob_ios),
    url(r'^callback/guomob/android$', cb_guomob_android),
    url(r'^callback/guomob/show$', show_guomob),

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

    url(r'^admin/stat/', Stat),
    url(r'^apns/test/', TestApns),

    url(r'^game/zhuanpan/', RequireAuth(ZhuanPan)),
    url(r'^game/records/$', RequireAuth(GetGameRecord)),

    url(r'^spider/qiubai/', Spider),
    url(r'^duanzi/qiushi/', QiuShi),
    url(r'^duiba/query/', QueryCredit),
    url(r'^duiba/consume/', ConsumeCredit),
    url(r'^duiba/result/', ResultCredit),
)

#urlpatterns += staticfiles_urlpatterns()
