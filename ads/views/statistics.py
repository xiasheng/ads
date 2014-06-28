
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import User, PointRecord, Dianjoy, Youmi, Miidi, Adwo, Domob, Waps, Yijifen, Guomob, Dianru, Mobsmar, Chukong, Mopan
from django.db.models import Sum

import time, datetime, json


def generateEmailContent(c):
    ret = '\r\n'
    ret += u' 今日新增用户：' + str(c['new_user']) + '\r\n'
    ret += u' 今日新增积分：' + str(c['new_point']) + '\r\n\r\n'
    ret += u' 积分详情' + '\r\n'
    ret += u'-------------------------------------------------------' + '\r\n'
    ret += u'          点义米：' + str(c['platform']['youmi']) + '\r\n'
    ret += u'          米迪：' + str(c['platform']['miidi']) + '\r\n'
    ret += u'          安沃：' + str(c['platform']['adwo']) + '\r\n'
    ret += u'          多盟：' + str(c['platform']['domob']) + '\r\n'
    ret += u'          万普：' + str(c['platform']['waps']) + '\r\n'
    ret += u'          易积分：' + str(c['platform']['yjf']) + '\r\n'
    ret += u'          果盟：' + str(c['platform']['guomob']) + '\r\n'
    ret += u'          点入：' + str(c['platform']['dianru']) + '\r\n'
    ret += u'          指盟：' + str(c['platform']['mobsmar']) + '\r\n'
    #ret += u'          力美：' + str(c['platform']['limei']) + '\r\n'
    ret += u'          触控：' + str(c['platform']['chukong']) + '\r\n'
    ret += u'          磨盘：' + str(c['platform']['mopan']) + '\r\n'
    return ret

def notifyEmail(title, content):
    from django.conf import settings
    from django.core.mail import send_mail, EmailMessage
    send_mail(title, content, settings.EMAIL_HOST_USER, settings.EMAIL_RECIPIENTS, fail_silently=False)
    #msg = EmailMessage(title, content, settings.EMAIL_HOST_USER, settings.EMAIL_RECIPIENTS)
    #msg.content_subtype = 'html'
    #msg.send()


def Stat(request):
    ret = {}
 
       
    t_now = int(time.time())

    t_end = t_now
    t_begin = t_now - 24 * 3600

    t_begin = int( request.GET.get('from', t_begin))
    t_end = int( request.GET.get('to', t_end))

    try:    
        count_new_user = User.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).count()
        new_point = PointRecord.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('point'))['point__sum']

        points_dianjoy = Dianjoy.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('currency'))['currency__sum']
        points_youmi = Youmi.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('point'))['point__sum']
        points_miidi = Miidi.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('cash'))['cash__sum']
        points_adwo = Adwo.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('point'))['point__sum']
        points_domob = Domob.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('point'))['point__sum']
        points_waps = Waps.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('points'))['points__sum']
        points_yjf = Yijifen.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('score'))['score__sum']
        points_guomob = Guomob.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('points'))['points__sum']
        points_dianru = Dianru.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('point'))['point__sum']
        points_mobsmar = Mobsmar.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('points'))['points__sum']
        #points_limei = Limei.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('point'))['point__sum']
        points_chukong = Chukong.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('coins'))['coins__sum']
        points_mopan = Mopan.objects.filter(time_created__gt=t_begin).filter(time_created__lt=t_end).aggregate(Sum('cash'))['cash__sum']

        ret['new_user']  = count_new_user
        ret['new_point'] = new_point
        p = {}
        p['dianjoy'] = points_dianjoy
        p['youmi'] = points_youmi
        p['miidi'] = points_miidi
        p['adwo'] = points_adwo
        p['domob'] = points_domob
        p['waps'] = points_waps
        p['yjf'] = points_yjf
        p['guomob'] = points_guomob
        p['dianru'] = points_dianru
        p['mobsmar'] = points_mobsmar
        #p['limei'] = 0
        p['chukong'] = points_chukong
        p['mopan'] = points_mopan

        ret['platform'] = p
        title = 'Moremoney Report %s' %(datetime.date.fromtimestamp(time.time()))
        content = generateEmailContent(ret)
        notifyEmail(title, content)
         
        return SuccessResponse(ret)
    except IOError:
        return ErrorResponse(E_SYSTEM)


